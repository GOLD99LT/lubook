# -*- coding: utf-8 -*-
"""扫描所有章节公式（$...$ / $$...$$）中的不规范字符：
- 公式内中文（应包 \\text{}）
- Unicode 符号 µ Ω ° × ± ≤ ≥ ≈ 及上下标等（应改用 KaTeX 命令）
只报告，不修改。参数化：--src 指定内容源（默认 <repo>/docs）。
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths_util import add_common_args, resolve_src
_args, _ = add_common_args().parse_known_args()
DOCS = resolve_src(_args)

CJK = re.compile(r'[\u4e00-\u9fff]')
# KaTeX 不直接支持或应使用命令的 Unicode
BAD = {
    '\u00b5': '\\mu', '\u03a9': '\\Omega', '\u00b0': '^{\\circ}',
    '\u00d7': '\\times', '\u00b1': '\\pm', '\u2264': '\\leq',
    '\u2265': '\\geq', '\u2248': '\\approx', '\u2212': '-',
    '\u2080':'_0','\u2081':'_1','\u2082':'_2','\u2083':'_3',
    '\u2126': '\\Omega', '\u03bc': '\\mu',
}

def formulas(body):
    out = []
    for m in re.finditer(r'\$\$(.+?)\$\$', body, re.S):
        out.append(('block', m.group(1)))
    tmp = re.sub(r'\$\$.+?\$\$', '', body, flags=re.S)
    for m in re.finditer(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$', tmp, re.S):
        out.append(('inline', m.group(1)))
    return out

total_files = 0
total_issues = 0
for part in sorted(os.listdir(DOCS)):
    pd = os.path.join(DOCS, part)
    if not os.path.isdir(pd) or part in ('assets',):
        continue
    for f in sorted(os.listdir(pd)):
        if not f.endswith('.md'):
            continue
        rel = '%s/%s' % (part, f)
        body = open(os.path.join(pd, f), encoding='utf-8').read()
        issues = []
        for kind, tex in formulas(body):
            bad_hits = [c for c in BAD if c in tex]
            tex_no_text = re.sub(r'\\text\{[^}]*\}', '', tex)
            cjk = CJK.findall(tex_no_text)
            if bad_hits or cjk:
                issues.append((kind, sorted(set(bad_hits)), ''.join(sorted(set(cjk))),
                              tex.strip()[:70]))
        if issues:
            total_files += 1
            total_issues += len(issues)
            print('\n%s' % rel)
            for kind, bh, cj, snip in issues:
                print('  [%s] 符号:%s 中文:%s' % (kind, ''.join(bh) or '-', cj or '-'))
                print('       %s' % snip)

print('\n==== 共 %d 个文件、%d 处公式需修正 ====' % (total_files, total_issues))
