#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_all.py — 多 app 全量验证（ADR-0006 起替代单 app 的 verify）。

遍历 apps/*，对每个 app 执行：
  1. 构建（build:<app>，含 gen sidebar/catalog）
  2. 内容 app：run_quality（manifest/快照 + validate/scan）
  3. 内容 app：freeze_manifest + 离线单文件 build_single_html
最后跑学习模块单测 test:learning。

本地默认 VP_BASE=/（根相对）；bundle 预览/部署由 build_pages_bundle 单独构建。
用法：python packages/tooling/src/verify_all.py
"""
import os, sys, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from paths_util import REPO_ROOT, list_apps, app_src, pnpm_cmd


def find_pnpm():
    """返回调用 pnpm 的命令前缀列表（兼容只有 corepack 的机器）。"""
    return pnpm_cmd()


def run(cmd, cwd, env):
    p = subprocess.run(cmd, cwd=cwd, env=env)
    return p.returncode


def main():
    apps = list_apps()
    if 'portal' in apps:
        apps = ['portal'] + [a for a in apps if a != 'portal']

    env = dict(os.environ)
    env['PYTHONUTF8'] = '1'
    env.setdefault('VP_BASE', '/')

    pnpm = find_pnpm()
    failures = []
    summary = []

    for app in apps:
        is_content = os.path.exists(os.path.join(app_src(app), 'SUMMARY.md'))

        print('\n========== verify app=%s（内容 app=%s）==========' % (app, is_content))

        rc = run(pnpm + ['run', 'build:' + app], REPO_ROOT, env)
        if rc != 0:
            failures.append('%s:build' % app)
            continue

        if is_content:
            # 构建内存预算（ADR-0012）：预计超预算就在真正 OOM 之前失败并给处置建议。
            rc = run([sys.executable,
                      os.path.join('packages', 'tooling', 'src', 'build_memory_budget.py'),
                      '--src', app_src(app), '--heap-mb', '8192'], REPO_ROOT, env)
            if rc != 0:
                failures.append('%s:memory-budget' % app)
                continue

            # 数学渲染契约（ADR-0012）：构建产物里必须只有占位、没有构建期 katex，
            # 且客户端渲染器与 katex chunk 都在。这条能拦住"公式悄悄退回构建期渲染"
            # 或"公式在页面上消失"两类回归。
            rc = run([sys.executable,
                      os.path.join('packages', 'tooling', 'src', 'scan_math_render.py'),
                      '--app', app], REPO_ROOT, env)
            if rc != 0:
                failures.append('%s:math-render' % app)
                continue

            # 内容档位与模块（速查/题库目录自动走 quick 口径）
            rc = run([sys.executable, os.path.join('scripts', 'check-content.py'),
                      '--app', app, '--profile', 'all', '--by-dir', '--strict'],
                     REPO_ROOT, env)
            if rc != 0:
                failures.append('%s:content-check' % app)
                continue

            # 旧错误说法回归（报告 0 命中才过；纠错语境已在工具内排除）
            rc = run([sys.executable,
                      os.path.join('packages', 'tooling', 'src', 'scan_legacy_errors.py'),
                      '--app', app, '--strict'], REPO_ROOT, env)
            if rc != 0:
                failures.append('%s:legacy-errors' % app)
                continue

            # 接地符号检查只对电子原理图分册有意义（hardware）；MCU/Linux 的框图、
            # 时序图、状态机本来就没有接地符号，套用只会产生假告警。
            _q = [sys.executable, 'run_quality.py', '--app', app]
            if app != 'hardware':
                _q.append('--skip-grounds')
            rc = run(_q, REPO_ROOT, env)
            if rc != 0:
                failures.append('%s:quality' % app)
                continue

            rc = run([sys.executable,
                      os.path.join('packages', 'tooling', 'src', 'freeze_manifest.py'),
                      '--app', app], REPO_ROOT, env)
            if rc != 0:
                # 退出码 2 = 内容已变更但快照基线未更新（freeze 拒绝静默覆盖基线）。
                # 这是门禁该拦的情况，给出可执行的下一步而不是笼统失败。
                if rc == 2:
                    failures.append('%s:baseline' % app)
                    print('  → 内容已变更但基线未更新；确认改动无误后运行：pnpm freeze:%s' % app)
                else:
                    failures.append('%s:freeze' % app)
                continue

            rc = run([sys.executable,
                      os.path.join('packages', 'tooling', 'src', 'build_single_html.py'),
                      '--app', app,
                      '--manifest', os.path.join('.generated', '%s-content-manifest.json' % app)],
                     REPO_ROOT, env)
            if rc != 0:
                failures.append('%s:offline' % app)
                continue

        summary.append(app)

    print('\n========== 学习模块单测 ==========')
    rc = run(pnpm + ['test:learning'], REPO_ROOT, env)
    if rc != 0:
        failures.append('learning:test')

    print('\n========== verify:all 汇总 ==========')
    print('通过 app: %s' % (', '.join(summary) if summary else '(无)'))
    if failures:
        print('失败项: %s' % ', '.join(failures))
        sys.exit(1)
    print('全部 app 验证通过（构建 + 质检 + 离线 + 学习单测）')


if __name__ == '__main__':
    main()
