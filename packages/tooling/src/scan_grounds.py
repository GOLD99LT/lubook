# -*- coding: utf-8 -*-
"""扫描所有原理图 SVG 中的接地符号（三条居中、长度递减的水平横线），
报告位置与尺寸，用于统一规范化。参数化：--src 指定内容源（默认 <repo>/docs）。"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths_util import add_common_args, resolve_src
_args, _ = add_common_args().parse_known_args()
SDIR = os.path.join(resolve_src(_args), 'assets', 'schematics')

LINE = re.compile(r'<line\b[^>]*x1="([\d.]+)"[^>]*y1="([\d.]+)"[^>]*x2="([\d.]+)"[^>]*y2="([\d.]+)"[^>]*/?>')

def horizontals(svg):
    hs = []
    for m in LINE.finditer(svg):
        x1, y1, x2, y2 = map(float, m.groups())
        if abs(y1 - y2) < 0.1:
            cx = (x1 + x2) / 2
            length = abs(x2 - x1)
            hs.append((cx, y1, length, min(x1, x2), max(x1, x2)))
    return hs

def find_grounds(hs):
    grounds = []
    used = set()
    for i, a in enumerate(hs):
        for j, b in enumerate(hs):
            if j == i: continue
            for k, c in enumerate(hs):
                if k in (i, j): continue
                trio = sorted([a, b, c], key=lambda t: t[1])
                t1, t2, t3 = trio
        # 上面循环无意义，改为下方显式判定
    # 显式：按 y 排序后滑窗
    hss = sorted(hs, key=lambda t: (round(t[0]/4), t[1]))
    n = len(hss)
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                t1, t2, t3 = hss[i], hss[j], hss[k]
                if abs(t1[0]-t2[0]) <= 3 and abs(t2[0]-t3[0]) <= 3:
                    d12, d23 = t2[1]-t1[1], t3[1]-t2[1]
                    if 3 <= d12 <= 14 and 3 <= d23 <= 14 and abs(d12-d23) <= 5:
                        if t1[2] > t2[2] > t3[2] and t1[2] >= 12:
                            key = (round(t1[0]), round(t1[1]))
                            if key not in used:
                                used.add(key)
                                grounds.append((t1, t2, t3))
    return grounds

total = 0
for f in sorted(os.listdir(SDIR)):
    if not f.endswith('.svg'):
        continue
    svg = open(os.path.join(SDIR, f), encoding='utf-8').read()
    gs = find_grounds(horizontals(svg))
    if not gs:
        print('%-40s 无接地' % f)
        continue
    for t1, t2, t3 in gs:
        total += 1
        cx = round(t1[0])
        lens = (round(t1[2]), round(t2[2]), round(t3[2]))
        gap = (round(t2[1]-t1[1]), round(t3[1]-t2[1]))
        flag = ''
        if t3[2] < 9: flag += ' 最下线过短'
        if lens[0]-lens[1] < 4 or lens[1]-lens[2] < 3: flag += ' 递减不匀'
        print('%-40s cx=%s topY=%s 长度=%s 间距=%s%s' %
              (f, cx, round(t1[1]), lens, gap, flag))
print('\n==== 共识别接地符号 %d 个 ====' % total)
