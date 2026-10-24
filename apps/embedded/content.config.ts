// apps/embedded/content.config.ts —— 嵌入式软件手册（MCU） 的站点元数据与装配。
//
// 本文件不在运行时访问文件系统：catalog / contentRevision / totalChapters 来自
// 预构建生成的静态模块（docs/.vitepress/catalog.generated.mjs）。
import type { DefaultTheme } from 'vitepress'
import { createLearningRepository } from '@lubook/learning'

import { catalog, contentRevision, totalChapters } from './docs/.vitepress/catalog.generated.mjs'

export const APP_ID = 'embedded'
export const TITLE = '嵌入式软件手册（MCU）'
export const DESCRIPTION =
  '从裸机到 RTOS：Cortex-M 外设驱动、通信接口、任务调度与量产工程实践。'
export const FAVICON = 'favicon.svg'

// 篇号 -> 篇名（与 docs/SUMMARY.md 的 `## 第N篇` 对齐；面包屑与 sidebar 用）。
export const PART_REGISTRY: Record<number, string> = {
  1: '第一篇 · 嵌入式基础',
  2: '第二篇 · Cortex-M 与 MCU 外设',
  3: '第三篇 · 通信接口与协议',
  4: '第四篇 · RTOS 与并发',
  5: '第五篇 · 存储、启动与升级',
  6: '第六篇 · 工程实践与量产'
}

export const NAV: DefaultTheme.NavItem[] = [
  { text: '开始学习', link: '/basics/embedded-overview' }
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
