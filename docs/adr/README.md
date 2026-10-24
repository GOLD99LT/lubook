# 架构决策记录（ADR）

本目录只追加（append-only），采用 Markdown ADR（MADR 风格）。一篇 ADR 记录一个**有后果、不可逆或影响面大**的决策。

## 索引

| 编号 | 标题 | 状态 |
|---|---|---|
| [ADR-0001](ADR-0001.md) | 采用 pnpm Monorepo 组织多专项 | Accepted |
| [ADR-0002](ADR-0002.md) | 内容 manifest 与「路径即 id」 | Accepted |
| [ADR-0003](ADR-0003.md) | 学习数据仓储化与 appId 隔离 | Accepted |
| [ADR-0004](ADR-0004.md) | 双形态共用 manifest 对账（Python 离线零依赖保留） | Accepted |
| [ADR-0005](ADR-0005.md) | 发布制品与 release.json | Proposed（目标，未实施） |
| [ADR-0006](ADR-0006.md) | 品牌重命名为「路书 Lubook」与多 app 门户拓扑 | Accepted（本地实施完成，待用户核实） |
| [ADR-0007](ADR-0007.md) | 学习数据与离线双形态统一协议（迁移隔离/持久化反馈/章节 id） | Accepted（阶段 A 实施完成，未 push） |
| [ADR-0008](ADR-0008.md) | 内容 frontmatter schema 以现状为准（id/status/sources 必填） | Accepted |
| [ADR-0009](ADR-0009.md) | 内容指纹覆盖 SVG 字节 + 快照基线不被静默覆盖 | Accepted |
| [ADR-0010](ADR-0010.md) | 客户端包体预算：ECharts 按需加载（theme chunk 1.15MB → 113KB） | Accepted |
| [ADR-0011](ADR-0011.md) | 构建内存预算：内容 4.6MB 后必须显式抬高 Node 堆（4GB → 6GB） | Accepted |
| [ADR-0012](ADR-0012.md) | 数学渲染改为运行期：构建内存 −61%、HTML −71%，容量 ×4.3 | Accepted |
| [ADR-0013](ADR-0013.md) | 双站部署拓扑与 CI 并发分组（门禁不再互相取消） | Accepted |
| [ADR-0014](ADR-0014.md) | P4 立项：嵌入式软件手册（MCU）与嵌入式 Linux 手册 | Accepted |

## 规则

- 新 ADR 编号递增，不复用、不删除；状态用 `Proposed / Accepted / Deprecated / Superseded by ADR-XXXX`。
- 何时**必须**写 ADR：不可逆依赖、数据格式（localStorage/manifest/导出）、URL 与内容 id 规则、部署拓扑、第三方服务、安全与版权相关变更（见根 [CONTRIBUTING.md](../../CONTRIBUTING.md) 与 [AGENTS.md](../../AGENTS.md)）。
- 改架构、构建、共享组件、部署：同一改动更新文档或补 ADR。
