// 学习数据门面（解耦后）。
//
// 历史实现在此文件里硬编码 `STORAGE_KEY='hh.v1.learning'` 并直接 localStorage.getItem/setItem，
// 还 import app 的 sidebar。现在：
//   - 本包不直接读写 localStorage、不 import app 的 sidebar；
//   - 持久化、按 appId 隔离、旧 key 迁移、导入/导出、tombstone 全部由
//     `@lubook/learning` 的 `LearningRepository` 负责（它内部已是 reactive 并自举 boot）；
//   - 这里只做一层薄委托：UI 读到的值直接穿透到 repository 的 reactive 状态，
//     因此 Vue computed 天然响应，不再维护第二份镜像。
import type {
  LearningRepository,
  ChapterStatus,
  RepositoryStats,
  ImportResult,
  PersistResult,
  SaveState
} from '@lubook/learning'
import type { CatalogProvider } from './catalog'

export type { ChapterStatus, RepositoryStats, ImportResult, PersistResult, SaveState } from '@lubook/learning'

export interface FavItem {
  /** 章节 id（= page.relativePath） */
  id: string
  title: string
  link: string
}

export interface LearningFacade {
  catalog: CatalogProvider
  repository: LearningRepository
  getStatus(id: string): ChapterStatus | undefined
  /** 传 null 表示取消标记（回到未学）；返回持久化结果供 UI 区分成功/失败 */
  setStatus(id: string, status: ChapterStatus | null): PersistResult
  isFavorite(id: string): boolean
  toggleFavorite(id: string): PersistResult
  getNote(id: string): string
  setNote(id: string, text: string): PersistResult
  stats(): RepositoryStats
  /** 全部已收藏章节（按 catalog 顺序） */
  favorites(): FavItem[]
  /** 导出为可下载的 JSON 字符串 */
  exportJSON(): string
  /** 导入（整体覆盖）；返回仓储的校验结果 */
  importJSON(text: string): ImportResult
  clearAll(): PersistResult
  /** 只读响应式保存状态（ADR-0007 §5）：UI 据此显示"已保存 / 未保存"。 */
  readonly saveState: SaveState
  /** 用当前内存状态重写一次持久化，供"重试"按钮使用。 */
  retrySave(): PersistResult
}

// 模块级上下文：createBookTheme 注入一次；组件通过 useLearning() 读取。
let current: LearningFacade | null = null

export function setLearningContext(facade: LearningFacade): void {
  current = facade
}

export function useLearning(): LearningFacade {
  if (!current) {
    throw new Error(
      '[@lubook/theme] 学习上下文未注入：请通过 createBookTheme({ catalog, repository }) 初始化主题'
    )
  }
  return current
}

export function createLearningFacade(
  repository: LearningRepository,
  catalog: CatalogProvider
): LearningFacade {
  function getStatus(id: string): ChapterStatus | undefined {
    return repository.getChapter(id).status
  }

  function setStatus(id: string, status: ChapterStatus | null): PersistResult {
    return repository.setStatus(id, status)
  }

  function isFavorite(id: string): boolean {
    return !!repository.getChapter(id).favorite
  }

  function toggleFavorite(id: string): PersistResult {
    return repository.setFavorite(id, !repository.getChapter(id).favorite)
  }

  function getNote(id: string): string {
    return repository.getChapter(id).note?.text ?? ''
  }

  function setNote(id: string, text: string): PersistResult {
    return repository.setNote(id, text)
  }

  function stats(): RepositoryStats {
    return repository.stats()
  }

  function favorites(): FavItem[] {
    const out: FavItem[] = []
    for (const e of catalog.entries) {
      const rec = repository.getChapter(e.id)
      if (rec.favorite) {
        out.push({
          id: e.id,
          title: catalog.titleById[e.id] || e.title,
          link: catalog.linkById[e.id] || e.link
        })
      }
    }
    return out
  }

  function exportJSON(): string {
    return JSON.stringify(repository.export(), null, 2)
  }

  function importJSON(text: string): ImportResult {
    return repository.importData(text, 'replace')
  }

  function clearAll(): PersistResult {
    return repository.clearAll()
  }

  return {
    catalog,
    repository,
    getStatus,
    setStatus,
    isFavorite,
    toggleFavorite,
    getNote,
    setNote,
    stats,
    favorites,
    exportJSON,
    importJSON,
    clearAll,
    get saveState() {
      return repository.saveState
    },
    retrySave: () => repository.retryPersist(),
    resetLocalData: () => repository.resetLocalData()
  }
}
