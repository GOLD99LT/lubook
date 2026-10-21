#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_vp_sidebar.py — 由 docs/SUMMARY.md + 各章 frontmatter 自动生成 VitePress 侧边栏。

规则（与离线版口径一致，复用 build_single_html 的解析）：
  - SUMMARY.md 中 `## 第N篇 · …` 为一个篇（一级分组）；`* [标题](dir/file.md)` 为该篇下的章。
  - 每章再读 frontmatter 的 `chapter`（章内分组名）与 `order`（组内排序）。
  - 输出三级结构：篇 → 分组(chapter) → 章；若一篇只有一个分组（或无分组），则压平为 篇 → 章。
  - 同时输出 nav（九篇 + 题库 + 附录的下拉入口）。

输出：docs/.vitepress/sidebar.generated.mjs
被 docs/.vitepress/config.mts import。零第三方依赖。
参数化：--src/--out（默认对 handbook 等价）。
"""
import os, re, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths_util import add_common_args, resolve_src, REPO_ROOT
_args, _ = add_common_args().parse_known_args()
DOCS = resolve_src(_args)
OUT = os.path.abspath(_args.out) if _args.out else os.path.join(
    DOCS, '.vitepress', 'sidebar.generated.mjs')


def parse_yaml(text):
    data = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith('#'):
            i += 1
            continue
        m = re.match(r'^([A-Za-z_][\w-]*):\s*(.*)$', line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val == '':
            items = []
            j = i + 1
            while j < len(lines) and (not lines[j].strip() or lines[j].startswith(' ')):
                mm = re.match(r'^\s+-\s*(.*)$', lines[j])
                if mm:
                    items.append(mm.group(1).strip())
                j += 1
            data[key] = items
            i = j
            continue
        if val.startswith('[') and val.endswith(']'):
            data[key] = [x.strip().strip("'\"") for x in val[1:-1].split(',') if x.strip()]
        else:
            v = val.strip("'\"")
            if re.match(r'^-?\d+$', v):
                v = int(v)
            data[key] = v
        i += 1
    return data


def split_frontmatter(text):
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            fm = text[3:end].strip()
            body = text[end + 4:]
            return parse_yaml(fm), body
    return {}, text


def parse_summary():
    parts = []
    cur = None
    for raw in open(os.path.join(DOCS, 'SUMMARY.md'), encoding='utf-8'):
        line = raw.rstrip('\n')
        m = re.match(r'^##\s+(.*)$', line)
        if m:
            cur = {'name': m.group(1).strip(), 'items': []}
            parts.append(cur)
            continue
        m = re.match(r'^\s*[*-]\s+\[([^\]]+)\]\(([^)]+)\)\s*$', line)
        if m and cur is not None:
            cur['items'].append((m.group(1).strip(), m.group(2).strip()))
    return parts


def vp_link(rel):
    """docs/power/buck.md -> /power/buck （VitePress 路由，不带 .md）。"""
    p = rel.replace('\\', '/')
    if p.startswith('./'):
        p = p[2:]
    if p.endswith('.md'):
        p = p[:-3]
    return '/' + p


def build():
    parts = parse_summary()
    sidebar = []
    nav = []
    chapter_count = 0
    for part in parts:
        # 收集该篇下每章的 frontmatter
        groups = {}   # group_name -> list of (order, text, link)
        group_order = []  # 保持分组首次出现顺序
        for disp, rel in part['items']:
            fp = os.path.join(DOCS, rel.replace('/', os.sep))
            if not os.path.exists(fp):
                print('  [warn] SUMMARY 文件缺失，跳过: %s' % rel, file=sys.stderr)
                continue
            meta, _ = split_frontmatter(open(fp, encoding='utf-8').read())
            grp = meta.get('chapter', '') or ''
            order = meta.get('order', 0)
            try:
                order = int(order)
            except Exception:
                order = 0
            title = meta.get('title') or disp
            # 侧边栏显示名：去掉冗长英文括注，保留中文主名；disp 已含编号
            label = disp
            link = vp_link(rel)
            if grp not in groups:
                groups[grp] = []
                group_order.append(grp)
            groups[grp].append((order, label, link, title))
            chapter_count += 1

        # 组内按 order 排序
        for g in groups:
            groups[g].sort(key=lambda x: x[0])

        # 决定是否压平
        nonempty_groups = [g for g in group_order if g]
        if len(nonempty_groups) <= 1:
            # 压平：篇 -> 章
            items = []
            for g in group_order:
                for (_o, label, link, _t) in groups[g]:
                    items.append({'text': label, 'link': link})
            sidebar.append({'text': part['name'], 'collapsed': False, 'items': items})
        else:
            items = []
            for g in group_order:
                gitems = [{'text': label, 'link': link}
                          for (_o, label, link, _t) in groups[g]]
                items.append({'text': g, 'collapsed': True, 'items': gitems})
            sidebar.append({'text': part['name'], 'collapsed': False, 'items': items})

        # nav：取每篇第一章作为入口（下拉显示篇名）
        first_link = None
        for g in group_order:
            if groups[g]:
                first_link = groups[g][0][2]
                break
        nav.append({'text': part['name'], 'link': first_link})

    # 输出 ESM
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    body = (
        '// 本文件由 tools/build_vp_sidebar.py 自动生成，请勿手改。\n'
        '// 数据源：docs/SUMMARY.md + 各章 frontmatter(chapter/order)。\n'
        'export const nav = ' + json.dumps(nav, ensure_ascii=False, indent=2) + '\n\n'
        'const sidebar = ' + json.dumps(sidebar, ensure_ascii=False, indent=2) + '\n\n'
        'export default sidebar\n'
    )
    open(OUT, 'w', encoding='utf-8').write(body)
    print('侧边栏已生成: %s（%d 篇 / %d 章）' % (OUT, len(sidebar), chapter_count))
    sync_brand_public()
    return chapter_count


def sync_brand_public():
    """把品牌资产同步到 <src>/public（VitePress 只拷贝 <srcDir>/public）。
    新布局：品牌资产单一来源在 packages/theme/public；兼容旧 <src>/.vitepress/theme/public。
    """
    import shutil
    dst = os.path.join(DOCS, 'public')
    candidates = [
        os.path.join(REPO_ROOT, 'packages', 'theme', 'public'),
        os.path.join(DOCS, '.vitepress', 'theme', 'public'),
    ]
    src = next((c for c in candidates if os.path.isdir(c)), None)
    if not src:
        return
    os.makedirs(dst, exist_ok=True)
    for fn in os.listdir(src):
        s = os.path.join(src, fn)
        d = os.path.join(dst, fn)
        if os.path.isfile(s):
            shutil.copy2(s, d)
    print('品牌 public 已同步到: %s <- %s' % (dst, src))


if __name__ == '__main__':
    n = build()
    if n == 0:
        print('未收集到任何章节，检查 SUMMARY.md', file=sys.stderr)
        sys.exit(1)
