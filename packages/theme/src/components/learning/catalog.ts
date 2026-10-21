// 章节目录契约（解耦后）。
//
// 历史实现曾在本文件里 `import sidebar from '../../../sidebar.generated.mjs'`
// 并就地 walk 生成目录——那是 app 私有产物，主题一旦 import 就无法复用到别的手册。
// 现在主题只定义契约：章节目录由 app 侧（从其 sidebar / content-manifest）构造为
// CatalogProvider，并通过 createBookTheme({ catalog }) 注入；本文件不再 import 任何 app 文件。

/** 单个章节的目录项 */
export interface CatalogEntry {
  /** 章节标识，与 VitePress `useData().page.relativePath` 一致（带 `.md` 后缀，如 `basics/voltage-current-power.md`） */
  id: string
  /** 章节标题（侧边栏 text） */
  title: string
  /** 干净 URL（无 `.md`，cleanUrls 模式下可直接跳转） */
  link: string
}

/** app 注入的章节目录提供者 */
export interface CatalogProvider {
  /** 全部章节，顺序即站点顺序 */
  entries: CatalogEntry[]
  /** id -> 标题 */
  titleById: Record<string, string>
  /** id -> 干净链接 */
  linkById: Record<string, string>
}
