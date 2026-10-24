#!/usr/bin/env python3
"""把 docs 下所有章节自动同步进 SUMMARY.md（按目录定篇、按 frontmatter order 排序）。

为什么不手工加行：内容分多批、多智能体并行产出，手工登记必然出现
"磁盘有但 SUMMARY 未登记"（构建直接失败）或顺序错位（章节编号全乱）。
本工具一次扫描全目录，重建每篇的条目块，保证：

- 每篇的条目 = 该篇目录下所有 .md，按 frontmatter 的 `order` 升序；
- 幂等：重复运行不产生重复行；
- 不动篇标题与其它非条目文字。

篇号来自 content.config.ts 的 PART_REGISTRY？那里只有篇名没有目录。
因此用 DIR_PART 映射（每个 app 一张表），未列出的目录跳过并提示。

用法：
    python packages/tooling/src/sync_summary.py --app embedded --dry-run
    python packages/tooling/src/sync_summary.py --app embedded
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

# 目录 -> 篇号。新分册按自己的篇结构登记在这里。
DIR_PART = {
    "embedded": {"basics": 1, "mcu": 2, "comm": 3, "rtos": 4, "storage": 5, "practice": 6},
    "embedded-linux": {"basics": 1, "kernel": 2, "userspace": 3,
                       "hardware": 4, "reliability": 5, "practice": 6},
}


def meta(path):
    t = io.open(path, encoding="utf-8").read()
    title = re.search(r"(?m)^title:\s*(.+)$", t)
    order = re.search(r"(?m)^order:\s*(\d+)\s*$", t)
    return (title.group(1).strip().strip('"\'') if title else os.path.basename(path)[:-3],
            int(order.group(1)) if order else 10 ** 6)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    docs = os.path.join(ROOT, "apps", args.app, "docs")
    summary_path = os.path.join(docs, "SUMMARY.md")
    mapping = DIR_PART.get(args.app)
    if not mapping:
        print("没有为 %s 配置目录→篇号映射，请先加 DIR_PART" % args.app)
        return 1

    # 收集章节
    by_part = {}
    unknown = []
    for dirpath, _d, files in os.walk(docs):
        if ".vitepress" in dirpath or os.sep + "assets" in dirpath:
            continue
        for name in sorted(files):
            if not name.endswith(".md") or name in ("index.md", "SUMMARY.md"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), docs).replace(os.sep, "/")
            top = rel.split("/")[0]
            if top not in mapping:
                unknown.append(rel)
                continue
            by_part.setdefault(mapping[top], []).append((rel, os.path.join(dirpath, name)))

    lines = io.open(summary_path, encoding="utf-8").read().splitlines()
    part_idx = [i for i, ln in enumerate(lines) if ln.startswith("## ")]
    if len(part_idx) < max(by_part or {1: 1}):
        print("SUMMARY 篇数不足：只有 %d 篇" % len(part_idx))
        return 1

    # 自底向上重建，避免行号漂移
    total = 0
    for part in sorted(by_part, reverse=True):
        start = part_idx[part - 1]
        end = part_idx[part] if part < len(part_idx) else len(lines)
        block = lines[start:end]
        # 保留篇标题与其后到第一个条目前的说明行
        head = []
        for ln in block:
            if ln.startswith("* ["):
                break
            head.append(ln)
        while head and head[-1].strip() == "":
            head.pop()

        entries = []
        for rel, fp in by_part[part]:
            title, order = meta(fp)
            entries.append((order, rel, "* [%s](%s)" % (title, rel)))
        entries.sort(key=lambda x: (x[0], x[1]))

        new_block = head + [""] + [e[2] for e in entries] + [""]
        lines[start:end] = new_block
        total += len(entries)
        print("第 %d 篇：%d 章" % (part, len(entries)))

    if unknown:
        print("未映射目录（未处理）: %s" % ", ".join(unknown))
    print("合计 %d 章" % total)

    if args.dry_run:
        print("（dry-run，未写文件）")
        return 0

    io.open(summary_path, "w", encoding="utf-8", newline="\n").write("\n".join(lines).strip() + "\n")
    print("已写入 %s" % summary_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
