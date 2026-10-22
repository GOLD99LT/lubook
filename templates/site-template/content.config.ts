// content.config.ts —— 本 app 的站点元数据与装配（复制后改这里即可）。
//
// 本文件【不在运行时访问文件系统】：catalog / contentRevision / totalChapters 来自
// 预构建生成的静态模块（docs/.vitepress/catalog.generated.mjs），浏览器端可安全 import。
// 仓储在模块加载时创建，knownIds 由 catalog 注入（ADR-0007 §3），使导入/迁移数据时
// 未知章节正确进入 tombstone，且现行章节不会被误判为已删除。
import type { DefaultTheme } from 'vitepress'
import { createLearningRepository } from '@lubook/learning'

import { catalog, contentRevision, totalChapters } from './docs/.vitepress/catalog.generated.mjs'

// 复制为 apps/<app> 后：①改 APP_ID（同时改 package.json 的 gen:catalog --appId）
// ②改 TITLE/DESCRIPTION ③改 docs/SUMMARY.md 与篇名
export const APP_ID = 'site-template'
export const TITLE = '新专项手册'
export const DESCRIPTION = '从 templates/site-template 派生的新专项：改 appId / 标题 / 篇名，写 md 与 SUMMARY。'
export const FAVICON = 'favicon.svg'

// 篇号 -> 篇名（与 docs/SUMMARY.md 的 `## 篇名` 对应；章 frontmatter 的 part 字段取这里的键）
export const PART_REGISTRY: Record<number, string> = {
  1: '示例篇'
}

export const NAV: DefaultTheme.NavItem[] = [
  { text: '开始', link: '/example/hello' }
]

export const SOCIAL_LINKS: DefaultTheme.SocialLink[] = []

export { catalog, contentRevision, totalChapters }

// 学习仓储：按 appId 隔离（localStorage 键 lubook.v1.<appId>.learning）。
// knownIds 必须由 catalog 注入：仓储启动时用它过滤已持久化数据，
// 漏传会让所有记录被当成"未知章节"丢弃（表现为刷新后进度/笔记全没了）。
// 新分册不传 legacyKeys（默认空），因此不会迁入其它分册的历史数据。
export const repository = createLearningRepository({
  appId: APP_ID,
  totalChapters,
  contentRevision,
  knownIds: catalog.entries.map((e) => e.id)
})
