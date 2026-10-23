#!/usr/bin/env python3
"""上线体检：按路由快照逐页检查线上站点。

为什么需要它：`verify:all` 验证的是本地构建，部署之后仍是另一回事——
曾有 portal 404、两张 SVG 破图、43 条死链在旧门禁下全绿却线上可见。
本脚本补的是"部署后"这一段：

1. 每条路由 HTTP 200；
2. 页面里有 `<title>`（不是空壳或错误页）；
3. HTML 里引用的同源资源（js/css/svg/png…）都能取到 200 —— 抓破图与缺 chunk；
4. 报告每页大小，异常大的单独列出（排查"某页突然膨胀"）。

不做的事（需要浏览器的部分交给人工/截图）：KaTeX 实际渲染、ECharts 绘制、交互行为。

用法：
    python packages/tooling/src/check_live_site.py --base https://gold99lt.github.io/lubook/hardware --app hardware
    python packages/tooling/src/check_live_site.py --base https://lubook.pages.dev/hardware --app hardware
    python packages/tooling/src/check_live_site.py --base ... --limit 10          # 抽样
    python packages/tooling/src/check_live_site.py --base ... --check-assets      # 连资源一起查

退出码：0 = 全绿；1 = 有失败项。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

UA = 'lubook-live-check/1.0'
TITLE_RE = re.compile(r'<title>(.*?)</title>', re.S)
ASSET_RE = re.compile(r'(?:src|href)="(/[^"#?]+\.(?:js|css|svg|png|jpe?g|webp|woff2?))"')


def fetch(url: str, timeout: float = 25.0, retries: int = 2):
    """取一次，失败重试。并发下偶发连接重置很常见，不该当成站点故障。"""
    last = (0, b'', 'unknown')
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, resp.read(), None
        except urllib.error.HTTPError as e:
            last = (e.code, b'', 'HTTP %s' % e.code)
            # 4xx 重试没意义；5xx 可能是临时的，留下一次机会
            if e.code < 500:
                return last
        except Exception as e:  # noqa: BLE001 - 网络异常种类多，统一记录
            last = (0, b'', type(e).__name__)
        if attempt < retries:
            time.sleep(0.6 * (attempt + 1))
    return last


def load_routes(app: str):
    snap = os.path.join(ROOT, 'tests', '%s.routes.snapshot.json' % app)
    if not os.path.exists(snap):
        return []
    with open(snap, encoding='utf-8') as fh:
        data = json.load(fh)
    if isinstance(data, dict):
        data = data.get('routes', [])
    routes = []
    for item in data:
        if isinstance(item, str):
            routes.append(item)
        elif isinstance(item, dict):
            routes.append(item.get('route') or item.get('path') or '')
    return [r for r in routes if r]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True, help='站点基址，如 https://host/hardware')
    ap.add_argument('--app', default='hardware', help='用哪个 routes 快照')
    ap.add_argument('--limit', type=int, default=0, help='只查前 N 条（抽样）')
    ap.add_argument('--check-assets', action='store_true', help='额外检查页面引用的同源资源')
    ap.add_argument('--workers', type=int, default=8)
    args = ap.parse_args()

    base = args.base.rstrip('/')
    parsed = urllib.parse.urlparse(base)
    origin = '%s://%s' % (parsed.scheme, parsed.netloc)
    base_path = parsed.path.rstrip('/')

    def resolve_asset(path: str) -> str:
        """页面里的资源是站点绝对路径（已含 base 前缀），别再拼一次 base。"""
        if base_path and path.startswith(base_path + '/'):
            return origin + path
        return origin + base_path + path if base_path else origin + path

    routes = load_routes(args.app)
    if not routes:
        print('没有可用的路由快照: tests/%s.routes.snapshot.json' % args.app)
        return 1
    if args.limit:
        routes = routes[: args.limit]

    failures = []
    sizes = []

    def check(route: str):
        url = base + route
        status, body, err = fetch(url)
        title = ''
        if body:
            m = TITLE_RE.search(body.decode('utf-8', 'ignore'))
            title = (m.group(1).strip() if m else '')
        return route, status, len(body), title, err, body

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(check, routes))

    assets_checked = 0
    for route, status, size, title, err, body in results:
        sizes.append((size, route))
        if status != 200:
            failures.append('%s -> HTTP %s %s' % (route, status, err or ''))
            continue
        if not title:
            failures.append('%s -> 没有 <title>（疑似空壳/错误页）' % route)
        if args.check_assets and body:
            html = body.decode('utf-8', 'ignore')
            for m in ASSET_RE.finditer(html):
                path = m.group(1)
                assets_checked += 1
                code, _b, _e = fetch(resolve_asset(path), timeout=15)
                if code != 200:
                    failures.append('%s -> 资源 %s HTTP %s' % (route, path, code))

    sizes.sort(reverse=True)
    print('==== 上线体检 ====')
    print('站点: %s' % base)
    print('路由: %d 条；失败: %d 条%s'
          % (len(routes), len(failures), '；资源检查: %d 个' % assets_checked if args.check_assets else ''))
    if sizes:
        print('最大页面: %s（%.0f KB）' % (sizes[0][1], sizes[0][0] / 1024))
        print('中位页面: %.0f KB' % (sorted(s for s, _r in sizes)[len(sizes) // 2] / 1024))
    if failures:
        print('\n失败项（最多显示 20 条）:')
        for f in failures[:20]:
            print('  - %s' % f)
        return 1
    print('\n全部通过。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
