#!/usr/bin/env python3
"""把品牌资产（packages/theme/public）同步到指定 app 的 docs/public。

VitePress 只拷贝 <srcDir>/public 到产物；门户没有 gen:sidebar，故用本脚本
在 predocs:build / predocs:dev 前同步 favicon 等品牌资产。

用法：
  python sync_public.py --app portal
  python sync_public.py --app hardware
"""
import argparse
import os
import shutil
import sys

import paths_util as P


def sync_public(app: str) -> int:
    src = os.path.join(P.REPO_ROOT, 'packages', 'theme', 'public')
    if not os.path.isdir(src):
        print('未找到品牌资产目录: %s' % src, file=sys.stderr)
        return 1
    docs = P.app_src(app)
    dst = os.path.join(docs, 'public')
    os.makedirs(dst, exist_ok=True)
    n = 0
    for fn in os.listdir(src):
        s = os.path.join(src, fn)
        if os.path.isfile(s):
            shutil.copy2(s, os.path.join(dst, fn))
            n += 1
    print('品牌 public 已同步: %s <- %s（%d 个文件）' % (dst, src, n))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--app', default='portal')
    a = ap.parse_args()
    return sync_public(a.app)


if __name__ == '__main__':
    raise SystemExit(main())
