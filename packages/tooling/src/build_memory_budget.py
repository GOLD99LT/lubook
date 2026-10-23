#!/usr/bin/env python3
"""构建内存预算检查。

背景见 docs/adr/ADR-0011.md：VitePress 单站构建的内存峰值随**页面数**线性增长，
内容涨到某个点就会 OOM。本脚本把这个关系固化成可检查的预算，
把"构建偶发 OOM"变成"构建前就知道够不够"。

实测基准（2026-10-23，vitepress 1.6.4，Node 24，硬件分册）：

数学渲染策略切换前后各测两点（见 ADR-0012）：

| 配置                        | 页面数 | 峰值内存 | 耗时  |
|-----------------------------|-------:|---------:|------:|
| 构建期 KaTeX，全站          |    144 | 5.94 GB  | 110 s |
| 构建期 KaTeX，仅 basics 篇  |     18 | 1.76 GB  |  35 s |
| **运行期 KaTeX，全站**      |    144 | **2.30 GB** | **45 s** |
| **运行期 KaTeX，仅 basics** |     18 | **0.99 GB** | **22 s** |

线性拟合（当前策略 = 运行期渲染）：**峰值 ≈ 0.80 GB + 10.4 MB × 页面数**

用法：
    python packages/tooling/src/build_memory_budget.py --src apps/hardware/docs
    python packages/tooling/src/build_memory_budget.py --src apps/hardware/docs --heap-mb 8192
    python packages/tooling/src/build_memory_budget.py --src apps/hardware/docs --json

退出码：
    0 = 预算内
    1 = 预计超预算（应在本机/CI OOM 之前就介入）
"""

from __future__ import annotations

import argparse
import json
import os
import sys

# ---- 实测模型（改动前请先重新测量并更新本文件与 ADR-0012）----
# 注：这两个常数对"数学渲染策略"敏感。构建期渲染 KaTeX 时是 1.16 GB + 33 MB/页，
# 运行期渲染后降到 0.80 GB + 10.4 MB/页。换策略必须重测。
BASE_GB = 0.80
GB_PER_PAGE = 0.0104
# 建议的安全系数：峰值不要贴着堆上限，GC 在临界区会抖动
SAFETY = 0.9
# 超过多少比例时提示"该考虑拆站"（相对堆上限）
SPLIT_HINT = 0.85


def count_pages(src: str) -> tuple[int, list[str]]:
    """统计会变成路由的 Markdown 页面，并返回按体积排序的最大页面。"""
    pages = []
    for root, _dirs, files in os.walk(src):
        for name in files:
            if not name.endswith(".md"):
                continue
            path = os.path.join(root, name)
            pages.append((os.path.getsize(path), os.path.relpath(path, src)))
    pages.sort(reverse=True)
    # VitePress 还会额外产出 404 页；实测 dist 的 html 数比 md 数多 1。
    return len(pages) + 1, [p[1] for p in pages[:5]]


def main() -> int:
    parser = argparse.ArgumentParser(description="VitePress 构建内存预算检查")
    parser.add_argument("--src", required=True, help="文档源目录，如 apps/hardware/docs")
    parser.add_argument("--heap-mb", type=int, default=8192, help="构建时分配的堆上限（MB）")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    args = parser.parse_args()

    pages, largest = count_pages(args.src)
    estimate_gb = BASE_GB + GB_PER_PAGE * pages
    heap_gb = args.heap_mb / 1024.0
    usable_gb = heap_gb * SAFETY
    ratio = estimate_gb / heap_gb if heap_gb else 0.0
    over = estimate_gb > usable_gb
    split_needed = ratio >= SPLIT_HINT
    # 反解：在给定堆上限下，最多能撑多少页
    max_pages = int((usable_gb - BASE_GB) / GB_PER_PAGE)

    report = {
        "src": args.src,
        "pages": pages,
        "estimateGb": round(estimate_gb, 2),
        "heapMb": args.heap_mb,
        "heapGb": round(heap_gb, 2),
        "usableGb": round(usable_gb, 2),
        "usageRatio": round(ratio, 3),
        "maxPagesForHeap": max_pages,
        "headroomPages": max_pages - pages,
        "overBudget": over,
        "splitRecommended": split_needed,
        "largestPages": largest,
        "model": f"峰值 ≈ {BASE_GB} GB + {GB_PER_PAGE * 1024:.0f} MB × 页面数",
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1 if over else 0

    print("==== 构建内存预算 ====")
    print("模型: %s" % report["model"])
    print("页面数: %d（含 404 页）" % pages)
    print("预计峰值: %.2f GB" % estimate_gb)
    print("堆上限: %.2f GB（可用 %.2f GB，留 10%% 安全余量）" % (heap_gb, usable_gb))
    print("占用率: %.0f%%" % (ratio * 100))
    print("此堆在上限内最多可撑: %d 页（当前 %d 页，余量 %d 页）"
          % (max_pages, pages, report["headroomPages"]))
    print("最大的页面: %s" % ", ".join(largest))

    if over:
        print()
        print("!! 预计超出预算：构建很可能 OOM。可选处置（按代价从低到高）：")
        print("   1) 抬高堆上限（--heap-mb / ADR-0011），确认机器与 CI runner 物理内存够；")
        print("   2) 把数学渲染换成运行期（ADR-0012）：本仓已默认如此，约占原峰值 60%；")
        print("   3) 拆站：按篇分成多个 VitePress 构建，峰值约降到"
              " %.2f + %.4f×每站页数 GB。" % (BASE_GB, GB_PER_PAGE))
        return 1

    if split_needed:
        print()
        print("! 已用掉 %.0f%% 预算，接近天花板：建议现在就开始评估拆站方案。" % (ratio * 100))
    else:
        print()
        print("预算充足。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
