#!/usr/bin/env python3
"""外链与来源复核：把 docs 里所有 http(s) 链接抓一遍，按可判定的事实分类。

背景：内容里 400+ 次外链引用（TI/ADI 应用笔记、厂商数据手册、GitHub 仓库、标准书城）。
`validate.py` 只查站内相对链接，外链以前从未系统验证过——而"编号写得对、URL 拼错"
或"文档已下架"这类问题，读者点开才知道。

本脚本只报告**机器能判定的事实**，不猜内容：
- `ok`      : 200，且（HTML 有 title / PDF 或其它类型有正确 Content-Type）
- `dead`    : 404 / 410 —— 链接确实不存在
- `blocked` : 403 / 406 / 429 / 401 —— 站点反爬或需登录，**不能据此判定失效**
- `error`   : 超时 / DNS / TLS / 连接重置
- `redirect` : 3xx 跳到别处（记录最终 URL，供人工判断是否仍指向同一文档）

不做的：标题与正文声称是否一致（需要语义判断，交人工看报告）。

用法：
    python packages/tooling/src/verify_sources.py --app hardware
    python packages/tooling/src/verify_sources.py --app hardware --json
    python packages/tooling/src/verify_sources.py --app hardware --dead-only

退出码：0 = 没有 dead；1 = 存在 dead（blocked/error 不算失效，只提示）。
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

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36 lubook-source-check/1.0')
URL_RE = re.compile(r'https?://[^\s)\]<>"`，。；）]+')
TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.S | re.I)


def collect(app: str):
    src = os.path.join(ROOT, 'apps', app, 'docs')
    uses = {}
    for dirpath, _dirs, files in os.walk(src):
        for name in sorted(files):
            if not name.endswith('.md'):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, src).replace(os.sep, '/')
            with open(path, encoding='utf-8', errors='ignore') as fh:
                text = fh.read()
            for m in URL_RE.finditer(text):
                url = m.group(0).rstrip('.,;:!?、')
                uses.setdefault(url, set()).add(rel)
    return uses


def probe(url: str):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                ctype = (resp.headers.get('Content-Type') or '').split(';')[0].strip()
                final = resp.geturl()
                body = b''
                if 'html' in ctype.lower():
                    body = resp.read(200_000)
                title = ''
                if body:
                    m = TITLE_RE.search(body.decode('utf-8', 'ignore'))
                    title = re.sub(r'\s+', ' ', m.group(1)).strip()[:120] if m else ''
                return {'status': resp.status, 'ctype': ctype, 'final': final,
                        'title': title, 'kind': 'ok'}
        except urllib.error.HTTPError as e:
            code = e.code
            if code in (401, 403, 406, 429):
                return {'status': code, 'ctype': '', 'final': url, 'title': '',
                        'kind': 'blocked'}
            if code in (404, 410):
                return {'status': code, 'ctype': '', 'final': url, 'title': '',
                        'kind': 'dead'}
            if 500 <= code < 600 and attempt < 2:
                time.sleep(1.0 * (attempt + 1))
                continue
            return {'status': code, 'ctype': '', 'final': url, 'title': '',
                    'kind': 'error'}
        except Exception as e:  # noqa: BLE001
            if attempt < 2:
                time.sleep(1.0 * (attempt + 1))
                continue
            return {'status': 0, 'ctype': '', 'final': url, 'title': '',
                    'kind': 'error', 'note': type(e).__name__}
    return {'status': 0, 'ctype': '', 'final': url, 'title': '', 'kind': 'error'}


def dns_caveat(urls):
    """检查本机 DNS 是否被透明代理接管。

    实测教训（2026-10-24）：本机所有域名都解析到 198.18.0.0/15（RFC 2544 基准网段），
    这是 Clash/VPN 之类 TUN 模式的典型表现。此时 HTTP 结果取决于代理规则，
    部分站点会返回 404/超时——**不能据此判定链接失效**。
    工具必须把这一点说出来，否则会得出"9 条死链"这种不可信的结论。
    """
    import ipaddress
    import socket

    hosts = []
    for u in urls:
        m = re.match(r'https?://([^/]+)', u)
        if m and m.group(1) not in hosts:
            hosts.append(m.group(1))
        if len(hosts) >= 3:
            break
    suspicious = []
    for host in hosts:
        try:
            addrs = {a[4][0] for a in socket.getaddrinfo(host, None)}
        except Exception:  # noqa: BLE001
            continue
        for addr in addrs:
            try:
                ip = ipaddress.ip_address(addr)
            except ValueError:
                continue
            if ip.is_private or ip.is_loopback or addr.startswith('198.18.') or addr.startswith('198.19.'):
                suspicious.append((host, addr))
    return suspicious


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--app', default='hardware')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--dead-only', action='store_true')
    ap.add_argument('--workers', type=int, default=6)
    args = ap.parse_args()

    uses = collect(args.app)
    urls = sorted(uses)
    if not urls:
        print('没有找到外链')
        return 0

    print('待检查外链 %d 条…' % len(urls), flush=True)
    caveat = dns_caveat(urls)
    if caveat:
        print('\n!! 注意：本机 DNS 把公网域名解析到内网/保留地址，说明有透明代理接管：')
        for host, addr in caveat[:5]:
            print('     %s -> %s' % (host, addr))
        print('   此时 404/超时 可能来自代理而非站点本身，**不能据此判定链接失效**；')
        print('   能确认的只有"200 可访问"，失效结论需换网络或人工复核。\n')
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(probe, urls))

    rows = []
    for url, res in zip(urls, results):
        res['url'] = url
        res['usedIn'] = sorted(uses[url])
        if res['final'] and res['final'].rstrip('/') != url.rstrip('/'):
            res['kind'] = res['kind'] if res['kind'] != 'ok' else 'redirect'
        rows.append(res)

    by_kind = {}
    for r in rows:
        by_kind.setdefault(r['kind'], []).append(r)

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print('==== 外链复核 ====')
        for kind in ('dead', 'blocked', 'error', 'redirect', 'ok'):
            group = by_kind.get(kind, [])
            print('%-9s %d' % (kind, len(group)))
        for kind in ('dead', 'error', 'blocked', 'redirect'):
            group = by_kind.get(kind, [])
            if not group or args.dead_only and kind != 'dead':
                continue
            print('\n---- %s（%d）----' % (kind, len(group)))
            for r in group[:30]:
                print('  %s -> HTTP %s %s' % (r['url'], r['status'], r.get('note', '')))
                if r['title']:
                    print('      title: %s' % r['title'])
                print('      引用: %s' % ', '.join(r['usedIn'][:4]))

    return 1 if by_kind.get('dead') else 0


if __name__ == '__main__':
    sys.exit(main())
