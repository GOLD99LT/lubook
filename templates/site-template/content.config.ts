// content.config.ts —— 本 app 的站点元数据与装配（复制后改这里即可）。
//
// 本文件【不在运行时访问文件系统】：catalog / contentRevision / totalChapters 来自
// 预构建生成的静态模块（docs/.vitepress/catalog.generated.mjs），浏览器端可安全 import。
// 仓储在模块加载时创建并注册全部已知章节，使导入数据时未知章节正确进入 tombstone。
import type { DefaultTheme } from 'vitepress'
import { createLearningRepository } from '@lubook/learning'

import { catalog, contentRevision, totalChapters } from './docs/.vitepress/catalog.generated.mjs'

// 复制为 apps/<app> 后：①改 APP_ID（同时改 package.json 的 gen:catalog --appId）
// ②改 TITLE/DESCRIPTION ③按需改 base（docs/.vitepress/config.mts）
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

// 学习仓储：按 appId 隔离（localStorage 键 hb.v1.<appId>.learning）。
export const repository = createLearningRepository({
  appId: APP_ID,
  totalChapters,
  contentRevision
})
catalog.entries.forEach((e) => repository.getChapter(e.id))
