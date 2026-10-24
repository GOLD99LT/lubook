// apps/embedded-linux/content.config.ts —— 嵌入式 Linux 手册 的站点元数据与装配。
//
// 本文件不在运行时访问文件系统：catalog / contentRevision / totalChapters 来自
// 预构建生成的静态模块（docs/.vitepress/catalog.generated.mjs）。
import type { DefaultTheme } from 'vitepress'
import { createLearningRepository } from '@lubook/learning'

import { catalog, contentRevision, totalChapters } from './docs/.vitepress/catalog.generated.mjs'

export const APP_ID = 'embedded-linux'
export const TITLE = '嵌入式 Linux 手册'
export const DESCRIPTION =
  'Cortex-A 板级开发：启动链、设备树、内核驱动、Buildroot/Yocto 与可靠升级。'
export const FAVICON = 'favicon.svg'

// 篇号 -> 篇名（与 docs/SUMMARY.md 的 `## 第N篇` 对齐；面包屑与 sidebar 用）。
export const PART_REGISTRY: Record<number, string> = {
  1: '第一篇 · 系统与构建',
  2: '第二篇 · 内核与驱动',
  3: '第三篇 · 用户空间与调试',
  4: '第四篇 · 硬件接口与板级支持',
  5: '第五篇 · 可靠性与升级',
  6: '第六篇 · 板级实战'
}

export const NAV: DefaultTheme.NavItem[] = [
  { text: '开始学习', link: '/basics/linux-overview' }
]

export const SOCIAL_LINKS: DefaultTheme.SocialLink[] = []

export { catalog, contentRevision, totalChapters }

// 学习数据按 appId 隔离（localStorage 键 lubook.v1.<appId>.learning）。
// knownIds 必须由 catalog 注入，否则持久化记录会被当成"未知章节"丢弃。
export const repository = createLearningRepository({
  appId: APP_ID,
  totalChapters,
  contentRevision,
  knownIds: catalog.entries.map((e) => e.id)
})
