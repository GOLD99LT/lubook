# packages/tooling（Python，非 npm 包）

离线构建、bundle 组装、多 app 质检、`vendor` 等纯标准库工具的归属包。

## 当前状态（多 app 参数化，ADR-0006）

- 脚本统一参数化 `--app/--src/--out`，默认对 `hardware` 等价（`src=apps/<app>/docs`）；内容 app 才做内容检查，门户（无 `SUMMARY.md`）自动跳过。
- `build_single_html.py` 按 `--app` 输出 `dist/<app>.html`，并按 `--manifest .generated/<app>-content-manifest.json` 对账（章节数/id 序列/标题/图片引用数/revision）；不重写 Markdown（ARCHITECTURE §6）。
- `build_pages_bundle.py`：按 `VP_BASE` 构建门户 + 各分册，门户 dist 放输出根、分册 dist 放 `<slug>/`，产出可整体部署目录。
- `verify_all.py`：遍历 `apps/*`，构建 + 内容 app 质检/快照/离线，最后跑 learning 单测。

## 内容

- `src/build_pages_bundle.py`：门户 + 分册 bundle 组装（GitHub Pages / Cloudflare）。
- `src/verify_all.py`：`pnpm verify:all` 的编排主体。
- `src/build_single_html.py`：离线单文件构建（纯标准库、内联 vendor、零依赖）。
- `src/freeze_manifest.py`：manifest/快照生成（`.generated/<app>-content-manifest.json`、`tests/<app>.*.snapshot.json`）。
- `src/run_quality` 相关：`validate.py / scan_math.py / scan_grounds.py / scan_svg_order.py`（+ `fix_*`）。
- `src/build_vp_sidebar.py / sync_public.py / fetch_vendor.py / _stats.py / test_net.py`：侧边栏/品牌资产同步/vendor 拉取/资料合并/统计/网络探测。
- `src/paths_util.py`：共享路径默认值（repo root 发现、`list_apps`、`add_common_args`）。
- `vendor/`：离线内联资源。

## 边界

- 这是 Python 包，**不是 npm 包**：不放 `package.json`，不参与 `pnpm install`。
- 运行方式：仓库根 `pnpm verify:all`（全量门禁）、`pnpm quality:<app>`、`pnpm bundle:pages`、`pnpm offline:<app>`。
- 核心脚本仅依赖标准库。
