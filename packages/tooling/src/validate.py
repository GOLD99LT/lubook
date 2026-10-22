#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate.py — 手册客观质检：frontmatter 完整性、id 一致/唯一、part 与目录一致、
图片与交叉引用死链、echarts JSON、公式/容器/details 配对、孤儿章节。

用法：python packages/tooling/src/validate.py [--src docs]
复用 build_single_html 的 frontmatter/SUMMARY 解析，保证口径一致。
"""
import os, re, sys, json, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from paths_util import add_common_args, resolve_src
import build_single_html as B

_args, _rest = add_common_args().parse_known_args()
B.DOCS = resolve_src(_args)
DOCS = B.DOCS
errors, warnings = [], []
def err(f, m): errors.append('%s: %s' % (f, m))
def warn(f, m): warnings.append('%s: %s' % (f, m))

DIR_PART = {'basics':1, 'components':2, 'opamp':3, 'digital':4, 'mcu':5,
            'power':6, 'pcb':7, 'practice':8, 'quizbank':9}

parts = B.parse_summary()
summary_paths = []
for p in parts:
    for _t, rel in p['items']:
        summary_paths.append(rel)

seen_ids, md_files = {}, []
for rel in summary_paths:
    fp = os.path.join(DOCS, rel.replace('/', os.sep))
    if not os.path.exists(fp):
        continue  # 未生产占位，构建时已 warn
    text = open(fp, encoding='utf-8').read()
    fm, body = B.split_frontmatter(text)
    _fm_end = text.find('\n---', 3)
    _fm_raw = text[3:_fm_end] if _fm_end > 0 else ''
    fm_raw = B.raw_frontmatter(text) if hasattr(B, 'raw_frontmatter') else text[3:text.find(chr(10) + '---', 3)]
    fid = os.path.basename(rel)[:-3]
    md_files.append((rel, fp, fm, body, fid))

    # ---- frontmatter ----
    # YAML 语法体检：本仓 frontmatter 由简单解析器读取，但 VitePress 用真正的 YAML 解析器。
    # 一旦写成 VitePress 读不了的形式，validate 全绿而构建直接失败。2026-10-22 的实例：
    # sources 里写了 `- [文字](url)`，`[` 被 YAML 当成 flow sequence 起点，整站构建挂掉。
    # 这里用最小规则拦住最容易踩的几类。
    for _lineno, _line in enumerate(_fm_raw.splitlines(), 1):
        _m = re.match(r'^(\s*)-\s+(.+)$', _line)
        if not _m:
            continue
        _item = _m.group(2).strip()
        if _item[:1] in ('[', '{', '*', '&', '!', '|', '>', '%', '@'):
            err(rel, 'frontmatter 第 %d 行列表项以 %r 开头，YAML 会误解析（改成纯文本或用引号包裹）: %s'
                % (_lineno, _item[0], _item[:40]))
        elif ': ' in _item and _item[:1] not in ('"', "'"):
            # 只提醒不判死：`- 书名: 副标题` 会被 YAML 解析成映射而不是字符串。
            # 这类写法不会炸构建（VitePress 静默接受），但 sources 会从字符串变成字典，
            # 属于"解析结果与作者意图不符"，逐条改成本高，先留作可见的提醒。
            warn(rel, 'frontmatter 第 %d 行列表项的 ": " 会被 YAML 当成映射: %s'
                 % (_lineno, _item[:40]))

    for key in ('id', 'title', 'part', 'order', 'tags', 'difficulty', 'status'):
        if key not in fm or fm[key] in (None, '', []):
            err(rel, 'frontmatter 缺少或为空: %s' % key)
    if not fm.get('sources'):
        err(rel, 'frontmatter 缺少 sources（至少 1 条）')
    if fm.get('id') and fm['id'] != fid:
        err(rel, 'id(%s) 与文件名(%s) 不一致' % (fm['id'], fid))
    _id = fm.get('id') or fid
    if _id in seen_ids:
        err(rel, 'id 重复: %s（与 %s）' % (_id, seen_ids[_id]))
    else:
        seen_ids[_id] = rel
    top = rel.split('/')[0]
    exp = DIR_PART.get(top)
    if exp and 'part' in fm and fm['part'] != exp:
        err(rel, 'part=%s 与目录 %s（应为 %s）不一致' % (fm['part'], top, exp))
    if 'difficulty' in fm and fm['difficulty'] not in (1, 2, 3):
        err(rel, 'difficulty 非法: %r' % fm['difficulty'])
    if 'status' in fm and fm['status'] not in ('draft', 'published', 'deprecated'):
        err(rel, 'status 非法: %r' % fm['status'])
    if 'order' in fm and not isinstance(fm['order'], int):
        err(rel, 'order 应为整数: %r' % fm['order'])

    # ---- 图片引用 ----
    for m in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', body):
        target = m.group(1).strip()
        if target.startswith(('http', 'data:')):
            continue
        t = target.split()[0]
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(fp), t))):
            err(rel, '图片不存在: %s' % target)

    # ---- 普通链接（先剔除图片）----
    body_no_img = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', body)
    for m in re.finditer(r'\[[^\]]+\]\(([^)]+)\)', body_no_img):
        target = m.group(1).strip()
        if target.startswith(('http', '#', 'data:')) or not target:
            continue
        t = target.split()[0]
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(fp), t))):
            err(rel, '链接目标不存在（死链）: %s' % target)

    # ---- echarts ----
    for blk in re.finditer(r'```echarts\s*\n(.*?)```', body, re.S):
        try:
            json.loads(blk.group(1))
        except Exception as e:
            err(rel, 'echarts JSON 非法: %s' % e)

    # ---- 配对 ----
    if body.count('$$') % 2 != 0:
        err(rel, '块公式 $$ 不配对（奇数个）')
    opens = len(re.findall(r'^:::[ \t]+\S+', body, re.M))
    closes = len(re.findall(r'^:::[ \t]*$', body, re.M))
    if opens != closes:
        err(rel, '自定义容器 ::: 不配对（开始 %s / 结束 %s）' % (opens, closes))
    do = len(re.findall(r'<details', body))
    dc = len(re.findall(r'</details>', body))
    if do != dc:
        err(rel, 'details 不配对（开始 %s / 结束 %s）' % (do, dc))

    # ---- 结构 ----
    if not re.search(r'^#\s+', body, re.M):
        err(rel, '缺少一级标题 #')
    h2 = len(re.findall(r'^##\s+', body, re.M))
    if h2 < 3:
        warn(rel, '二级标题过少（%s），模块可能不全' % h2)

# ---- 孤儿章节（磁盘有、SUMMARY 无）----
# 跳过清单必须与 freeze_manifest.py 的 skip 一致，否则 index.md 会恒定产生一条假告警。
for root, _d, files in os.walk(DOCS):
    for f in files:
        if f.endswith('.md') and f not in ('index.md', 'SUMMARY.md', 'LICENSE-docs.md'):
            rel = os.path.relpath(os.path.join(root, f), DOCS).replace(os.sep, '/')
            if rel not in summary_paths:
                warn(rel, '磁盘文件未出现在 SUMMARY（孤儿章节）')

print('==== validate 报告 ====')
print('已检查章节: %d' % len(md_files))
print('SUMMARY 占位（未生产）: %d' % (len(summary_paths) - len(md_files)))
print('硬错误 %d，提醒 %d' % (len(errors), len(warnings)))
for e in errors:
    print(' [ERROR] ' + e)
for w in warnings:
    print(' [warn] ' + w)
sys.exit(1 if errors else 0)
