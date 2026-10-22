#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
freeze_manifest.py — 冻结内容基线（纯 Python 标准库，零第三方依赖）。

数据源：apps/<app>/docs/SUMMARY.md + 各章 frontmatter + 磁盘扫描。
产物（按分册 slug 命名，ADR-0006 / NAMING）：
  .generated/<app>-content-manifest.json   内容清单（生成物，不入库；.generated/ 在 .gitignore）
  tests/<app>.routes.snapshot.json         已发布 clean URL 的排序列表（入库，CI 比对基准）
  tests/<app>.manifest.snapshot.json       内容指纹：章节数/标题序列/图片总数/SVG 数/接地数/整体 checksum（入库）

结构严格按 ARCHITECTURE §3.1：
  ContentManifest { appId, revision, docs[] }
  ContentDoc { id(=相对路径, 如 opamp/inverting-amplifier.md), path, url(clean URL),
               title, part(篇名), order, tags[], difficulty?, images[], checksum }
  id / url 不可重复；SUMMARY↔磁盘必须双向对齐，否则立即非零退出。
解析逻辑复用 packages/tooling/src/build_vp_sidebar.py（与 sidebar / 离线构建同口径）。
参数化：--app/--src（默认对 hardware 等价）。
"""
import os, re, sys, json, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from paths_util import REPO_ROOT, add_common_args, resolve_src
_args, _ = add_common_args().parse_known_args()

ROOT = REPO_ROOT
DOCS = resolve_src(_args)
GEN_DIR = os.path.join(ROOT, '.generated')
TESTS_DIR = os.path.join(ROOT, 'tests')
APP_ID = _args.app

import build_vp_sidebar as S
S.DOCS = DOCS  # 与本脚本口径一致，避免 import 时的默认 src 漂移


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def normalize_text_for_hash(b):
    """跨平台换行归一：CRLF/CR -> LF（与仓库 blob 一致），保证 Windows(CRLF) 与
    Linux(LF) 检出时同一份逻辑内容算出相同 checksum。入参为文件原始字节。"""
    return b.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')


def clean_url(rel):
    """opamp/inverting-amplifier.md -> /opamp/inverting-amplifier（VitePress clean URL）。"""
    p = rel.replace('\\', '/')
    if p.startswith('./'):
        p = p[2:]
    if p.endswith('.md'):
        p = p[:-3]
    return '/' + p


def extract_images(body, doc_fp, src=DOCS):
    """正文图片引用（与 validate.py 同口径），返回 src 相对路径列表。
    按出现顺序收集、不去重——imageTotal 对齐 §1「418 处图片引用」。"""
    out = []
    for m in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', body):
        target = m.group(1).strip()
        if target.startswith(('http', 'data:')):
            continue
        t = target.split()[0]
        abs_t = os.path.normpath(os.path.join(os.path.dirname(doc_fp), t))
        out.append(os.path.relpath(abs_t, src).replace(os.sep, '/'))
    return out


def count_svg(src=DOCS):
    base = os.path.join(src, 'assets')
    return sum(1 for _r, _d, fs in os.walk(base) for f in fs if f.endswith('.svg'))


def scan_grounds_count(src=DOCS):
    """子进程跑 scan_grounds.py 并解析末行接地符号总数（不重复实现扫描逻辑）。
    显式传 --src 让多 app 各自扫描。"""
    env = dict(os.environ)
    env['PYTHONUTF8'] = '1'
    p = subprocess.run([sys.executable, os.path.join(HERE, 'scan_grounds.py'),
                        '--src', src],
                       capture_output=True, env=env)
    out = p.stdout.decode('utf-8', 'replace')
    m = re.search(r'共识别接地符号\s*(\d+)\s*个', out)
    return int(m.group(1)) if m else -1


def build_manifest(app=APP_ID, src=DOCS):
    """返回 (manifest, routes, fingerprint)；任何一致性错误先打印再 SystemExit(1)。
    显式 app/src 优先（run_quality 多 app 复用），默认取模块级（CLI 解析值）。"""
    src = os.path.abspath(src)
    S.DOCS = src  # 让 parse_summary/frontmatter 走同一 src
    errors = []
    parts = S.parse_summary()
    docs = []
    for part in parts:
        for disp, rel in part['items']:
            rel = rel.replace('\\', '/')
            fp = os.path.join(src, *rel.split('/'))
            if not os.path.exists(fp):
                errors.append('SUMMARY 登记但磁盘缺失: %s' % rel)
                continue
            raw = open(fp, 'rb').read()
            fm, body = S.split_frontmatter(raw.decode('utf-8'))
            order = fm.get('order', 0)
            try:
                order = int(order)
            except (TypeError, ValueError):
                order = 0
            doc = {
                'id': rel,
                'path': rel,
                'url': clean_url(rel),
                'title': fm.get('title') or disp,
                'part': part['name'],
                'order': order,
                'tags': [str(t) for t in (fm.get('tags') or [])],
                'images': extract_images(body, fp, src),
                'checksum': sha256_bytes(normalize_text_for_hash(raw).encode('utf-8')),
            }
            if fm.get('difficulty') in (1, 2, 3):
                doc['difficulty'] = fm['difficulty']
            docs.append(doc)

    # ---- 一致性校验（ARCHITECTURE §3.1 构建时强校验）----
    seen_id, seen_url = set(), set()
    for d in docs:
        if d['id'] in seen_id:
            errors.append('id 重复: %s' % d['id'])
        if d['url'] in seen_url:
            errors.append('url 重复: %s' % d['url'])
        seen_id.add(d['id'])
        seen_url.add(d['url'])

    summary_set = {d['id'] for d in docs}
    skip = {'index.md', 'SUMMARY.md', 'LICENSE-docs.md'}
    for root, _d, files in os.walk(src):
        for f in files:
            if not f.endswith('.md'):
                continue
            rel = os.path.relpath(os.path.join(root, f), src).replace(os.sep, '/')
            if rel in skip or rel.startswith('.vitepress'):
                continue
            if rel not in summary_set:
                errors.append('磁盘有但 SUMMARY 未登记: %s' % rel)

    if errors:
        for e in errors:
            print('[ERROR] ' + e, file=sys.stderr)
        print('manifest 一致性校验失败，共 %d 处' % len(errors), file=sys.stderr)
        sys.exit(1)

    overall = hashlib.sha256(
        '\n'.join('%s\t%s' % (d['id'], d['checksum']) for d in docs).encode('utf-8')
    ).hexdigest()
    manifest = {
        'appId': app,
        'revision': 'sha256-' + overall[:16],   # 由内容 checksum 派生
        'docs': docs,
    }
    routes = sorted(['/'] + [d['url'] for d in docs])
    fingerprint = {
        'appId': app,
        'revision': manifest['revision'],
        'docCount': len(docs),
        'titles': [d['title'] for d in docs],
        'imageTotal': sum(len(d['images']) for d in docs),
        'svgCount': count_svg(src),
        'groundsCount': scan_grounds_count(src),
        'overallChecksum': overall,
    }
    return manifest, routes, fingerprint


def _load_json(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def write_outputs(manifest, routes, fingerprint, app=APP_ID, accept=False):
    """写产物。

    `.generated/<app>-content-manifest.json` 每次都写（离线构建要用）；
    但 **快照是门禁基线，不能自动覆盖**：新增/改写内容时，基线必须由人显式确认。

    - 快照不存在 → 首次生成，直接写（新分册引导）。
    - 快照一致   → 不写（保持工作区干净）。
    - 快照不一致 → 默认拒绝写入并返回 False，提示加 --accept；
                  加 --accept 才更新基线（等价于"我确认这次内容变更是有意的"）。
    """
    os.makedirs(GEN_DIR, exist_ok=True)
    os.makedirs(TESTS_DIR, exist_ok=True)

    def dump(path, obj):
        tmp = path + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
            f.write('\n')
        os.replace(tmp, path)

    dump(os.path.join(GEN_DIR, '%s-content-manifest.json' % app), manifest)

    targets = [
        (os.path.join(TESTS_DIR, '%s.routes.snapshot.json' % app), routes),
        (os.path.join(TESTS_DIR, '%s.manifest.snapshot.json' % app), fingerprint),
    ]
    changed = []
    for path, obj in targets:
        old = _load_json(path)
        if old == obj:
            continue
        changed.append(path)
        if old is None or accept:
            dump(path, obj)
            continue
        # 有差异且未 --accept：保留旧基线，交给调用方决定
        print('[baseline] 快照与当前内容不一致，未覆盖：%s' % os.path.basename(path))
        if path.endswith('manifest.snapshot.json'):
            if old.get('revision') != obj.get('revision'):
                print('           revision  %s -> %s' % (old.get('revision'), obj.get('revision')))
            if old.get('docCount') != obj.get('docCount'):
                print('           docCount  %s -> %s' % (old.get('docCount'), obj.get('docCount')))
        else:
            print('           路由条数  %s -> %s' % (len(old) if isinstance(old, list) else '?',
                                                     len(obj) if isinstance(obj, list) else '?'))
    if changed and not accept:
        blocked = [p for p in changed if _load_json(p) is not None]
        if blocked:
            print('[baseline] 内容已变更但基线未更新。确认这是有意的改动后运行：\n'
                  '           python packages/tooling/src/freeze_manifest.py --app %s --accept' % app)
            return False
    return True


if __name__ == '__main__':
    # --app/--src 由模块顶部的 add_common_args().parse_known_args() 解析；
    # --accept 是本脚本独有的开关，用 parse_known_args 兼容不冲突的方式读取。
    accept = '--accept' in sys.argv
    manifest, routes, fp = build_manifest(APP_ID, DOCS)
    ok = write_outputs(manifest, routes, fp, APP_ID, accept=accept)
    print('manifest 已生成: %d 章 / %d 处图片引用 / svg=%d / grounds=%d / routes=%d / revision=%s'
          % (fp['docCount'], fp['imageTotal'], fp['svgCount'],
             fp['groundsCount'], len(routes), fp['revision']))
    if not ok:
        sys.exit(2)
