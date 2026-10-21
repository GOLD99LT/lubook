#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_quality.py — 多 app 统一质量门禁（ADR-0006 起按分册参数化；纯 Python 标准库）。

用法：
  python run_quality.py --app hardware
  python run_quality.py --app hardware --src apps/hardware/docs --snapshot-prefix hardware

固定顺序（每个内容分册）：
  1. manifest 一致性与快照门禁
     SUMMARY↔磁盘双向对齐、id/url 唯一、计数对齐，
     并与入库的 tests/<app>.routes.snapshot.json、tests/<app>.manifest.snapshot.json 逐字比对
     （删除/变更即失败——URL 破坏性变更须人工批准并更新快照）。
  2. packages/tooling/src/validate.py       frontmatter/死链/echarts/配对/结构（退出码门禁）
  3. packages/tooling/src/scan_grounds.py   接地符号：总数对齐基线且无「过短/递减不匀」告警
  4. packages/tooling/src/scan_svg_order.py SVG 根 <svg> 位置：broken 必须为 0
  5. packages/tooling/src/scan_math.py      公式字符：需修正处数必须为 0

门户 apps/portal 无 SUMMARY/内容 manifest：自动跳过内容类检查（仅保留构建期校验）。
任一失败 → 非零退出码。
"""
import os, re, sys, json, argparse, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(ROOT, 'packages', 'tooling', 'src')
sys.path.insert(0, TOOLS)

from paths_util import add_common_args, resolve_src

FAILURES = []


def step(name, ok, detail=''):
    print('[%s] %s %s' % ('PASS' if ok else 'FAIL', name, detail))
    if not ok:
        FAILURES.append(name)


def run_tool(script, app, src):
    env = dict(os.environ)
    env['PYTHONUTF8'] = '1'
    p = subprocess.run([sys.executable, os.path.join(TOOLS, script),
                        '--app', app, '--src', src],
                       capture_output=True, env=env, cwd=ROOT)
    out = (p.stdout or b'').decode('utf-8', 'replace')
    err = (p.stderr or b'').decode('utf-8', 'replace')
    return p.returncode, out, err


def check_manifest(app, src, prefix):
    import freeze_manifest as F
    try:
        manifest, routes, fp = F.build_manifest(app, src)
        built = True
    except SystemExit:
        built = False
        manifest = routes = fp = None
    step('manifest/consistency (SUMMARY<->磁盘, id/url 唯一)', built)
    if not built:
        return None

    snap_routes = json.load(open(os.path.join(ROOT, 'tests', '%s.routes.snapshot.json' % prefix),
                                 encoding='utf-8'))
    snap_fp = json.load(open(os.path.join(ROOT, 'tests', '%s.manifest.snapshot.json' % prefix),
                             encoding='utf-8'))
    step('manifest/routes snapshot 比对', snap_routes == routes,
         '(stored=%d live=%d)' % (len(snap_routes), len(routes)))
    step('manifest/fingerprint 比对', snap_fp == fp,
         '(stored=%s / live=%s)' % (
             json.dumps(snap_fp, sort_keys=True, ensure_ascii=False),
             json.dumps(fp, sort_keys=True, ensure_ascii=False)))
    ids = [d['id'] for d in manifest['docs']]
    urls = [d['url'] for d in manifest['docs']]
    step('manifest/id 唯一', len(ids) == len(set(ids)))
    step('manifest/url 唯一', len(urls) == len(set(urls)))
    step('manifest/计数对齐',
         manifest['appId'] == app and fp['docCount'] == len(ids)
         and fp['imageTotal'] == sum(len(d['images']) for d in manifest['docs'])
         and len(routes) == len(ids) + 1)
    return fp


def main():
    ap = add_common_args()
    ap.add_argument('--snapshot-prefix', default=None,
                    help='快照文件名前缀（默认 = --app）')
    args = ap.parse_args()

    app = args.app
    src = resolve_src(args)
    prefix = args.snapshot_prefix or app

    is_content = os.path.exists(os.path.join(src, 'SUMMARY.md'))
    print('=== run_quality: app=%s src=%s 快照前缀=%s（内容 app=%s）==='
          % (app, src, prefix, is_content))

    fp = None
    if is_content:
        print('\n==== 1/5 manifest 一致性与快照门禁 ====')
        fp = check_manifest(app, src, prefix)

        print('\n==== 2/5 validate.py ====')
        rc, out, err = run_tool('validate.py', app, src)
        print(out)
        if err.strip():
            print(err)
        step('validate.py (退出码门禁)', rc == 0, '(exit %d)' % rc)

        print('\n==== 3/5 scan_grounds.py ====')
        rc, out, err = run_tool('scan_grounds.py', app, src)
        m = re.search(r'共识别接地符号\s*(\d+)\s*个', out)
        grounds = int(m.group(1)) if m else -1
        flagged = ('最下线过短' in out) or ('递减不匀' in out)
        expect = fp['groundsCount'] if fp else -1
        step('scan_grounds.py (数量对齐基线且无告警)',
             grounds == expect and not flagged,
             '(grounds=%d expect=%d, flagged=%s)' % (grounds, expect, flagged))

        print('\n==== 4/5 scan_svg_order.py ====')
        rc, out, err = run_tool('scan_svg_order.py', app, src)
        m = re.search(r'BROKEN[^\d]*(\d+)', out)
        broken = int(m.group(1)) if m else -1
        step('scan_svg_order.py (broken 必须为 0)', broken == 0, '(broken=%d)' % broken)

        print('\n==== 5/5 scan_math.py ====')
        rc, out, err = run_tool('scan_math.py', app, src)
        m = re.search(r'(\d+)\s*处公式需修正', out)
        issues = int(m.group(1)) if m else -1
        step('scan_math.py (issues 必须为 0)', issues == 0, '(issues=%d)' % issues)
    else:
        print('\n门户/非内容 app：跳过内容 manifest/validate/scan 检查（由构建 + 截图兜底）')

    print('\n==== run_quality 结果: %d 项失败 ====' % len(FAILURES))
    if FAILURES:
        for f in FAILURES:
            print('  [FAIL] ' + f)
    sys.exit(1 if FAILURES else 0)


if __name__ == '__main__':
    main()
