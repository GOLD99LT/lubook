#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_pages_bundle.py — 多 app 合并部署目录（ADR-0006 / NAMING）。

按 VP_BASE 构建门户 + 各内容分册，并把它们组装成一个整体可部署目录：
  门户 portal 的 dist → bundle 根（base = VP_BASE）
  内容分册 <slug> 的 dist → bundle/<slug>/（base = VP_BASE + '<slug>/'）
部署取值：
  GitHub Pages  VP_BASE=/lubook/  → 门户 /lubook/、分册 /lubook/<slug>/
  Cloudflare    VP_BASE=/         → 门户 /、分册 /<slug>/

用法：
  python packages/tooling/src/build_pages_bundle.py --vp-base /lubook/
  python packages/tooling/src/build_pages_bundle.py --vp-base / --include-offline
  python packages/tooling/src/build_pages_bundle.py --skip-build --out site
零第三方依赖（Python 标准库）。
"""
import os, sys, shutil, subprocess, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from paths_util import REPO_ROOT, list_apps, app_dist


def normalize_base(vp):
    b = (vp or '/').strip()
    if not b.startswith('/'):
        b = '/' + b
    if not b.endswith('/'):
        b = b + '/'
    return b


def find_pnpm():
    """定位 pnpm 可执行（Windows 下解析到 pnpm.CMD，避免 CreateProcess 找不到 .CMD）。"""
    found = shutil.which('pnpm')
    if found:
        return found
    for cand in ('pnpm.CMD', 'pnpm.cmd', 'pnpm'):
        p = shutil.which(cand)
        if p:
            return p
    return 'pnpm'


def run_build(pnpm, app, env):
    print('--- 构建 app=%s（VP_BASE=%s）---' % (app, env['VP_BASE']))
    p = subprocess.run([pnpm, 'run', 'build:' + app], cwd=REPO_ROOT, env=env)
    return p.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vp-base', default=None,
                    help='部署根 base（默认读 VP_BASE 环境变量，再默认 /）')
    ap.add_argument('--out', default=os.path.join(REPO_ROOT, '.bundle'),
                    help='整体部署目录输出路径（默认 .bundle）')
    ap.add_argument('--apps', default=None,
                    help='逗号分隔的 app 列表（默认遍历 apps/*，portal 优先）')
    ap.add_argument('--skip-build', action='store_true',
                    help='跳过构建，仅从现有 dist 组装')
    ap.add_argument('--include-offline', action='store_true',
                    help='同时把 dist/<app>.html 离线单文件拷进 bundle')
    args = ap.parse_args()

    vp_raw = args.vp_base if args.vp_base is not None else os.environ.get('VP_BASE', '/')
    vp = normalize_base(vp_raw)
    out = os.path.abspath(args.out)

    apps = args.apps.split(',') if args.apps else list_apps()
    apps = [a.strip() for a in apps if a.strip()]
    if 'portal' in apps:
        apps = ['portal'] + [a for a in apps if a != 'portal']

    env = dict(os.environ)
    env['VP_BASE'] = vp
    env['PYTHONUTF8'] = '1'

    pnpm = find_pnpm()

    # 1) 构建（base 在构建期烘焙）
    if not args.skip_build:
        for app in apps:
            rc = run_build(pnpm, app, env)
            if rc != 0:
                print('app=%s 构建失败（exit %d）' % (app, rc))
                sys.exit(rc)

    # 2) 组装
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out, exist_ok=True)

    placed = []
    for app in apps:
        src = app_dist(app)
        if not os.path.isdir(src):
            print('缺少 dist: %s（先构建，或去掉 --skip-build）' % src)
            sys.exit(1)
        dst = out if app == 'portal' else os.path.join(out, app)
        os.makedirs(dst, exist_ok=True)
        shutil.copytree(src, dst, dirs_exist_ok=True)
        placed.append((app, '/' if app == 'portal' else '/' + app + '/'))

    # 3) 离线单文件（可选）
    if args.include_offline:
        for app in apps:
            offline = os.path.join(REPO_ROOT, 'dist', app + '.html')
            if os.path.isfile(offline):
                shutil.copy2(offline, os.path.join(out, app + '.html'))

    # 4) 报告
    print('\n=== bundle 已组装：%s（VP_BASE=%s）===' % (out, vp))
    for app, path in placed:
        print('  %-10s -> %s' % (app, path))
    if args.include_offline:
        print('  （已含离线单文件 dist/<app>.html）')


if __name__ == '__main__':
    main()
