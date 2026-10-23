#!/usr/bin/env python3
"""数学渲染产物契约检查（ADR-0012）。

背景：为了让构建内存从 5.94 GB 降到 2.30 GB，数学公式改为**运行期渲染**：
构建产物里只应有 `<span class="math-tex" data-math="…">TeX 源码</span>` 占位，
由 `@lubook/theme` 在浏览器里懒加载 katex 填充。

这个契约很脆——任何一处改动都可能悄悄退回旧行为或让公式消失：

| 可能的回归 | 后果 | 本脚本能查出 |
|---|---|---|
| 有人设了 `LUBOOK_MATH=build` | 构建内存回到 5.9 GB，页面上没有占位 | 构建产物里出现 `class="katex"` |
| 占位渲染器被删/改 | 浏览器无公式可渲染，页面显示原始 TeX | 占位缺 `data-math` |
| katex 懒加载 chunk 没打出 | 占位永远不渲染 | dist 里没有 katex chunk |
| 主题的渲染器被删 | 占位永远不渲染 | 主题 chunk 里没有 `data-rendered` |

浏览器里的"真的渲染出来了"仍由人工/截图验证（CI 不做浏览器），
但上面这些**静态可判**的回归应该由门禁拦住，而不是等读者发现公式不见了。

用法：
    python packages/tooling/src/scan_math_render.py --app hardware
    python packages/tooling/src/scan_math_render.py --app hardware --dist <dir>

退出码：0 = 契约成立；1 = 违约（打印具体原因）
"""

from __future__ import annotations

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))          # packages/tooling/src
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))  # repo root

PLACEHOLDER_RE = re.compile(r'<span class="math-tex[^"]*"([^>]*)>')
BUILD_TIME_KATEX_RE = re.compile(r'<span class="katex')


def iter_files(root: str, suffix: str):
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            if name.endswith(suffix):
                yield os.path.join(dirpath, name)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--app', default='hardware')
    ap.add_argument('--dist', default='', help='默认 apps/<app>/docs/.vitepress/dist')
    args = ap.parse_args()

    dist = args.dist or os.path.join(ROOT, 'apps', args.app, 'docs', '.vitepress', 'dist')
    if not os.path.isdir(dist):
        print('找不到构建产物: %s（先跑 build:%s）' % (dist, args.app))
        return 1

    problems = []
    placeholders = 0
    missing_attr = 0
    built_time_katex = 0
    html_count = 0

    for path in iter_files(dist, '.html'):
        html_count += 1
        with open(path, encoding='utf-8', errors='ignore') as fh:
            text = fh.read()
        placeholders += text.count('class="math-tex')
        built_time_katex += len(BUILD_TIME_KATEX_RE.findall(text))
        for m in PLACEHOLDER_RE.finditer(text):
            if 'data-math=' not in m.group(1):
                missing_attr += 1
                if len(problems) < 5:
                    problems.append('占位缺 data-math: %s' % os.path.relpath(path, dist))

    if built_time_katex:
        problems.append(
            '构建产物里有 %d 处 class="katex" —— 说明构建期又渲染了公式'
            '（检查是否有人设了 LUBOOK_MATH=build，见 ADR-0012）' % built_time_katex)

    if missing_attr:
        problems.append('%d 个占位缺 data-math 属性（客户端无法渲染）' % missing_attr)

    assets = os.path.join(dist, 'assets')
    js_files = list(iter_files(assets, '.js')) if os.path.isdir(assets) else []
    has_katex_chunk = any('katex' in os.path.basename(p).lower() for p in js_files)
    has_renderer = False
    for p in js_files:
        try:
            with open(p, encoding='utf-8', errors='ignore') as fh:
                if 'data-rendered' in fh.read():
                    has_renderer = True
                    break
        except OSError:
            continue

    if placeholders and not has_katex_chunk:
        problems.append('产物里没有 katex 懒加载 chunk（客户端无法渲染）')
    if placeholders and not has_renderer:
        problems.append('主题 chunk 里找不到运行期渲染器（没有 data-rendered 标记）')

    print('==== 数学渲染契约 ====')
    print('页面: %d 个；占位: %d 个；构建期 katex: %d 处' % (html_count, placeholders, built_time_katex))
    print('katex chunk: %s；运行期渲染器: %s'
          % ('有' if has_katex_chunk else '无', '有' if has_renderer else '无'))

    if problems:
        print('\n违约：')
        for p in problems:
            print('  - %s' % p)
        return 1

    print('\n契约成立。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
