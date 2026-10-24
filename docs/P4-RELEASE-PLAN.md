# P4 上线预案（embedded / embedded-linux）

> 状态：**待用户确认**。本文只描述"确认后要做什么"，不含已执行动作。
> 依据：`docs/DEVELOPMENT-STANDARD.md` §6/§8、ADR-0014（P4 立项）、ADR-0013（双站拓扑）。

## 1. 交付物清单

| 分册 | 目录 | 路由前缀 | 篇数 | 内容 |
|---|---|---|---|---|
| 嵌入式软件手册（MCU） | `apps/embedded` | `/lubook/embedded/`（镜像 `/embedded/`） | 6 | 见 `docs/SUMMARY.md` |
| 嵌入式 Linux 手册 | `apps/embedded-linux` | `/lubook/embedded-linux/`（镜像 `/embedded-linux/`） | 6 | 见 `docs/SUMMARY.md` |

两个分册共用既有工程形态（shared-config / theme / content-core / learning），
**没有新增运行时依赖、没有新增第三方服务**。

## 2. 上线前必须全绿的验收项

| # | 项 | 命令 | 判据 |
|---|---|---|---|
| 1 | 内容门禁 | `pnpm verify:all` | 退出 0；`embedded/embedded-linux` 的 quality 0 失败 |
| 2 | 路由基线 | `git diff tests/*.routes.snapshot.json` | 新分册快照为**新增**，hardware 快照零差异 |
| 3 | 构建 | `pnpm build:embedded && pnpm build:embedded-linux` | 退出 0 |
| 4 | 离线单文件 | `pnpm offline:embedded && pnpm offline:embedded-linux` | 产物生成、manifest 对账一致 |
| 5 | 渲染抽验 | 本地起服务 + headless 浏览器 | KaTeX 错误 0、图表渲染、无空白页 |
| 6 | 门户链接 | 本地构建 portal | 卡片链接指向正确 slug |

## 3. 上线动作（按顺序，每步可回滚）

1. **门户卡片开关**：`apps/portal/content.config.ts` 里把两个分册的 `available` 由 `false` 改 `true`。
2. **提交并推送 main**（一次推送触发两条流水线）：
   - `Deploy VitePress docs to Pages` → `https://gold99lt.github.io/lubook/`
   - `Deploy to Cloudflare Pages (mirror)` → `https://lubook.pages.dev/`
3. **等两条流水线 success**（并发组已带调用方，不会互相取消，见 ADR-0013）。
4. **上线体检**：
   ```bash
   python packages/tooling/src/check_live_site.py --base https://gold99lt.github.io/lubook/embedded --app embedded --check-assets
   python packages/tooling/src/check_live_site.py --base https://lubook.pages.dev/embedded --app embedded --check-assets
   python packages/tooling/src/check_live_site.py --base https://gold99lt.github.io/lubook/embedded-linux --app embedded-linux --check-assets
   python packages/tooling/src/check_live_site.py --base https://lubook.pages.dev/embedded-linux --app embedded-linux --check-assets
   ```
   判据：路由与同源资源全部 200。
5. **浏览器抽验**：每个分册至少 3 页（首页、公式最多的一页、图最多的一页）。

## 4. 回滚

| 场景 | 动作 |
|---|---|
| 站点构建失败 | GitHub Actions 里 revert 该提交；Pages 会回到上一版 |
| 页面内容错误 | 同上前提下回滚单章文件再推 |
| 门户卡片误开 | 把 `available` 改回 `false` 再推（卡片显示"即将上线"，分册仍可直接访问） |

## 5. 已知不在本次范围

- P4 之外的新分册（暂无）。
- 全文一致性深度复审（本轮只做**抽样复算审查**：每批 4~6 章、约 200 条量化断言）。
- 联网来源复核（本机 DNS 被透明代理接管，结论只对 200 可信；见 `verify_sources.py` 的自检声明）。
