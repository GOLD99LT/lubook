#!/usr/bin/env python3
"""旧错误说法的回归扫描（报告用，不阻断构建）。

背景：这次内容整改纠正了 300+ 处技术错误，其中很多是"读起来很顺、但推导是错的"说法。
它们已经改掉了，但同类错误很容易被后续写作者重新写回来（尤其是参考旧稿/旧图时）。
本脚本把其中最危险的几条固化成模式，扫描全文，**命中即报告**。

设计取舍：
- **只收"实践中几乎不会合法出现"的模式**，避免误报把工具变成噪音。
  例如 "D=CCR/ARR" 就故意不收——正文里讨论"常见错误"时会合法地引用它。
- 默认只报告、退出码 0；加 `--strict` 才在命中时返回 1，方便手工巡检或将来接入门禁。

用法：
    python packages/tooling/src/scan_legacy_errors.py --app hardware
    python packages/tooling/src/scan_legacy_errors.py --app hardware --strict
    python packages/tooling/src/scan_legacy_errors.py --app hardware --json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

# (正则, 说明, 正确说法)
PATTERNS = [
    (
        r'θ_\{JA\}\s*=\s*θ_\{JC\}\s*\+\s*θ_\{JB\}|θJA\s*=\s*θJC\s*\+\s*θJB',
        '热阻串联模型',
        'θJA 是壳路径与板路径的并联：(θJC+θCA)∥(θJB+θBA)；三者相加是错的。',
    ),
    (
        r'输入门限是?按\s*5\s*V\s*逻辑设计',
        'MAX232 归因错误',
        'MAX232 不能用于 3.3V 的主因是供电（规定 5V±10%），其逻辑输入是 TTL 兼容的。',
    ),
    (
        r'多数\s*RS-?232\s*接收器内部有偏置',
        'RS-232 失效保护绝对化',
        '标准不强制接收器带失效保护偏置，只能说"很多带偏置的接收器"。',
    ),
    (
        r'1A/mm²?\s*(?:约|大致|就够了)',
        '载流口诀当结论',
        'IPC-2221 的 A 单位是 mil²；外层 1oz/10°C 约 2.4A/mm，1A/mm 只是保守口诀。',
    ),
    (
        r'共模.{0,6}(?:可差|能差|相差).{0,4}几十伏',
        'RS-232 共模能力',
        'RS-232 是单端对地接口，"几十伏共模"是 RS-485/CAN 的指标。',
    ),
    (
        r'平面电容.{0,10}(?:等效|代替|替代).{0,6}去耦',
        '平面电容当去耦',
        '1cm²/0.2mm 只有约 19pF，不能当去耦主力。',
    ),
    (
        r'降低噪声增益.{0,12}(?:改善|提高|救).{0,6}稳定',
        '噪声增益方向',
        '能改善稳定性的是**提高**噪声增益，不是降低。',
    ),
]


# 命中后还要看上下文：正文在"指出这个说法是错的"时，会合法地引用错误说法。
# 这些标记出现在命中位置附近，就判为"已澄清"，不计入命中。
CLARIFY_MARKERS = (
    '反的', '相反', '错误', '不对', '不是', '不能', '不可', '并非', '误',
    '纠正', '勘误', '有人', '常见的说', '常见一句', '网上常见', '以为', '别',
    '而非', '其实', '正确', '应为', '应该',
)
WINDOW_BEFORE = 40
WINDOW_AFTER = 60

QUOTE_PAIRS = (('“', '”'), ('「', '」'), ('"', '"'), ('《', '》'))


def is_quoted(line: str, start: int, end: int) -> bool:
    """命中处在引号里 → 是在**引用**这个说法，不是主张它。

    两种情况：
    - 成对但同字符（ASCII 双引号）：用到 start 之前的引号个数奇偶判断是否在引号内；
    - 开闭不同字符（“” 「」 《》）：找 start 之前最近的开引号，且 end 之后有闭引号。
    """
    for open_q, close_q in QUOTE_PAIRS:
        if open_q == close_q:
            if line.count(open_q, 0, start) % 2 == 1:
                return True
        else:
            opened = line.rfind(open_q, 0, start)
            if opened >= 0 and line.find(close_q, end) >= 0:
                # 确保这个开引号之后到 end 之间没有别的同种开引号（避免误判）
                if line.find(open_q, opened + len(open_q), start) < 0:
                    return True
    return False


def is_clarified(line: str, start: int, end: int) -> bool:
    if is_quoted(line, start, end):
        return True
    window = line[max(0, start - WINDOW_BEFORE): min(len(line), end + WINDOW_AFTER)]
    return any(marker in window for marker in CLARIFY_MARKERS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--app', default='hardware')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--strict', action='store_true', help='命中即非零退出')
    args = ap.parse_args()

    src = os.path.join(ROOT, 'apps', args.app, 'docs')
    if not os.path.isdir(src):
        print('目录不存在: %s' % src)
        return 2

    hits = []
    clarified = 0
    scanned = 0
    for dirpath, _dirs, files in os.walk(src):
        for name in sorted(files):
            if not name.endswith('.md'):
                continue
            path = os.path.join(dirpath, name)
            scanned += 1
            with open(path, encoding='utf-8', errors='ignore') as fh:
                text = fh.read()
            for line_no, line in enumerate(text.splitlines(), 1):
                for pattern, label, fix in PATTERNS:
                    for m in re.finditer(pattern, line):
                        if is_clarified(line, m.start(), m.end()):
                            clarified += 1
                            continue
                        hits.append({
                            'file': os.path.relpath(path, src).replace(os.sep, '/'),
                            'line': line_no,
                            'label': label,
                            'fix': fix,
                            'text': line.strip()[:120],
                        })

    if args.json:
        print(json.dumps({'scanned': scanned, 'hits': hits}, ensure_ascii=False, indent=2))
    else:
        print('==== 旧错误说法回归扫描 ====')
        print('扫描 %d 个 Markdown；命中 %d 处；另有 %d 处是正文在纠错（已排除）'
              % (scanned, len(hits), clarified))
        for h in hits:
            print('  %s:%d  [%s]' % (h['file'], h['line'], h['label']))
            print('     原文: %s' % h['text'])
            print('     应为: %s' % h['fix'])
        if not hits:
            print('\n未发现已知的旧错误说法。')

    if args.strict and hits:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
