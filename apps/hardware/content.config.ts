// apps/hardware/content.config.ts —— 硬件分册 app 的站点元数据与装配（part registry）。
//
// 本文件【不在运行时访问文件系统】：catalog / contentRevision / totalChapters 来自
// 预构建生成的静态模块（docs/.vitepress/catalog.generated.mjs），因此浏览器端也能安全
// import。仓储在模块加载时创建并注册全部已知章节，使导入数据时未知章节正确进入 tombstone。
import type { DefaultTheme } from 'vitepress'
import { createLearningRepository } from '@lubook/learning'
import type { CatalogProvider } from '@lubook/theme'

import { catalog, contentRevision, totalChapters } from './docs/.vitepress/catalog.generated.mjs'

export const APP_ID = 'hardware'
export const TITLE = '硬件工程师手册'
export const DESCRIPTION =
  '一本开源、可交互的硬件工程师学习手册：从电路基础到电源、PCB 与 EMC，含原理图、公式推导、设计示例与面试题库。'
export const FAVICON = 'favicon.svg'

// 篇号 -> 篇名（与 docs/SUMMARY.md 一致；面包屑 pageHead 用）。
export const PART_REGISTRY: Record<number, string> = {
  1: '第一篇 · 电路基础',
  2: '第二篇 · 元器件详解',
  3: '第三篇 · 模拟电路与运放',
  4: '第四篇 · 数字电路与逻辑',
  5: '第五篇 · 单片机与嵌入式硬件',
  6: '第六篇 · 电源设计',
  7: '第七篇 · PCB 设计与 EMC',
  8: '第八篇 · 测量、调试与工程实践',
  9: '第九篇 · 硬件测试与面试题库',
  10: '附录'
}

// 顶部固定导航（沿用原 config.mts；非生成的篇下拉）。
export const NAV: DefaultTheme.NavItem[] = [
  { text: '开始学习', link: '/basics/voltage-current-power' },
  { text: '工程速查', link: '/appendix/glossary' },
  { text: '面试刷题', link: '/quizbank/quiz-basics' },
  { text: '附录', link: '/appendix/resources' }
]

export const SOCIAL_LINKS: DefaultTheme.SocialLink[] = [
  { icon: 'github', link: 'https://github.com/GOLD99LT/lubook' }
]

export { catalog, contentRevision, totalChapters }

// 学习仓储：创建后逐章注册（catalog 含全部 140 章），避免现行章被误判为 tombstone。
export const repository = createLearningRepository({
  appId: APP_ID,
  totalChapters,
  contentRevision
})
catalog.entries.forEach((e) => repository.getChapter(e.id))
