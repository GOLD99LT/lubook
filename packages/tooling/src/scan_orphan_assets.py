#!/usr/bin/env python3
"""清点未被任何章节引用的原理图（孤儿图）。

结论先行（2026-10-23 评估）：本仓现有 129 张孤儿图，合计约 363 KB，
**没有一张进入构建产物**——VitePress 只打包被引用的资源，所以它们对读者是零成本。
因此本脚本**默认只报告、不删除**：删掉它们只省仓库体积，却可能误删将来要复用的图。

什么时候才值得删：
- 仓库体积成为问题时（例如连续大图占用超过几十 MB）；
- 或者某张图**内容已被证伪**（错的公式/错的拓扑），留着会误导后来的人。
  这种情况应该由章节作者在改稿时顺手删，而不是批量清理。

用法：
    python packages/tooling/src/scan_orphan_assets.py --app hardware
    python packages/tooling/src/scan_orphan_assets.py --app hardware --json
    python packages/tooling/src/scan_orphan_assets.py --app hardware --max-kb 500   # 超过阈值才非零退出

退出码：默认 0；给了 --max-kb 且超出时为 1。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

IMG_RE = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')


def collect(app: str):
    src = os.path.join(ROOT, 'apps', app, 'docs')
    schematics = os.path.join(src, 'assets', 'schematics')
    used = set()
    for dirpath, _dirs, files in os.walk(src):
        for name in files:
            if not name.endswith('.md'):
                continue
            with open(os.path.join(dirpath, name), encoding='utf-8', errors='ignore') as fh:
                text = fh.read()
            for m in IMG_RE.finditer(text):
                target = m.group(1).split()[0]
                if target.startswith(('http', 'data:')):
                    continue
                used.add(os.path.basename(os.path.normpath(os.path.join(dirpath, target))))

    if not os.path.isdir(schematics):
        return None, None, []

    all_svg = sorted(f for f in os.listdir(schematics) if f.endswith('.svg'))
    data = []
    for name in all_svg:
        if name in used:
            continue
        path = os.path.join(schematics, name)
        data.append({'name': name, 'bytes': os.path.getsize(path)})
    return schematics, all_svg, data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--app', default='hardware')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--max-kb', type=float, default=0,
                    help='孤儿图总量上限（KB）；超过则非零退出。默认 0 = 只报告')
    args = ap.parse_args()

    schematics, all_svg, data = collect(args.app)
    if schematics is None:
        print('找不到原理图目录: %s' % schematics)
        return 1

    total = sum(d['bytes'] for d in data)
    report = {
        'app': args.app,
        'svgs': len(all_svg),
        'orphans': len(data),
        'orphanKb': round(total / 1024.0, 1),
        'top': [d['name'] for d in sorted(data, key=lambda x: -x['bytes'])[:10]],
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print('==== 孤儿原理图清点 ====')
        print('SVG 总数: %d；被引用: %d；孤儿: %d（%.1f KB）'
              % (report['svgs'], report['svgs'] - report['orphans'], report['orphans'],
                 report['orphanKb']))
        print('提示：孤儿图不进入构建产物，对读者零成本；删除前请确认没有复用计划。')
        if report['top']:
            print('最大的孤儿图: %s' % ', '.join(report['top'][:6]))

    if args.max_kb and report['orphanKb'] > args.max_kb:
        print('\n超出上限 %.1f KB（当前 %.1f KB）' % (args.max_kb, report['orphanKb']))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
