# AGENTS.md — 智能体协作任务书

本文件是路书 Lubook 工程中所有 AI 智能体的工作规范。新增篇章、新增 Agent 时在此追加，不改动既有条目。

> Monorepo 总规范见根 [`../../AGENTS.md`](../../AGENTS.md)，操作步骤见 [`../../docs/PLAYBOOK.md`](../../docs/PLAYBOOK.md)；本文件聚焦「内容写作与质检」。

## 1. 工程概述

- 目标：生产路书各分册（Markdown 为唯一事实来源），可构建为单文件 HTML、可发布为网站，门户统一聚合。
- 内容按各分册 `apps/<app>/docs/SUMMARY.md` 装配；章节文件分布在 `apps/<app>/docs/<篇>/`。
- Agent 之间通过**文件系统**交接，不依赖对话上下文。

## 2. 文件与命名约定

- 每章一个 Markdown 文件，文件名 = 语义 id（小写英文、连字符），如 `inverting-amplifier.md`。
- **章节 id 即相对路径**（如 `opamp/inverting-amplifier.md`），frontmatter 不再手写 `id`，也不回填 `status/sources`（见 ADR-0002）。
- 原理图放 `apps/<app>/docs/assets/schematics/<id>.svg`；风格遵循 `packages/tooling/templates/schematic-library.svg`。
- 稳定路径一旦发布不可更改（改路径=URL 变更，须 ADR）；显示编号由构建时按 SUMMARY 顺序生成，正文中禁止手写"第 N 章"。
- 交叉引用链接相对路径文件，如 `[反相放大器](../opamp/inverting-amplifier.md)`。

## 3. Frontmatter 规范

```yaml
title: 反相比例放大器         # 必填
part: 3                      # 必填 1-10（对应 content.config 的 PART_REGISTRY）
chapter: 运放应用电路          # 可空
order: 45                    # 必填，篇内排序，间隔取 5
tags: [运放, 反相放大]         # 必填，至少1个
difficulty: 2                # 必填 1入门/2进阶/3深入
# 不写 id（=相对路径）；status / sources 本期不要求、不回填（ARCHITECTURE §14）
```

## 4. Markdown 扩展语法（构建脚本支持）

- 行内公式 `$V=IR$`；块公式 `$$...$$`（KaTeX）
- 自定义容器（开始行 `::: 类型 标题`，结束行 `:::`）：
  - `motivation` 设计动机（橙）
  - `analogy` 直觉类比（蓝）
  - `example` 设计示例（绿）
  - `pitfall` 常见坑（红）
  - `advanced` 进阶内容（默认折叠，小白可跳过）
- 波形图：```` ```echarts ```` 代码块，内容为 ECharts option JSON
- 原理图：`![](../assets/schematics/xxx.svg)`（构建时内联），或 ```` ```svg ```` 代码块
- 自测题：`<details><summary>问题</summary>答案</details>`
- 表格：标准 GFM 表格，列多时用表格块呈现

## 5. Agent 角色

### 调研 Agents（资料采集）

| Agent | 范围 | 输出 |
|---|---|---|
| Research-A | 模电/运放/元器件 | 追加 `sources.list.yaml`；资料克隆到 `sources/`；写 `sources/index-a.md` |
| Research-B | 电源/PCB/EMC | 同上 `sources/index-b.md` |
| Research-C | 数电/单片机/工程实践 | 同上 `sources/index-c.md` |

调研产出每条包含：名称、URL、类型（仓库/官方笔记/视频/书籍）、star/活跃度、License、质量评级 A/B/C、对应章节 id、一句话内容摘要。

仓库筛选：star 较高或内容成体系、近 2 年有更新（经典老资料除外）、许可可参考、非纯碎片。

### 写作 Agents（每篇一个，可并行）

- 输入：`apps/<app>/docs/SUMMARY.md` 中该篇条目、`packages/tooling/templates/chapter.md`、`sources/` 中相关资料、本规范。
- 输出：该篇所有 Markdown 文件 + 原理图 SVG，写入对应 `apps/<app>/docs/<篇>/`。
- 单个 Agent 负责不超过 15 章；超过则拆分为多个 Agent（如 part3 可拆为 core/circuits 两个）。
- 每章必须完成模板的 11 个模块；基础层与 `::: advanced` 分层。
- 电路章必须含：原理图、静态分析、动态分析（含波形）、环路分析（结论+进阶推导）、取值计算、设计示例、坑、自测题、来源。

### 质检构建 Agent

1. 运行 `python packages/tooling/src/validate.py`：frontmatter 完整性、SUMMARY 与文件一致性、图片存在、死链、id 唯一性；
2. 运行 `python packages/tooling/src/build_single_html.py` 构建；
3. 截图核对（桌面 1440 宽）：目录、块样式、图表渲染、无控制台错误；
4. 产出问题清单（定位到文件与章节），打回对应写作 Agent。

## 6. 质量 Checklist（写作 Agent 自检）

- [ ] 每个数字、公式、结论有来源，可追溯
- [ ] 公式给结论并解释每个符号；推导放 `advanced`
- [ ] 至少一张原理图；元件标号、节点、电流方向清晰
- [ ] 关键动态结论配波形/频响图
- [ ] 电阻等元件给出取值数量级与权衡，而非只写"取 10k"
- [ ] 设计示例从需求到验算完整走一遍
- [ ] 至少 2 条常见坑（现象→原因→解决）
- [ ] 至少 2 道自测题，答案折叠
- [ ] 术语首次出现给中英对照
- [ ] 无原文复制；内容为自己的结构与表述

## 7. 版权红线

- 禁止整段搬运任何来源（包括 GitHub 仓库、数据手册正文、博客）。
- 做法：读懂 → 用本手册结构和语言重写 → frontmatter `sources` 注明。
- 厂商商标、芯片型号归各自所有者；引用数据手册参数时注明编号。
- 文档 CC BY-SA 4.0，提交即表示同意该协议。
