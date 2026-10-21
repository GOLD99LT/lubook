#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_single_html.py — 把指定 app 的 Markdown 手册构建为单个自包含 HTML。

用法（按 app 参数化，默认 app=hardware）：
    python packages/tooling/src/build_single_html.py --app hardware
    python packages/tooling/src/build_single_html.py --app hardware --published
    python packages/tooling/src/build_single_html.py --app hardware \
        --manifest .generated/hardware-content-manifest.json

零第三方依赖（Python 3.8+）。输出 dist/<app>.html（如 dist/hardware.html）。
若传入 --manifest 且文件存在，则在构建后按其对账（章节数/标题/图片引用数）；
manifest 缺失时维持现状自解析，不重写 Markdown（ARCHITECTURE §6）。
"""
import os, re, sys, json, base64, html as H

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths_util import (REPO_ROOT, DEFAULT_SRC, DEFAULT_VENDOR,
                        DEFAULT_OUT_DIST, add_common_args)

ROOT = REPO_ROOT
DOCS = DEFAULT_SRC
DIST = DEFAULT_OUT_DIST
VENDOR = DEFAULT_VENDOR

WARNINGS = []
def warn(msg):
    WARNINGS.append(msg)
    print('  [warn] ' + msg)

# ============================================================
# 离线分册品牌（按 app 区分；中文书名保留，新增「路书」系列角标）
# storePrefix：离线运行时 localStorage 键前缀；hardware 沿用旧 'hh' 以保留既有离线笔记
# ============================================================
OFFLINE_BRANDS = {
    'hardware': {
        'book': '硬件工程师手册',
        'en': 'HARDWARE HANDBOOK',
        'htmlTitle': '硬件工程师手册 · 路书',
        'storePrefix': 'hh',
        'series': '路书 · Lubook 系列',
    },
}

def brand_for(app):
    if app in OFFLINE_BRANDS:
        return dict(OFFLINE_BRANDS[app])
    return {
        'book': app,
        'en': app.upper(),
        'htmlTitle': '%s · 路书' % app,
        'storePrefix': app,
        'series': '路书 · Lubook 系列',
    }

# ============================================================
# YAML 子集解析（frontmatter）
# ============================================================
def parse_yaml(text):
    data = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith('#'):
            i += 1; continue
        m = re.match(r'^([A-Za-z_][\w-]*):\s*(.*)$', line)
        if not m:
            i += 1; continue
        key, val = m.group(1), m.group(2).strip()
        if val == '':
            # 块数组：后续缩进的 - item
            items = []
            j = i + 1
            while j < len(lines) and (not lines[j].strip() or lines[j].startswith(' ')):
                mm = re.match(r'^\s+-\s*(.*)$', lines[j])
                if mm: items.append(mm.group(1).strip())
                j += 1
            data[key] = items
            i = j; continue
        if val.startswith('[') and val.endswith(']'):
            data[key] = [x.strip().strip("'\"") for x in val[1:-1].split(',') if x.strip()]
        else:
            v = val.strip("'\"")
            if re.match(r'^-?\d+$', v): v = int(v)
            data[key] = v
        i += 1
    return data

def split_frontmatter(text):
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            fm = text[3:end].strip()
            body = text[end+4:]
            if body.startswith('\n'): body = body[1:]
            return parse_yaml(fm), body
    return {}, text

# ============================================================
# SUMMARY 解析
# ============================================================
def parse_summary():
    path = os.path.join(DOCS, 'SUMMARY.md')
    if not os.path.exists(path):
        return []
    parts = []
    current = None
    for raw in open(path, encoding='utf-8'):
        line = raw.rstrip('\n')
        m = re.match(r'^##\s+(.*)$', line)
        if m:
            current = {'name': m.group(1).strip(), 'items': []}
            parts.append(current)
            continue
        m = re.match(r'^\s*[*-]\s+\[([^\]]+)\]\(([^)]+)\)\s*$', line)
        if m and current is not None:
            current['items'].append((m.group(1).strip(), m.group(2).strip()))
    return parts

# ============================================================
# 资源内联（SVG 直接内联；其他图片转 base64）
# ============================================================
def inline_asset(src, base_dir):
    p = os.path.normpath(os.path.join(base_dir, src.replace('/', os.sep)))
    if not os.path.exists(p):
        warn('图片不存在: %s' % src)
        return '<span class="img-missing">[图片缺失: %s]</span>' % H.escape(src)
    ext = os.path.splitext(p)[1].lower()
    raw = open(p, 'rb').read()
    if ext == '.svg':
        content = raw.decode('utf-8', errors='replace')
        # 去掉 XML 声明，保留 svg 本体
        content = re.sub(r'<\?xml[^>]*\?>', '', content).strip()
        return content
    mime = {'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.gif':'image/gif',
            '.webp':'image/webp'}.get(ext, 'application/octet-stream')
    b64 = base64.b64encode(raw).decode('ascii')
    return '<img class="inline-img" alt="" src="data:%s;base64,%s">' % (mime, b64)

def attr_escape(s):
    """转义放进 HTML 属性的文本（反斜杠在 HTML 中保持原样，不做 JSON 转义）。"""
    return (s.replace('&', '&amp;').replace('"', '&quot;')
            .replace('<', '&lt;').replace('>', '&gt;'))

# ============================================================
# 行内 Markdown
# ============================================================
def inline(text):
    s = H.escape(text)
    # 行内代码
    s = re.sub(r'`([^`]+)`', lambda m: '<code>%s</code>' % m.group(1), s)
    # 行内公式 $...$（排除 $$）
    s = re.sub(r'(?<!\$)\$([^$\n]+?)\$(?!\$)',
               lambda m: '<span class="tex-inline" data-t="%s"></span>' % attr_escape(m.group(1)), s)
    # 图片（行内）
    def _img(m):
        return '<span class="inline-fig">' + inline_asset(m.group(2), _INLINE_BASE[0]) + '</span>'
    s = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', _img, s)
    # 链接
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
               lambda m: '<a href="%s" target="_blank" rel="noopener">%s</a>' % (m.group(2), m.group(1)), s)
    # 粗体 / 斜体
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)
    return s

_INLINE_BASE = [DOCS]

# ============================================================
# 读取所有卡片
# ============================================================
def collect_cards(only_published=False):
    cards = []
    for part in parse_summary():
        for disp, rel in part['items']:
            fp = os.path.join(DOCS, rel.replace('/', os.sep))
            if not os.path.exists(fp):
                warn('SUMMARY 中的文件不存在，已跳过: %s' % rel)
                continue
            meta, body = split_frontmatter(open(fp, encoding='utf-8').read())
            if only_published and str(meta.get('status', 'draft')) != 'published':
                continue
            cid = meta.get('id') or os.path.splitext(os.path.basename(fp))[0]
            cards.append({
                'id': cid, 'title': meta.get('title', cid),
                'part': part['name'], 'chapter': meta.get('chapter', ''),
                'tags': meta.get('tags', []), 'difficulty': int(meta.get('difficulty', 1)),
                'sources': meta.get('sources', []), 'rel': rel,
                'body': body, 'base_dir': os.path.dirname(fp)
            })
    return cards

# ============================================================
# 块级 Markdown 解析
# ============================================================
CT_ICONS = {
    'motivation': '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4" fill="currentColor"/></svg>',
    'analogy': '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.5.4.8 1 .9 1.7h5.4c.1-.7.4-1.3.9-1.7A6 6 0 0 0 12 3Z"/></svg>',
    'example': '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L4 17v3h3l5.3-5.3a4 4 0 0 0 5.4-5.4l-2.3 2.3-2.4-2.4 2.7-2.2Z"/></svg>',
    'pitfall': '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3 2.5 20h19L12 3Z"/><line x1="12" y1="10" x2="12" y2="14"/><circle cx="12" cy="17.2" r=".6" fill="currentColor"/></svg>',
    'advanced': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.6 2.2c-.7.4-1.1 1-1.1 1.8"/><line x1="12" y1="17" x2="12" y2="17.3"/></svg>'
}
DEFAULT_TITLES = {'motivation': '设计动机 · 为什么需要它', 'analogy': '直觉类比',
                  'example': '设计示例', 'pitfall': '常见坑', 'advanced': '进阶内容（可跳过）'}

def is_block_start(l):
    s = l.strip()
    patterns = [r'^```', r'^:::', r'^#{1,6}\s', r'^>', r'^[-*]\s', r'^\d+\.\s',
                r'^<\w+', r'^\$\$', r'^!\[', r'^\|']
    return any(re.match(p, s) for p in patterns)

def render_code(lang, buf):
    code = '\n'.join(buf)
    if lang == 'echarts':
        try:
            json.loads(code)
        except Exception as e:
            warn('echarts JSON 解析失败: %s' % e)
        return ('<div class="block fig"><pre class="echarts-src" hidden>%s</pre>'
                '<div class="chart-box"></div></div>') % H.escape(code)
    if lang == 'svg':
        return '<div class="block fig">%s</div>' % code.strip()
    cls = ' class="lang-%s"' % lang if lang else ''
    return '<pre class="codeblock"><code%s>%s</code></pre>' % (cls, H.escape(code))

def pitfall_post(inner):
    def repl(m):
        c = m.group(1)
        mt = re.match(r'^<strong>(.*?)</strong>[：:]\s*(.*)$', c, re.S)
        if mt:
            return ('<div class="pit-item"><span class="pit-t">%s</span>'
                    '<span class="pit-d">%s</span></div>') % (mt.group(1), mt.group(2))
        return '<div class="pit-item"><span class="pit-d">%s</span></div>' % c
    inner = re.sub(r'<li>(.*?)</li>', repl, inner, flags=re.S)
    return re.sub(r'</?(ul|ol)[^>]*>', '', inner)

def render_container(ctype, title, inner):
    title = title or DEFAULT_TITLES.get(ctype, '')
    icon = CT_ICONS.get(ctype, '')
    if ctype == 'advanced':
        return ('<details class="advanced"><summary>%s<span>%s</span></summary>'
                '<div class="adv-body">%s</div></details>') % (icon, inline(title), inner)
    if ctype == 'pitfall':
        inner = pitfall_post(inner)
    return ('<div class="block %s"><div class="b-title">%s%s</div>%s</div>'
            ) % (ctype, icon, inline(title), inner)

def parse_table_row(s):
    return [c.strip() for c in s.strip().strip('|').split('|')]

def render_table(head, rows):
    ncol = max(len(head), 1)
    cols = ''.join('<col style="width:%d%%">' % int(100 / ncol) for _ in range(ncol))
    return ('<div class="block tbl"><div class="tbl-wrap"><table><colgroup>%s</colgroup>'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div></div>') % (
        cols,
        ''.join('<th>%s</th>' % inline(c) for c in head),
        ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % inline(c) for c in r) for r in rows))

def render_list(items, ordered):
    tag = 'ol' if ordered else 'ul'
    out = ['<%s>' % tag]
    i = 0
    while i < len(items):
        indent, content = items[i]
        sub = []
        k = i + 1
        while k < len(items) and items[k][0] > 0:
            sub.append(items[k]); k += 1
        if sub:
            sub_html = render_list([(0, c) for _, c in sub], ordered)
            out.append('<li>%s %s</li>' % (inline(content), sub_html))
            i = k
        else:
            out.append('<li>%s</li>' % inline(content)); i += 1
    out.append('</%s>' % tag)
    return ''.join(out)

def render_details(buf):
    text = '\n'.join(buf)
    m = re.search(r'<summary>(.*?)</summary>', text, re.S)
    q = m.group(1).strip() if m else ''
    a = re.sub(r'</?details[^>]*>', '', text)
    a = re.sub(r'<summary>.*?</summary>', '', a, flags=re.S).strip()
    a_html = parse_blocks(a.splitlines(), _INLINE_BASE[0])
    return ('<details class="quiz-item"><summary class="quiz-q">'
            '<span class="qmark">Q</span><span>%s</span><span class="qarrow">▾</span></summary>'
            '<div class="quiz-a">%s</div></details>') % (inline(q), a_html)

def render_block_formula(tex):
    return '<div class="tex-block" data-t="%s"></div>' % attr_escape(tex.strip())

def parse_blocks(lines, base_dir):
    out = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1; continue
        # 围栏代码
        m = re.match(r'^```(\w*)\s*$', s)
        if m:
            lang = m.group(1)
            j = i + 1; buf = []
            while j < n and not re.match(r'^```\s*$', lines[j].strip()):
                buf.append(lines[j]); j += 1
            out.append(render_code(lang, buf))
            i = j + 1; continue
        # 容器
        m = re.match(r'^:::\s*(\w+)\s*(.*)$', s)
        if m:
            ctype, ctitle = m.group(1), m.group(2).strip()
            j = i + 1; buf = []
            while j < n and not re.match(r'^:::\s*$', lines[j].strip()):
                buf.append(lines[j]); j += 1
            out.append(render_container(ctype, ctitle, parse_blocks(buf, base_dir)))
            i = j + 1; continue
        # 块公式
        if s.startswith('$$'):
            if s.endswith('$$') and len(s) > 2:
                out.append(render_block_formula(s[2:-2])); i += 1; continue
            j = i + 1; buf = []
            if s != '$$': buf.append(s[2:])
            while j < n and not lines[j].strip().endswith('$$'):
                buf.append(lines[j]); j += 1
            if j < n and lines[j].strip() != '$$':
                buf.append(lines[j].strip()[:-2])
            out.append(render_block_formula('\n'.join(buf)))
            i = j + 1; continue
        # 标题
        m = re.match(r'^(#{1,6})\s+(.*)$', s)
        if m:
            lvl = len(m.group(1))
            out.append('<h%d>%s</h%d>' % (lvl, inline(m.group(2)), lvl)); i += 1; continue
        if re.match(r'^(-{3,}|\*{3,})$', s):
            out.append('<hr>'); i += 1; continue
        # 表格
        if s.startswith('|') and i + 1 < n and re.match(r'^\|[\s:|-]+\|?\s*$', lines[i + 1].strip()):
            head = parse_table_row(s)
            j = i + 2; rows = []
            while j < n and lines[j].strip().startswith('|'):
                rows.append(parse_table_row(lines[j].strip())); j += 1
            out.append(render_table(head, rows))
            i = j; continue
        # 引用
        if s.startswith('>'):
            j = i; buf = []
            while j < n and lines[j].strip().startswith('>'):
                buf.append(re.sub(r'^\s*>\s?', '', lines[j])); j += 1
            out.append('<blockquote>%s</blockquote>' % inline(' '.join(buf)))
            i = j; continue
        # 列表
        if re.match(r'^[-*]\s+', s) or re.match(r'^\d+\.\s+', s):
            j = i; items = []; ordered = None
            while j < n:
                l = lines[j]
                if not l.strip():
                    if j + 1 < n and re.match(r'^\s*([-*]|\d+\.)\s', lines[j + 1]):
                        j += 1; continue
                    break
                m1 = re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)$', l)
                if not m1: break
                if ordered is None: ordered = bool(re.match(r'\d+\.', m1.group(2)))
                items.append((len(m1.group(1)), m1.group(3)))
                j += 1
            out.append(render_list(items, ordered))
            i = j; continue
        # HTML 块
        m = re.match(r'^<(\w+)', s)
        if m:
            if m.group(1) == 'details':
                j = i; buf = []
                while j < n and '</details>' not in lines[j]:
                    buf.append(lines[j]); j += 1
                if j < n: buf.append(lines[j])
                out.append(render_details(buf))
                i = j + 1; continue
            out.append(s); i += 1; continue
        # 单独图片
        m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', s)
        if m:
            fig = '<div class="block fig">' + inline_asset(m.group(2), base_dir)
            if m.group(1): fig += '<div class="fig-cap">%s</div>' % inline(m.group(1))
            out.append(fig + '</div>'); i += 1; continue
        # 段落
        j = i; buf = []
        while j < n and lines[j].strip() and not is_block_start(lines[j]):
            buf.append(lines[j].strip()); j += 1
        out.append('<p>%s</p>' % inline(' '.join(buf)))
        i = j
    return '\n'.join(out)

def md_to_html(card):
    _INLINE_BASE[0] = card['base_dir']
    return parse_blocks(card['body'].splitlines(), card['base_dir'])

# ============================================================
# 页面样式
# ============================================================
CSS_STR = r"""
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{font-family:'Noto Sans SC','PingFang SC','Microsoft YaHei','Hiragino Sans GB',-apple-system,sans-serif;background:#f4f3ee;color:#222a32;font-size:16px;line-height:1.75}
button{font-family:inherit;cursor:pointer}
::selection{background:#e8c39a}
.layout{display:flex;min-height:100vh}
.sidebar{width:300px;flex-shrink:0;background:#101821;color:#aebac8;display:flex;flex-direction:column;position:fixed;top:0;bottom:0;left:0;z-index:50}
.main{flex:1;margin-left:300px;min-width:0;display:flex;flex-direction:column}
.sb-brand{padding:20px 20px 14px;border-bottom:1px solid #1d2a37}
.sb-brand .logo{display:flex;align-items:center;gap:10px;font-weight:900;font-size:18px;color:#f0f4f8}
.sb-brand .sub{font-size:12px;color:#6b7a8a;margin-top:5px;padding-left:34px;letter-spacing:1px}
.sb-brand .series{margin-top:9px;font-size:11px;color:#d99a4e;letter-spacing:.5px;padding-left:2px}
.sb-search{padding:14px 16px 10px}
.sb-search input{width:100%;background:#15202b;border:1px solid #243242;border-radius:8px;color:#dde5ec;padding:9px 12px;font-size:13.5px;outline:none;font-family:inherit}
.sb-search input:focus{border-color:#b5642e}
.sb-search input::placeholder{color:#5d6c7c}
.sb-tree{flex:1;min-height:0;overflow-y:auto;padding:4px 10px 20px}
.sb-tree::-webkit-scrollbar{width:8px}
.sb-tree::-webkit-scrollbar-thumb{background:#263543;border-radius:4px}
.tree-part{margin-top:10px}
.tree-part-name{font-size:11.5px;font-weight:700;color:#7e8d9d;letter-spacing:1.2px;padding:8px 12px 5px}
.tree-chapter{font-size:12px;color:#8fa0b0;padding:4px 12px 2px 20px}
.tree-item{display:flex;align-items:center;gap:8px;padding:7px 12px 7px 16px;border-radius:7px;cursor:pointer;font-size:14px;color:#aebac8;line-height:1.35}
.tree-item:hover{background:#182532;color:#e6ecf2}
.tree-item.active{background:#1d2c3b;color:#fff;font-weight:700;box-shadow:inset 3px 0 0 #b5642e}
.tree-item .tlearned{margin-left:auto;color:#3a9e5e;font-size:12px}
.tree-item .tstar{color:#d9a441;font-size:11px;margin-right:2px}
.sb-foot{flex-shrink:0;padding:12px 18px;border-top:1px solid #1d2a37;font-size:12px;color:#6b7a8a}
.progress-bar{height:5px;background:#1d2a37;border-radius:3px;overflow:hidden;margin-bottom:8px}
.progress-bar i{display:block;height:100%;background:linear-gradient(90deg,#b5642e,#d99a4e);width:0;transition:width .4s}
.sb-foot .ptext{display:flex;justify-content:space-between;align-items:center}
.sb-foot button{background:none;border:none;color:#8fa0b0;font-size:11.5px}
.sb-foot button:hover{color:#d99a4e}
.depth-toggle{display:flex;background:#15202b;border:1px solid #243242;border-radius:7px;overflow:hidden;margin-bottom:8px}
.depth-toggle button{flex:1;background:none;border:none;color:#7e8d9d;font-size:12px;padding:6px 0}
.depth-toggle button.on{background:#1d2c3b;color:#d99a4e;font-weight:700}
.topbar{position:sticky;top:0;z-index:30;background:rgba(244,243,238,.92);backdrop-filter:blur(8px);border-bottom:1px solid #e3e0d7;display:flex;align-items:center;gap:12px;padding:10px 28px}
.topbar .crumb{font-size:13px;color:#5c6772;flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.topbar .crumb b{color:#222a32;font-weight:700}
.icon-btn{background:#fff;border:1px solid #e3e0d7;border-radius:8px;width:36px;height:36px;display:flex;align-items:center;justify-content:center;color:#5c6772}
.icon-btn:hover{border-color:#b5642e;color:#b5642e}
.icon-btn.on{background:#fdf3e6;border-color:#b5642e;color:#b5642e}
#menuBtn{display:none}
.reader{flex:1;padding:36px 40px 60px}
.card{display:none}.card.show{display:block}
.article{max-width:860px;width:100%;margin:0 auto}
.card-head{margin-bottom:26px}
.card-tags{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:14px}
.tag{font-size:12px;background:#e9e6dc;color:#6b6452;padding:3px 11px;border-radius:20px;font-family:Consolas,'JetBrains Mono','Courier New',monospace}
.diff-badge{font-size:11px;padding:3px 10px;border-radius:20px;font-family:Consolas,'JetBrains Mono','Courier New',monospace}
.diff-1{background:#e7f2ea;color:#3a7e4e}.diff-2{background:#fdf0df;color:#a35f22}.diff-3{background:#f3e9f7;color:#6d44a0}
.card-title{font-size:31px;font-weight:900;line-height:1.3}
.card-meta{font-size:13px;color:#5c6772;margin-top:10px;font-family:Consolas,'JetBrains Mono','Courier New',monospace}
.article h2{font-size:22px;font-weight:800;margin:32px 0 13px;padding-bottom:8px;border-bottom:1px solid #e3e0d7}
.article h3{font-size:17.5px;font-weight:700;margin:24px 0 10px}
.article p{margin:11px 0}
.article hr{border:none;border-top:1px solid #e3e0d7;margin:24px 0}
.article blockquote{border-left:4px solid #c2a45d;background:#faf6e8;padding:12px 18px;border-radius:0 9px 9px 0;margin:16px 0;font-size:14.5px;color:#5d5640}
.article code{background:#efece3;padding:2px 6px;border-radius:5px;font-family:Consolas,'JetBrains Mono','Courier New',monospace;font-size:13px;color:#8a4b1f}
.codeblock{background:#15202b;color:#d8e2ec;padding:16px 18px;border-radius:10px;overflow-x:auto;margin:16px 0}
.codeblock code{background:none;color:inherit;padding:0;font-size:13.5px;line-height:1.7}
.block{margin:22px 0;border-radius:12px;padding:18px 22px;font-size:15.5px}
.block .b-title{display:flex;align-items:center;gap:9px;font-weight:700;font-size:15px;margin-bottom:10px}
.block.motivation{background:#fdf3e6;border:1px solid #eccfa6;border-left:4px solid #b5642e}
.block.motivation .b-title{color:#b5642e}
.block.analogy{background:#eaf2fb;border:1px solid #c6dcf1;border-left:4px solid #5b8fc4}
.block.analogy .b-title{color:#2f6aa3}
.block.example{background:#ecf5ee;border:1px solid #c5e2cc;border-left:4px solid #4f9e63}
.block.example .b-title{color:#2f7a44}
.block.example ul,.block.example ol{padding-left:20px}.block.example li{margin:7px 0}
.block.pitfall{background:#fbece9;border:1px solid #f1cdc5;border-left:4px solid #cc5a47}
.block.pitfall .b-title{color:#b23f2d}
.pit-item{margin:11px 0;padding-left:27px;position:relative}
.pit-item:before{content:'!';position:absolute;left:0;top:2px;width:16px;height:16px;border-radius:50%;background:#cc5a47;color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center}
.pit-item .pit-t{font-weight:700;color:#a23a29}
.pit-item .pit-d{display:block;font-size:14px;color:#6f5a56;margin-top:2px}
.block.fig{background:#fff;border:1px solid #d9d5c9;padding:18px}
.block.fig .fig-cap{font-size:13px;color:#5c6772;margin-top:10px;line-height:1.6;border-top:1px dashed #e3e0d7;padding-top:10px}
.block.fig svg{width:100%;height:auto;display:block;max-height:460px}
.chart-box{width:100%;height:340px}
.block.tbl{background:#fff;border:1px solid #d9d5c9;padding:0;overflow:hidden}
.block.tbl .tbl-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;table-layout:fixed;font-size:14px}
th,td{padding:11px 16px;text-align:left;vertical-align:top;border-bottom:1px solid #e3e0d7;line-height:1.65;word-break:break-word}
th{background:#f3f1ea;font-weight:700;font-size:13px;color:#4a463c}
tr:last-child td{border-bottom:none}
.article ul,.article ol{padding-left:23px;margin:11px 0}
.article li{margin:6px 0}
.article li ul,.article li ol{margin:4px 0}
.tex-block{background:#f1edf9;border:1px solid #d9cff2;border-left:4px solid #8065c2;border-radius:10px;padding:15px 20px;margin:18px 0;overflow-x:auto}
.tex-block .katex-display{margin:0}
.advanced{background:#f1edf9;border:1px solid #d9cff2;border-radius:10px;margin:18px 0;overflow:hidden}
.advanced summary{padding:12px 18px;font-weight:700;font-size:14px;color:#5d44a8;cursor:pointer;list-style:none;display:flex;gap:9px;align-items:center}
.advanced summary::-webkit-details-marker{display:none}
.adv-body{padding:4px 20px 16px;font-size:14.5px}
.quiz-item{background:#faf6e8;border:1px solid #e6d9ad;border-radius:10px;margin:14px 0}
.quiz-q{padding:14px 18px;font-weight:700;font-size:14.5px;display:flex;gap:10px;cursor:pointer;list-style:none;align-items:flex-start}
.quiz-q::-webkit-details-marker{display:none}
.quiz-q .qmark{flex-shrink:0;width:22px;height:22px;border-radius:50%;background:#c2a45d;color:#fff;font-size:12px;display:flex;align-items:center;justify-content:center;font-weight:700}
.quiz-q .qarrow{margin-left:auto;color:#b39a4f;transition:transform .25s}
details[open] .qarrow{transform:rotate(180deg)}
.quiz-a{padding:0 18px 15px 50px;font-size:14px;color:#4d5247;line-height:1.75}
.quiz-a:before{content:'答案：';font-weight:700;color:#8a7128}
.src-list{margin-top:26px;padding-top:14px;border-top:1px dashed #d9d5c9;font-size:12.5px;color:#8a8272}
.src-list b{color:#6b6452}.src-list a{color:#8a4b1f;word-break:break-all}
.notes{margin-top:30px;background:#fff;border:1px solid #e3e0d7;border-radius:12px;padding:18px 22px}
.notes .n-title{font-weight:700;font-size:14.5px;display:flex;gap:8px;margin-bottom:10px;align-items:center}
.notes textarea{width:100%;min-height:96px;border:1px solid #e3e0d7;border-radius:8px;padding:12px;font-family:inherit;font-size:14px;resize:vertical;outline:none;line-height:1.7}
.notes textarea:focus{border-color:#b5642e}
.notes .n-status{font-size:12px;color:#3a9e5e;margin-top:6px;text-align:right;min-height:16px}
.card-actions{display:flex;gap:10px;margin:26px 0 4px;flex-wrap:wrap}
.act-btn{display:flex;align-items:center;gap:7px;padding:9px 18px;border-radius:9px;border:1px solid #e3e0d7;background:#fff;font-size:14px;color:#5c6772}
.act-btn:hover{border-color:#b5642e;color:#b5642e}
.act-btn.on.learned{background:#ecf5ee;border-color:#4f9e63;color:#3a9e5e}
.act-btn.on.starred{background:#fdf3e6;border-color:#b5642e;color:#b5642e}
.pager{display:flex;justify-content:space-between;gap:14px;margin-top:40px;padding-top:22px;border-top:1px solid #e3e0d7}
.pager a{flex:1;background:#fff;border:1px solid #e3e0d7;border-radius:10px;padding:14px 18px;text-align:left;font-size:14px;color:#5c6772;text-decoration:none}
.pager a:hover{border-color:#b5642e;color:#b5642e}
.pager a.disabled{opacity:.4;pointer-events:none}
.pager .pdir{display:block;font-size:11.5px;color:#b5642e;margin-bottom:3px;font-family:Consolas,'JetBrains Mono','Courier New',monospace}
.pager .pnext{text-align:right}
.toast{position:fixed;bottom:30px;left:50%;transform:translateX(-50%) translateY(20px);background:#222c36;color:#fff;padding:11px 24px;border-radius:10px;font-size:14px;opacity:0;pointer-events:none;transition:all .3s;z-index:100}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.search-panel{display:none;padding:30px 40px}
.search-panel.show{display:block}
.search-panel h2{font-size:20px;margin-bottom:18px}
.s-result{background:#fff;border:1px solid #e3e0d7;border-radius:10px;padding:15px 20px;margin-bottom:11px;cursor:pointer}
.s-result:hover{border-color:#b5642e}
.s-result .sr-title{font-weight:700;font-size:15.5px}
.s-result .sr-meta{font-size:12.5px;color:#5c6772;margin-top:4px}
.s-result mark{background:#f5d9b0;padding:0 3px;border-radius:3px}
.s-empty{color:#5c6772;font-size:14px}
.inline-img{max-width:100%}
.img-missing{color:#cc5a47;font-size:13px}
body.depth-basic .card.diff-3{display:none !important}
body.depth-basic .tree-item.for-diff-3{display:none}
@media (max-width:900px){
  .sidebar{transform:translateX(-100%);transition:transform .3s;box-shadow:0 0 40px rgba(0,0,0,.3)}
  .sidebar.open{transform:translateX(0)}
  .main{margin-left:0}#menuBtn{display:flex}
  .reader{padding:24px 18px 50px}.search-panel{padding:24px 18px}
  .card-title{font-size:24px}.topbar{padding:10px 16px}
}
"""

# ============================================================
# HTML 模板
# ============================================================
PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__HTML_TITLE__</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%23101821'/%3E%3Cpolygon points='10,7 10,25 24,16' fill='none' stroke='%23c98a3e' stroke-width='2.4'/%3E%3C/svg%3E">
__VENDOR__
<style>__CSS__</style>
</head>
<body>
<div class="layout">
  <aside class="sidebar" id="sidebar">
    <div class="sb-brand">
      <div class="logo">
        <svg width="24" height="24" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#1d2c3b"/><polygon points="10,7 10,25 24,16" fill="none" stroke="#d99a4e" stroke-width="2.4"/></svg>
        __BOOK_TITLE__
      </div>
      <div class="sub">__BOOK_EN__</div>
      <div class="series">__SERIES__</div>
    </div>
    <div class="sb-search"><input type="text" id="searchInput" placeholder="搜索知识点，如 虚短 / Buck…"></div>
    <nav class="sb-tree" id="tree">__TREE__</nav>
    <div class="sb-foot">
      <div class="depth-toggle"><button id="dtAll" class="on">全部深度</button><button id="dtBasic">仅入门</button></div>
      <div class="progress-bar"><i id="progBar"></i></div>
      <div class="ptext"><span id="progText"></span><button id="exportBtn">导出笔记备份</button></div>
    </div>
  </aside>
  <div class="main">
    <header class="topbar">
      <button class="icon-btn" id="menuBtn"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
      <div class="crumb" id="crumb"></div>
      <button class="icon-btn" id="starBtn" title="收藏"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12,2 15,9 22,9.5 16.8,14.2 18.5,21.5 12,17.6 5.5,21.5 7.2,14.2 2,9.5 9,9"/></svg></button>
      <button class="icon-btn" id="learnedBtn" title="标记已学"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><polyline points="4,12.5 9.5,18 20,6.5"/></svg></button>
    </header>
    <div class="reader" id="reader">__CARDS__</div>
    <div class="search-panel" id="searchPanel"></div>
  </div>
</div>
<div class="toast" id="toast"></div>
<script>window.BRAND=__BRAND__;</script>
<script>window.SEARCH_DATA=__SEARCH__;</script>
<script>__RUNTIME__</script>
</body>
</html>
"""

# ============================================================
# 组装
# ============================================================
def group_parts(cards):
    groups = []
    for c in cards:
        if not groups or groups[-1]['name'] != c['part']:
            groups.append({'name': c['part'], 'cards': []})
        groups[-1]['cards'].append(c)
    return groups

def build_tree(cards):
    h = []
    for g in group_parts(cards):
        h.append('<div class="tree-part"><div class="tree-part-name">%s</div>' % H.escape(g['name']))
        last = None
        for c in g['cards']:
            if c['chapter'] and c['chapter'] != last:
                h.append('<div class="tree-chapter">%s</div>' % H.escape(c['chapter']))
            last = c['chapter']
            h.append('<div class="tree-item for-diff-%d" data-id="%s"><span class="ticon">·</span><span>%s</span></div>'
                     % (c['difficulty'], c['id'], H.escape(c['title'])))
        h.append('</div>')
    return ''.join(h)

def pager_link(x, is_next):
    if not x:
        label = '已经是最后一节' if is_next else '已经是第一节'
        pd = '下一节 →' if is_next else '← 上一节'
        return '<a class="disabled"><span class="pdir">%s</span>%s</a>' % (pd, label)
    pd = '下一节 →' if is_next else '← 上一节'
    cls = 'pnext' if is_next else ''
    return '<a class="%s" href="#%s"><span class="pdir">%s</span>%s</a>' % (
        cls, x['id'], pd, H.escape(x['title']))

def build_card(c, idx, total, cards):
    prev = cards[idx - 1] if idx > 0 else None
    nxt = cards[idx + 1] if idx < total - 1 else None
    tags = ''.join('<span class="tag">#%s</span>' % H.escape(t) for t in c['tags'])
    diff = '<span class="diff-badge diff-%d">难度 %d</span>' % (c['difficulty'], c['difficulty'])
    src = ''
    if c['sources']:
        items = []
        for s in c['sources']:
            s = str(s)
            if s.startswith('http'):
                items.append('<a href="%s" target="_blank">%s</a>' % (H.escape(s), H.escape(s)))
            else:
                items.append(H.escape(s))
        src = '<div class="src-list"><b>参考来源：</b><br>' + '<br>'.join(items) + '</div>'
    pager = '<nav class="pager">%s %s</nav>' % (pager_link(prev, False), pager_link(nxt, True))
    return (
        '<section class="card diff-%d" id="card-%s" data-id="%s">'
        '<article class="article"><div class="card-head">'
        '<div class="card-tags">%s %s</div>'
        '<h1 class="card-title">%s</h1>'
        '<div class="card-meta">%s · 第 %d 节</div></div>'
        '%s%s'
        '<div class="card-actions">'
        '<button class="act-btn learned" data-role="learned">标记为已学</button>'
        '<button class="act-btn starred" data-role="starred">收藏</button></div>'
        '<div class="notes"><div class="n-title">我的笔记（自动保存在本机浏览器）</div>'
        '<textarea data-role="note" placeholder="记录理解、疑问、实验现象…"></textarea>'
        '<div class="n-status" data-role="nstatus"></div></div>'
        '%s</article></section>'
    ) % (c['difficulty'], c['id'], c['id'], tags, diff, H.escape(c['title']),
         H.escape(c['part']), idx + 1, c['html'], src, pager)

def plain_text(body):
    t = re.sub(r'```.*?```', '', body, flags=re.S)
    t = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', t)
    t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)
    t = re.sub(r'\$\$?[^$]*\$\$?', '', t)
    t = re.sub(r'[#*`>:]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

RUNTIME_JS = r"""
const CARDS = window.SEARCH_DATA || [];
const BRAND = window.BRAND || {app:'hardware', storePrefix:'hh'};
const STORE = {
  learned: JSON.parse(localStorage.getItem(BRAND.storePrefix + '-learned') || '{}'),
  starred: JSON.parse(localStorage.getItem(BRAND.storePrefix + '-starred') || '{}'),
  notes: JSON.parse(localStorage.getItem(BRAND.storePrefix + '-notes') || '{}')
};
let charts = [];
const $ = s => document.querySelector(s);
function save(k){ localStorage.setItem(BRAND.storePrefix + '-' + k, JSON.stringify(STORE[k])); }
function cardEl(id){ return document.getElementById('card-' + id); }
function currentId(){ const s = $('.card.show'); return s ? s.dataset.id : null; }

/* ---- KaTeX ---- */
function renderTex(){
  document.querySelectorAll('.tex-inline').forEach(el =>
    katex.render(el.dataset.t, el, {throwOnError:false}));
  document.querySelectorAll('.tex-block').forEach(el =>
    katex.render(el.dataset.t, el, {displayMode:true, throwOnError:false}));
}

/* ---- ECharts ---- */
function initCharts(){
  charts.forEach(c => c.dispose()); charts = [];
  document.querySelectorAll('.echarts-src').forEach(pre => {
    const fig = pre.closest('.fig'); const box = fig.querySelector('.chart-box');
    try { const c = echarts.init(box); c.setOption(JSON.parse(pre.textContent)); charts.push(c); }
    catch(e){ console.error('echarts error', e); }
  });
}

/* ---- 状态标记 ---- */
function refreshMarks(){
  CARDS.forEach(c => {
    const sec = cardEl(c.id); if(!sec) return;
    const L = !!STORE.learned[c.id], S = !!STORE.starred[c.id];
    const lb = sec.querySelector('[data-role=learned]');
    lb.classList.toggle('on', L); lb.textContent = L ? '已学' : '标记为已学';
    const sb = sec.querySelector('[data-role=starred]');
    sb.classList.toggle('on', S); sb.textContent = S ? '已收藏' : '收藏';
    const ti = document.querySelector('.tree-item[data-id="' + c.id + '"]');
    if(ti) ti.innerHTML = '<span class="ticon">' + (S ? '<span class="tstar">★</span>' : '·') +
      '</span><span>' + c.title + '</span>' + (L ? '<span class="tlearned">✓</span>' : '');
  });
  const n = CARDS.filter(c => STORE.learned[c.id]).length;
  $('#progText').textContent = '已学 ' + n + ' / ' + CARDS.length;
  $('#progBar').style.width = (CARDS.length ? n / CARDS.length * 100 : 0) + '%';
}
function toggle(key, id){
  STORE[key][id] = !STORE[key][id];
  if(!STORE[key][id]) delete STORE[key][id];
  save(key); refreshMarks();
  toast(STORE[key][id] ? '已标记' : '已取消');
}

/* ---- 笔记 ---- */
function bindNotes(){
  CARDS.forEach(c => {
    const sec = cardEl(c.id);
    const ta = sec.querySelector('[data-role=note]');
    ta.value = STORE.notes[c.id] || '';
    let timer;
    ta.addEventListener('input', () => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        STORE.notes[c.id] = ta.value; save('notes');
        const st = sec.querySelector('[data-role=nstatus]');
        st.textContent = '已自动保存 · ' + new Date().toLocaleTimeString();
        setTimeout(() => st.textContent = '', 2500);
      }, 500);
    });
    sec.querySelector('[data-role=learned]').onclick = () => toggle('learned', c.id);
    sec.querySelector('[data-role=starred]').onclick = () => toggle('starred', c.id);
  });
}

/* ---- 路由 ---- */
function route(){
  const id = location.hash.slice(1);
  const c = CARDS.find(x => x.id === id) || CARDS[0];
  document.querySelectorAll('.card').forEach(s =>
    s.classList.toggle('show', s.dataset.id === c.id));
  document.querySelectorAll('.tree-item').forEach(t =>
    t.classList.toggle('active', t.dataset.id === c.id));
  $('#crumb').innerHTML = c.part + ' / <b>' + c.title + '</b>';
  $('#learnedBtn').classList.toggle('on', !!STORE.learned[c.id]);
  $('#starBtn').classList.toggle('on', !!STORE.starred[c.id]);
  window.scrollTo(0, 0);
  setTimeout(() => charts.forEach(x => x.resize()), 60);
}

/* ---- 搜索 ---- */
function escRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
function doSearch(kw){
  kw = kw.trim();
  const reader = $('#reader'), panel = $('#searchPanel');
  if(!kw){ panel.classList.remove('show'); reader.style.display = 'block'; return; }
  const k = kw.toLowerCase();
  const hits = CARDS.filter(c =>
    (c.title + ' ' + (c.tags||[]).join(' ') + ' ' + c.part + ' ' + c.text).toLowerCase().includes(k));
  reader.style.display = 'none'; panel.classList.add('show');
  let html = '<h2>搜索 “' + kw + '” · 找到 ' + hits.length + ' 个知识点</h2>';
  if(!hits.length) html += '<div class="s-empty">没有匹配的知识点，换个关键词试试。</div>';
  hits.forEach(c => {
    const full = c.title + ' ' + c.text;
    const i = full.toLowerCase().indexOf(k);
    const snip = full.slice(Math.max(0, i - 22), i + 46)
      .replace(new RegExp(escRe(kw), 'i'), m => '<mark>' + m + '</mark>');
    html += '<div class="s-result" data-id="' + c.id + '">' +
      '<div class="sr-title">' + c.title + '</div>' +
      '<div class="sr-meta">' + c.part + ' · ' + (c.tags||[]).map(t => '#' + t).join(' ') + '</div>' +
      '<div class="sr-meta">…' + snip + '…</div></div>';
  });
  panel.innerHTML = html;
  panel.querySelectorAll('.s-result').forEach(el =>
    el.onclick = () => { $('#searchInput').value = ''; location.hash = el.dataset.id; });
}

/* ---- 深度切换 ---- */
function setDepth(b){
  document.body.classList.toggle('depth-basic', b);
  $('#dtAll').classList.toggle('on', !b);
  $('#dtBasic').classList.toggle('on', b);
  const id = currentId();
  if(b && id){
    const cur = CARDS.find(c => c.id === id);
    if(cur.diff >= 3){ const f = CARDS.find(c => c.diff < 3); if(f) location.hash = f.id; }
  }
}

/* ---- 导出 / Toast / 杂项 ---- */
let toastTimer;
function toast(msg){
  const t = $('#toast'); t.textContent = msg; t.classList.add('show');
  clearTimeout(toastTimer); toastTimer = setTimeout(() => t.classList.remove('show'), 1800);
}
$('#exportBtn').onclick = () => {
  const data = {exportedAt:new Date().toISOString(), learned:STORE.learned,
    starred:STORE.starred, notes:STORE.notes};
  const blob = new Blob([JSON.stringify(data, null, 2)], {type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = BRAND.app + '-notes-' + new Date().toISOString().slice(0,10) + '.json';
  a.click(); toast('笔记备份已导出');
};
$('#menuBtn').onclick = () => $('#sidebar').classList.toggle('open');
$('#searchInput').addEventListener('input', e => doSearch(e.target.value));
$('#learnedBtn').onclick = () => { const id = currentId(); if(id) toggle('learned', id); };
$('#starBtn').onclick = () => { const id = currentId(); if(id) toggle('starred', id); };
$('#dtAll').onclick = () => setDepth(false);
$('#dtBasic').onclick = () => setDepth(true);
window.addEventListener('hashchange', route);
window.addEventListener('resize', () => charts.forEach(c => c.resize()));
/* 目录点击（事件委托） */
document.getElementById('tree').addEventListener('click', e => {
  const item = e.target.closest('.tree-item');
  if(item){ location.hash = item.dataset.id; document.getElementById('sidebar').classList.remove('open'); }
});

renderTex(); initCharts(); bindNotes(); refreshMarks(); route();
"""

# ============================================================
# 本地 vendor 内联（KaTeX + ECharts，离线自包含）
# ============================================================

def load_vendor():
    if not os.path.isdir(VENDOR):
        print('未找到 vendor 目录(%s)，请先运行: python packages/tooling/src/fetch_vendor.py' % VENDOR)
        sys.exit(1)
    parts = []
    # --- KaTeX CSS：woff2 转 data URI，移除 woff/ttf fallback ---
    css = open(os.path.join(VENDOR, 'katex.min.css'), encoding='utf-8').read()
    def font_data(m):
        p = os.path.join(VENDOR, 'fonts', m.group(1))
        b = base64.b64encode(open(p, 'rb').read()).decode()
        return "url(data:font/woff2;base64,%s) format('woff2')" % b
    # 兼容 KaTeX CSS 中单/双引号两种写法：format('woff2') 与 format("woff2")
    css = re.sub(r'''url\(fonts/([^)]+?\.woff2)\)\s*format\((['"])woff2\2\)''', font_data, css)
    css = re.sub(r''',\s*url\(fonts/[^)]+?\.woff\)\s*format\((['"])woff\1\)''', '', css)
    css = re.sub(r''',\s*url\(fonts/[^)]+?\.ttf\)\s*format\((['"])truetype\1\)''', '', css)
    parts.append('<style>%s</style>' % css)
    # --- JS ---
    for f in ('katex.min.js', 'echarts.min.js'):
        js = open(os.path.join(VENDOR, f), encoding='utf-8').read()
        js = js.replace('</script>', '<\\/script>')
        parts.append('<script>%s</script>' % js)
    return '\n'.join(parts)

# ============================================================
# 主入口
# ============================================================
def _count_images(body):
    """统计正文中的本地图片引用数（与 freeze_manifest.extract_images 同口径）。"""
    n = 0
    for m in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', body):
        t = m.group(1).strip()
        if t.startswith(('http', 'data:')):
            continue
        n += 1
    return n


def reconcile_with_manifest(cards, manifest_path):
    """按 content-manifest.json 对账：章节数 / id 序列 / 标题序列 / 图片引用数。
    文件缺失时仅告警并跳过（维持自解析口径）；对账失败以非零退出。"""
    if not manifest_path:
        return
    if not os.path.exists(manifest_path):
        print('[manifest] 未找到 %s，跳过对账（维持自解析）' % manifest_path)
        return
    with open(manifest_path, encoding='utf-8') as f:
        man = json.load(f)
    docs = man.get('docs', [])
    problems = []
    if len(cards) != len(docs):
        problems.append('章节数 离线=%d manifest=%d' % (len(cards), len(docs)))
    if [c.get('rel') for c in cards] != [d['id'] for d in docs]:
        problems.append('章节 id 序列与 manifest 不一致（manifest id=相对路径）')
    if [c['title'] for c in cards] != [d['title'] for d in docs]:
        problems.append('标题序列与 manifest 不一致')
    built_imgs = sum(_count_images(c['body']) for c in cards)
    man_imgs = sum(len(d.get('images', [])) for d in docs)
    if built_imgs != man_imgs:
        problems.append('图片引用数 离线=%d manifest=%d' % (built_imgs, man_imgs))
    if problems:
        print('[manifest] 对账失败:')
        for p in problems:
            print('  [MISMATCH] ' + p)
        sys.exit(1)
    print('[manifest] 对账一致：%d 章 / %d 处图片 / revision=%s'
          % (len(cards), built_imgs, man.get('revision')))


def main():
    ap = add_common_args()
    ap.add_argument('--published', action='store_true',
                    help='只构建 status: published 的章节')
    ap.add_argument('--manifest', default='',
                    help='可选 content-manifest.json 路径；存在则构建后对账，缺失则跳过')
    args = ap.parse_args()

    global DOCS, DIST, VENDOR
    from paths_util import resolve_src
    DOCS = resolve_src(args)
    VENDOR = os.path.abspath(args.vendor)
    if args.out:
        DIST = os.path.abspath(args.out)
    _INLINE_BASE[0] = DOCS

    app = args.app
    brand = brand_for(app)

    only_pub = args.published
    cards = collect_cards(only_pub)
    if not cards:
        print('没有可构建的章节（检查 SUMMARY.md 与文件是否存在，或去掉 --published）')
        sys.exit(1)
    for c in cards:
        c['html'] = md_to_html(c)
    tree = build_tree(cards)
    card_html = ''.join(build_card(c, i, len(cards), cards)
                        for i, c in enumerate(cards))
    search = [{'id': c['id'], 'title': c['title'], 'part': c['part'],
               'tags': c['tags'], 'diff': c['difficulty'],
               'text': plain_text(c['body'])} for c in cards]
    brand_js = json.dumps({'app': app, 'storePrefix': brand['storePrefix']},
                          ensure_ascii=False)
    page = (PAGE_TEMPLATE
            .replace('__HTML_TITLE__', H.escape(brand['htmlTitle']))
            .replace('__BOOK_TITLE__', H.escape(brand['book']))
            .replace('__BOOK_EN__', H.escape(brand['en']))
            .replace('__SERIES__', H.escape(brand['series']))
            .replace('__VENDOR__', load_vendor())
            .replace('__CSS__', CSS_STR)
            .replace('__TREE__', tree)
            .replace('__CARDS__', card_html)
            .replace('__SEARCH__', json.dumps(search, ensure_ascii=False))
            .replace('__BRAND__', brand_js)
            .replace('__RUNTIME__', RUNTIME_JS))
    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, '%s.html' % app)
    open(out, 'w', encoding='utf-8').write(page)
    print('构建完成: %s（%d 章）' % (out, len(cards)))
    if WARNINGS:
        print('共 %d 条警告' % len(WARNINGS))
    reconcile_with_manifest(cards, args.manifest)

if __name__ == '__main__':
    main()
