#!/usr/bin/env python3
"""把章节登记进 docs/SUMMARY.md（幂等）。

为什么需要：SUMMARY 决定页面顺序、章节编号与 sidebar。手工在长文件里插行容易
插错篇、漏登记（构建会报"磁盘有但 SUMMARY 未登记"）或重复登记。
本工具按篇定位、按相对路径去重，重复执行不会产生重复行。

用法：
    # 追加到第 2 篇末尾（标题用 frontmatter 的 title 或显式给）
    python packages/tooling/src/update_summary.py --app embedded --part 2 \
        --entries "mcu/cortex-m-arch.md,mcu/clock-tree.md,mcu/gpio.md"

    # 不带标题时自动读该章 frontmatter 的 title
    python packages/tooling/src/update_summary.py --app embedded --part 1 --entries "basics/startup-boot.md"

    # 只看会改成什么，不写文件
    python packages/tooling/src/update_summary.py --app embedded --part 2 --entries "..." --dry-run

退出码：0 成功（含"已存在，未改动"）；1 找不到篇或文件。
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def chapter_title(path: str) -> str:
    try:
        text = io.open(path, encoding="utf-8").read()
    except OSError:
        return ""
    m = re.search(r"(?m)^title:\s*(.+)$", text)
    return m.group(1).strip().strip('"\'') if m else ""


def chapter_meta(path: str):
    """返回 (title, order)。order 缺失时给一个很大的数，排到后面。"""
    try:
        text = io.open(path, encoding="utf-8").read()
    except OSError:
        return "", 10**6
    t = re.search(r"(?m)^title:\s*(.+)$", text)
    o = re.search(r"(?m)^order:\s*(\d+)\s*$", text)
    return (t.group(1).strip().strip('"\'') if t else "",
            int(o.group(1)) if o else 10**6)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", required=True)
    ap.add_argument("--part", type=int, required=True, help="第几篇（1 起）")
    ap.add_argument("--entries", required=True, help="相对 docs 的 md 路径，逗号分隔")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    docs = os.path.join(ROOT, "apps", args.app, "docs")
    summary_path = os.path.join(docs, "SUMMARY.md")
    if not os.path.exists(summary_path):
        print("找不到 SUMMARY: %s" % summary_path)
        return 1

    text = io.open(summary_path, encoding="utf-8").read()
    lines = text.splitlines()

    # 找篇标题行：按出现顺序数 `## ` 开头的行
    part_starts = [i for i, ln in enumerate(lines) if ln.startswith("## ")]
    if args.part < 1 or args.part > len(part_starts):
        print("篇号越界：%d（SUMMARY 只有 %d 篇）" % (args.part, len(part_starts)))
        return 1
    start = part_starts[args.part - 1]
    end = part_starts[args.part] if args.part < len(part_starts) else len(lines)

    block = lines[start:end]
    existing = "\n".join(block)

    added = []
    for rel in [e.strip() for e in args.entries.split(",") if e.strip()]:
        if rel in existing:
            continue
        fp = os.path.join(docs, rel.replace("/", os.sep))
        if not os.path.exists(fp):
            print("章节文件不存在，跳过: %s" % rel)
            continue
        title, order = chapter_meta(fp)
        added.append((order, rel, "* [%s](%s)" % (title or os.path.splitext(os.path.basename(rel))[0], rel)))

    if not added:
        print("没有需要新增的条目（都已登记）。")
        return 0

    # 有序装配：把本篇已有条目与新增条目一起按 frontmatter 的 order 排序。
    # 这样无论批次先后、谁先写完，最终顺序都等于设计顺序（order = 篇内排序）。
    entries = []   # (order, 原索引, 行)
    for i, ln in enumerate(block):
        m = re.search(r"\]\(([^)]+)\)", ln)
        if not ln.startswith("* [") or not m:
            continue
        rel = m.group(1)
        _, order = chapter_meta(os.path.join(docs, rel.replace("/", os.sep)))
        entries.append((order, i, ln))

    for order, rel, line in added:
        entries.append((order, 10 ** 6, line))   # 新增条目置于同级末尾，稳定排序保留顺序

    entries.sort(key=lambda x: (x[0], x[1]))

    # 重建本节：标题行 + 空行 + 排序后的条目（节内其它非条目的文字保持不动）
    head = []
    for ln in block:
        if ln.startswith("* ["):
            break
        head.append(ln)
    while head and head[-1] == "":
        head.pop()

    new_block = head + [""] + [e[2] for e in entries] + [""]
    new_lines = lines[:start] + new_block + lines[end:]

    print("将新增 %d 条到第 %d 篇（%s），并按 order 排序：" % (len(added), args.part, lines[start]))
    for _o, rel, _l in added:
        print("  + " + rel)

    if args.dry_run:
        print("（dry-run，未写文件）")
        return 0

    io.open(summary_path, "w", encoding="utf-8", newline="\n").write("\n".join(new_lines) + "\n")
    print("已写入 %s（本篇共 %d 条）" % (summary_path, len(entries)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
