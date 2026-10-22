---
id: hello
title: Hello · 示例章
part: 1
chapter: 示例分组
order: 5
tags: [示例, 入门]
difficulty: 1
status: published
sources:
  - templates/site-template（脚手架自带示例）
---

# Hello · 示例章

这是 `templates/site-template` 的示例章，验证共享工具链在空 app 下即可工作：

- `pnpm --filter @lubook/site-template gen` 生成 sidebar 与 catalog（Python + Node，零第三方依赖）；
- `pnpm --filter @lubook/site-template docs:dev` 可启动、HMR 正常；
- `pnpm --filter @lubook/site-template docs:build` 0 错误（SSR 成功）；
- `pnpm --filter @lubook/site-template docs:preview` 可加载产物；
- 五类容器、KaTeX 公式、ECharts 围栏、折叠题、学习面板（在学/已学/收藏/笔记）均可用。

## 公式与容器自检

行内公式 $V_{out}=D\cdot V_{in}$ 与块公式：

$$
D=\frac{V_{out}}{V_{in}}
$$

::: example 示例
这是一个 `tip` 容器；shared-config 还提供 motivation / analogy / example / pitfall / advanced。
:::

新专项脚手架流程（ARCHITECTURE §9）：`cp -r templates/site-template apps/<app>` →
改 `content.config.ts` 的 APP_ID/TITLE/篇名、package.json 的 `gen:catalog --appId` →
写 md 与 SUMMARY（`## 篇名` 分组）→ 先做 3–5 章验证。
