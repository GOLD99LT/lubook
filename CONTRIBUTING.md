# 贡献指南（Contributing）

感谢参与路书 Lubook。本仓库是 **pnpm Monorepo**（门户 + 多领域分册，在线 VitePress + 离线单文件），Markdown 是唯一事实来源。提交前请先读 [`docs/NAMING.md`](docs/NAMING.md)（命名宪法）、[`ARCHITECTURE.md`](ARCHITECTURE.md)（不变量与「不做」清单）与 [`docs/PLAYBOOK.md`](docs/PLAYBOOK.md)（操作手册）。

## 开发环境

- Node 22 + pnpm 12（用 corepack 启用，见 PLAYBOOK）；Python 3.11+（核心脚本仅用标准库）。
- 安装：`pnpm install`（CI 用 `pnpm install --frozen-lockfile`）。
- 常用命令：

```bash
pnpm dev:portal          # 本地开发门户（predev 自动生成）
pnpm dev:hardware        # 本地开发硬件分册
pnpm build:hardware      # 构建硬件分册
pnpm build:template      # 脚手架空 app 也必须能构建
pnpm test:learning       # 学习仓储单测（43 项）
pnpm quality:hardware    # run_quality：manifest 快照 + 五质检
pnpm offline:hardware    # 离线单文件 + manifest 对账
pnpm bundle:pages        # 组装门户+各分册为可整体部署目录
pnpm verify:all          # 遍历 apps 串联以上（提交前必跑）
```

## 内容贡献

1. 在对应篇目录新建/修改 `apps/hardware/docs/<篇>/<id>.md`；
2. 在 `apps/hardware/docs/SUMMARY.md` 的 `## 篇名` 下加一行；
3. frontmatter 至少写 `title / part / chapter / order / tags / difficulty`（id 即相对路径，**不要**手写 id、status、sources，参见 [ADR-0002](docs/adr/ADR-0002.md)）；
4. 原理图放 `apps/hardware/docs/assets/schematics/`，遵循 `packages/tooling/templates/schematic-library.svg`；
5. 写作细则与质检 checklist 见 [`packages/tooling/AGENTS.md`](packages/tooling/AGENTS.md)。

内容语法：行内/块公式 `$...$` / `$$...$$`（KaTeX）；五类容器 `::: motivation/analogy/example/pitfall/advanced`；` ```echarts ` 波形图；`<details>` 折叠题。**不要用 emoji 当图标**（图标用内联 SVG）。

## 提交前必查（PR checklist）

- [ ] `pnpm verify:all` 全绿（各 app 构建 + run_quality + 离线对账 + learning 单测）。
- [ ] 改了内容后：`tests/<app>.routes.snapshot.json` 与 `tests/<app>.manifest.snapshot.json` 比对仍为零差异；若确为有意变更，按下面「破坏性变更」流程处理。
- [ ] 门户/首页/代表章桌面/移动截图无 console 错误、无横向溢出（截图方法见 PLAYBOOK）。
- [ ] 改了共享包，所有 app 与 `templates/site-template` 都仍能构建。
- [ ] 内容遵循「数据可追溯、不整段搬运来源」，版权红线见 tooling/AGENTS.md。

## 破坏性变更与 ADR 触发规则

以下变更**必须先写 ADR**（追加到 `docs/adr/`，流程见 [ADR 索引](docs/adr/README.md)），并在 PR 描述里说明：

1. **URL / 内容 id**：移动或重命名章节、改 clean URL、改 SUMMARY 装配规则（会改变路由快照）。
2. **数据格式**：localStorage 键（`lubook.v1.<slug>.learning`）、manifest/导出 schema、学习数据迁移规则（见 [ADR-0003](docs/adr/ADR-0003.md)、[ADR-0006](docs/adr/ADR-0006.md)）。
3. **不可逆依赖**：新增运行时依赖、锁定版本、引入第三方服务或外部资源。
4. **构建与部署拓扑**：改 pnpm workspace、构建命令、`VP_BASE`/base 策略、CI/CD、发布流程。
5. **安全、版权、内容许可**相关。

此外，**改架构 / 构建 / 共享组件 / 部署**时，必须在同一改动里同步更新文档或补 ADR。

确需更新路由/内容快照时：本地重新生成 `tests/<app>.*.snapshot.json`，在 PR 中逐条列出 URL/指纹变化及其原因（URL 变化须 ADR）；不得在未说明的情况下直接覆盖快照。

## 不做（避免过度工程）

不把 Python 离线/质检重写为 Node；不为重构而批量回填已有章节（新章须按 ADR-0008 写全 frontmatter）；不引入 IndexedDB；不建审核状态机/CODEOWNERS；不做 embedded/embedded-linux 实际内容、门户增强/仿真/题库/计算器/Giscus/PWA/云同步（这些按 ARCHITECTURE §14 与 REQUIREMENTS 附录 A 立项后再做）。

## 许可证

- 代码与构建工具：MIT（`LICENSE`）。
- 文档内容：CC BY-SA 4.0（`apps/hardware/docs/LICENSE-docs.md`）。提交内容即表示同意按对应许可证发布。
