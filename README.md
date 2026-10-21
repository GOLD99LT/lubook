# 路书 Lubook · 路先生知识手册

> 一个开源、可交互的个人知识手册合集（pnpm Monorepo）：以**门户**为入口，按领域分册，Markdown 是唯一事实源，在线 VitePress 与离线单文件 HTML 双形态。
>
> 首个分册《硬件工程师手册》从零开始、由浅入深：电路基础 → 元器件 → 模拟电路与运放 → 数字电路 → 单片机硬件 → 电源设计 → PCB/EMC → 测量调试与工程实践，共 140 章，每章含原理图、静态/动态分析、设计示例、常见坑与自测题。

- 门户入口：<https://gold99lt.github.io/lubook/>
- 硬件分册：<https://gold99lt.github.io/lubook/hardware/>
- 国内镜像：<https://lubook.pages.dev/>
- 命名宪法：[`docs/NAMING.md`](docs/NAMING.md) ｜ 架构蓝图：[`ARCHITECTURE.md`](ARCHITECTURE.md) ｜ 操作手册：[`docs/PLAYBOOK.md`](docs/PLAYBOOK.md) ｜ 贡献指南：[`CONTRIBUTING.md`](CONTRIBUTING.md) ｜ 决策记录：[`docs/adr/`](docs/adr/)

## 分册与路线

| 分册 | 内容 | 状态 |
|---|---|---|
| 门户 `portal` | 路书品牌首页 + 分册导航 | 已上线 |
| 硬件工程师手册 `hardware` | 140 章 + 411 张原理图 | 已上线 |
| 嵌入式软件手册 `embedded` | Cortex-M 裸机 / HAL / RTOS | 即将上线（P4 试点） |
| 嵌入式 Linux 手册 `embedded-linux` | Cortex-A / 启动链 / 设备树 / Yocto / OTA | 即将上线（P4 试点） |

硬件分册 140 章分布：电路基础 14 / 元器件 13 / 模拟电路与运放 33 / 数字电路 12 / 单片机 13 / 电源 12 / PCB 13 / 工程实践 12 / 题库 9 / 附录 9。

## 环境要求

- Node 22 + **pnpm 12**（用 corepack 启用，见 [PLAYBOOK](docs/PLAYBOOK.md)）
- Python 3.11+（离线构建与质检，核心脚本仅用标准库）

## 快速开始

```bash
pnpm install
pnpm dev:portal        # 本地开发门户
pnpm dev:hardware      # 本地开发硬件分册（自动生成 sidebar/catalog）
pnpm build:hardware    # 构建硬件分册
pnpm preview:hardware  # 预览构建产物
```

## 多 app 构建与离线单文件

```bash
pnpm bundle:pages      # 组装门户 + 各分册为一个可整体部署目录（VP_BASE=/lubook/）
pnpm verify:all        # 遍历 apps：构建 + 质检 + 离线 + learning 单测
pnpm offline:hardware  # 硬件分册离线单文件 dist/hardware.html（自包含 140 章，按 manifest 对账）
```

## 质量门禁

- `pnpm verify:all`：遍历 `apps/*`，门户构建、内容 app 构建 + run_quality（路由/内容快照 + validate/scan_math/scan_grounds/scan_svg_order）+ 离线对账，最后 learning 单测。
- `pnpm quality:hardware`：仅硬件分册质检。
- 已发布 URL 受 `tests/<app>.routes.snapshot.json` 保护，任何路径变更须先写 ADR。

## 新增一个分册

`templates/site-template` 是与正式 app 同形态的脚手架：复制到 `apps/<app>`，改 appId/标题/篇名，写内容，验证通过后在门户 `apps/portal/content.config.ts` 加卡片。详见 [PLAYBOOK 第 9 节](docs/PLAYBOOK.md)。

## 仓库结构

```
lubook-monorepo/
├── apps/
│   ├── portal/          # 门户：品牌首页 + 分册卡片
│   └── hardware/        # 硬件分册：140 章 Markdown + assets SVG（唯一事实源）
├── packages/
│   ├── shared-config/   # defineBookConfig：通用 markdown/搜索/插件
│   ├── theme/           # 布局、品牌、学习 UI、EChart、图片查看器
│   ├── content-core/    # 内容 manifest 生成（TS，CLI bin book-manifest）
│   ├── learning/        # 学习数据仓储（lubook.v1.<slug>.learning、legacyKeys 迁移）
│   └── tooling/         # Python：bundle 组装/离线构建/质检（零第三方依赖）
├── templates/site-template/  # 新分册脚手架
├── tests/               # hardware 路由/内容指纹快照（CI 基准）
├── docs/                # 活文档：NAMING + PLAYBOOK + ADR
└── .github/workflows/    # quality.yml（多 app 矩阵）、deploy-docs/cloudflare
```

## 部署

- GitHub Pages（主）：`deploy-docs.yml`，推 `main` 用 `bundle:pages`（`VP_BASE=/lubook/`）组装并统一发布；门户在根、分册在 `<slug>/`。
- Cloudflare Pages（镜像，根路径）：`deploy-cloudflare.yml` 用 `bundle:cloudflare`（`VP_BASE=/`），`wrangler pages deploy --project-name=lubook`。
- 自定义域名（`lubook.dev`）列为 backlog，本期不注册。

## License

- 代码与构建工具：[MIT License](LICENSE)
- 文档内容（`apps/hardware/docs/`）：[CC BY-SA 4.0](apps/hardware/docs/LICENSE-docs.md)
