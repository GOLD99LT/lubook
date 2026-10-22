# AGENTS.md — 路书 Lubook 智能体协作规范（根）

本文件是所有 AI 智能体在本仓库工作的**根规范**。命名宪法见 [`docs/NAMING.md`](docs/NAMING.md)；内容生产细则见 [`packages/tooling/AGENTS.md`](packages/tooling/AGENTS.md)；操作步骤见 [`docs/PLAYBOOK.md`](docs/PLAYBOOK.md)；权威蓝图是 [`ARCHITECTURE.md`](ARCHITECTURE.md)。

## 1. 工程是什么

「路书 Lubook」是作者路先生的开源个人知识手册合集，**pnpm Monorepo**：`apps/portal` 是占根的极简门户（品牌首页 + 分册卡片）；`apps/hardware` 是 140 章的硬件工程师手册；`packages/*` 提供共享配置/主题/内容内核/学习仓储；`packages/tooling` 是 Python 离线构建、质检与 bundle 组装；`templates/site-template` 是新分册脚手架。两种交付形态长期并存：在线 VitePress 与离线单文件 HTML，共用同一份 Markdown。

## 2. 不可违反的不变量（违反即返工）

1. **Markdown 是唯一事实源**；内容文件只 `git mv`，Git 对内容仅见 rename，不改写 140 章正文与 411 SVG。
2. **现有线上 URL 永不变**；路由快照（`tests/<app>.routes.snapshot.json`）必须零差异，任何 URL 变更先写 ADR。
3. **不把 Python 离线/质检重写为 Node**；离线构建保持零第三方依赖。
4. **不回填** 已有章节（不为重构而批量改写正文/frontmatter）；但**新章必须写全** `id/status/sources` 等字段（ADR-0008）。不引入 IndexedDB；不建审核状态机/CODEOWNERS。
5. 不做 embedded/embedded-linux 实际内容、门户增强/仿真/题库/计算器/Giscus/PWA/云同步/后端/英文版（P4/P5 立项后再说）。
6. 不部署、不合并 main、不 push、不改 GitHub 仓库设置、不碰 Cloudflare 项目、不买域名，除非用户明确授权。
7. pnpm 无法启用时**停下反馈**，禁止擅自降级或换 npm/yarn。

## 3. 常用命令

```bash
pnpm install                         # 安装/链接全部 workspace
pnpm dev:portal                      # 开发门户
pnpm dev:hardware                    # 开发硬件分册
pnpm build:hardware                  # 构建硬件分册
pnpm bundle:pages                    # 组装门户+各分册为可整体部署目录
pnpm verify:all                      # 遍历 apps：构建/质检/离线 + learning 单测
pnpm quality:hardware                # 硬件分册质检（manifest 快照 + validate/scan_*）
```

## 4. 交接与验证

- 智能体之间以**文件系统**交接，不依赖对话上下文。
- 产出后必须自证：构建退出码、`run_quality` 各项数字、快照 diff、（必要时）截图结论，而不是「我看着没问题」。
- 新增生成物要确认已被 `.gitignore` 忽略（`.generated/`、`**/.vitepress/{cache,dist}`、`*.generated.mjs`、`docs/public`、`dist/`、`.shots/`、`.bundle/`）。

## 5. ADR 触发规则

改架构/构建/共享组件/部署必须在**同一改动**更新文档或补 ADR；下列事项必须先写 ADR：不可逆依赖、数据格式（localStorage/manifest/导出）、URL 与内容 id、部署拓扑、第三方服务、安全与版权。ADR 只追加，见 [`docs/adr/README.md`](docs/adr/README.md)。

## 6. 内容写作要点

每章 frontmatter：`title/part/chapter/order/tags/difficulty`；五类容器、KaTeX、ECharts、`<details>` 折叠题；图标用内联 SVG，不用 emoji；公式给结论并解释符号。完整 checklist 与版权红线见 [`packages/tooling/AGENTS.md`](packages/tooling/AGENTS.md)。
