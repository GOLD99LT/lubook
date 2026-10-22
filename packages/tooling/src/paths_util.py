# -*- coding: utf-8 -*-
"""
paths_util.py — packages/tooling 共享路径默认值（纯 Python 标准库，零第三方依赖）。

按 ARCHITECTURE §4 / ADR-0006：脚本参数化 --app/--src/--out/--vendor，默认对 hardware 等价：
  - app    = 'hardware'
  - src    = <repo_root>/apps/hardware/docs
  - vendor = <repo_root>/packages/tooling/vendor
未传参时默认值与硬件分册当前布局等价，保证 run_quality.py --app hardware 可跑通。
"""
import os
import shutil
import argparse

# packages/tooling/src
HERE = os.path.dirname(os.path.abspath(__file__))
# packages/tooling
TOOLING_DIR = os.path.dirname(HERE)


def find_repo_root(start=None):
    """向上查找含 ARCHITECTURE.md 的目录作为仓库根。"""
    d = os.path.abspath(start or HERE)
    while True:
        if os.path.exists(os.path.join(d, 'ARCHITECTURE.md')):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return d
        d = parent


REPO_ROOT = find_repo_root()
# P2 起内容在 apps/<slug>/docs；品牌重命名后硬件分册为 apps/hardware/docs
DEFAULT_SRC = os.path.join(REPO_ROOT, 'apps', 'hardware', 'docs')
DEFAULT_VENDOR = os.path.join(TOOLING_DIR, 'vendor')
DEFAULT_OUT_DIST = os.path.join(REPO_ROOT, 'dist')


def pnpm_cmd():
    """返回调用 pnpm 的命令前缀（列表）。

    有的机器只装了 corepack、没有独立的 pnpm 可执行文件（Windows 上尤其常见），
    直接 subprocess 调 'pnpm' 会抛 FileNotFoundError/ WinError 2。
    这里按 pnpm -> pnpm.cmd -> corepack pnpm 的顺序回退。
    """
    for name in ('pnpm', 'pnpm.cmd', 'pnpm.CMD', 'pnpm.exe'):
        p = shutil.which(name)
        if p:
            return [p]
    for name in ('corepack', 'corepack.cmd', 'corepack.exe'):
        p = shutil.which(name)
        if p:
            return [p, 'pnpm']
    return ['pnpm']

def list_apps():
    """返回 apps/ 下含 package.json 的分册 slug 列表（按目录名排序，含 portal）。"""
    apps_dir = os.path.join(REPO_ROOT, 'apps')
    if not os.path.isdir(apps_dir):
        return []
    out = []
    for name in sorted(os.listdir(apps_dir)):
        if os.path.isfile(os.path.join(apps_dir, name, 'package.json')):
            out.append(name)
    return out


def app_src(app):
    """分册内容源目录：apps/<app>/docs。"""
    return os.path.join(REPO_ROOT, 'apps', app, 'docs')


def app_dist(app):
    """分册 VitePress 构建产物目录：apps/<app>/docs/.vitepress/dist。"""
    return os.path.join(REPO_ROOT, 'apps', app, 'docs', '.vitepress', 'dist')


def add_common_args(parser=None, out_default=None):
    """给 ArgumentParser 追加 --app/--src/--out/--vendor 四个通用参数。
    未显式传 --src 时，--src 随 --app 派生（apps/<app>/docs）。"""
    p = parser or argparse.ArgumentParser()
    p.add_argument('--app', default='hardware',
                   help='应用 slug（默认 hardware）')
    p.add_argument('--src', default=None,
                   help='内容源目录（默认 apps/<app>/docs）')
    p.add_argument('--out', default=out_default,
                   help='输出目录/文件（默认见各脚本）')
    p.add_argument('--vendor', default=DEFAULT_VENDOR,
                   help='vendor 资源目录（默认 packages/tooling/vendor）')
    return p


def resolve_src(args):
    """统一口径：--src 显式优先，否则 apps/<app>/docs。"""
    if getattr(args, 'src', None):
        return os.path.abspath(args.src)
    return app_src(getattr(args, 'app', 'hardware'))
