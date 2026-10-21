// @lubook/learning — LearningRepository：学习数据仓储化。
// 按 appId 隔离（localStorage），支持一次性旧键迁移、导入导出（merge/replace）、未知章节 tombstone。
// UI 只依赖本接口，不直接碰 localStorage；本版不引入 IndexedDB（见 ARCHITECTURE §5 / §14.3）。
import { reactive } from 'vue'

// ---- 契约类型（@lubook/theme 依赖同一接口，命名/字段不可改）----

export type ChapterStatus = 'done' | 'learning'

export interface ChapterRecord {
  status?: ChapterStatus
  favorite?: boolean
  note?: { text: string; updatedAt: string }
}

export interface LearningExport {
  schemaVersion: 1
  appId: string
  contentRevision: string
  exportedAt: string
  progress: Record<string, ChapterStatus>
  favorites: Record<string, boolean>
  notes: Record<string, { text: string; updatedAt: string }>
}

export interface RepositoryStats {
  total: number
  done: number
  learning: number
  favCount: number
  pct: number
}

export interface ImportResult {
  ok: boolean
  message: string
  tombstones?: string[]
}

export interface LearningRepository {
  readonly appId: string
  getChapter(id: string): ChapterRecord
  setChapter(id: string, rec: ChapterRecord): void
  setStatus(id: string, status: ChapterStatus | null): void
  setFavorite(id: string, fav: boolean): void
  setNote(id: string, text: string): void
  stats(): RepositoryStats
  export(contentRevision?: string): LearningExport
  importData(data: unknown, mode: 'merge' | 'replace'): ImportResult
  clearAll(): void
}

export interface CreateLearningRepositoryOptions {
  appId: string
  /** 已知章节总数（用于 stats.total / pct） */
  totalChapters: number
  /** 内容 revision，导出时写入；默认 'unknown' */
  contentRevision?: string
  /** 可注入的存储（测试用内存 Storage）；缺省时浏览器用 localStorage，SSR/无 localStorage 用内存实现 */
  storage?: Storage
}

// ---- 常量 ----

/** 旧版全局键（docs/.vitepress 旧 store）。一次性迁移后保留，不删除。 */
const OLD_KEY = 'hh.v1.learning'
const SCHEMA_VERSION = 1 as const
const NOTE_MAX_LEN = 100_000 // 单条笔记字符上限
const NOTES_TOTAL_MAX = 5 * 1024 * 1024 // 笔记总字符上限（5MB）

// ---- 内部持久化形态 ----

interface PersistedShape {
  schemaVersion: 1
  appId: string
  progress: Record<string, ChapterStatus>
  favorites: Record<string, boolean>
  notes: Record<string, { text: string; updatedAt: string }>
}

interface OldShape {
  version: number
  progress: Record<string, unknown>
  notes: Record<string, unknown>
  favorites: Record<string, unknown>
}

// ---- 工具 ----

function safeParse(s: string): unknown {
  try {
    return JSON.parse(s)
  } catch {
    return null
  }
}

function warn(...args: unknown[]): void {
  if (typeof console !== 'undefined' && typeof console.warn === 'function') {
    console.warn('[hw/learning]', ...args)
  }
}

/** SSR 守卫：注入优先；其次浏览器全局 localStorage；都没有则用内存 Map（不持久化，保证不崩）。 */
function resolveStorage(injected?: Storage): Storage {
  if (injected) return injected
  try {
    const g = globalThis as { localStorage?: Storage }
    if (g && g.localStorage) return g.localStorage
  } catch {
    /* ignore */
  }
  return createMemoryStorage()
}

function createMemoryStorage(): Storage {
  const m = new Map<string, string>()
  return {
    get length() {
      return m.size
    },
    key(i: number) {
      return Array.from(m.keys())[i] ?? null
    },
    getItem(k: string) {
      return m.has(k) ? (m.get(k) as string) : null
    },
    setItem(k: string, v: string) {
      m.set(k, String(v))
    },
    removeItem(k: string) {
      m.delete(k)
    },
    clear() {
      m.clear()
    }
  } as Storage
}

// ---- 严格字段校验（导入用）----

function normalizeProgress(v: unknown): Record<string, ChapterStatus> {
  if (v == null) return {}
  if (typeof v !== 'object' || Array.isArray(v)) throw new TypeError('progress 字段必须是对象')
  const out: Record<string, ChapterStatus> = {}
  for (const [k, val] of Object.entries(v as Record<string, unknown>)) {
    if (val !== 'done' && val !== 'learning') {
      throw new TypeError(`progress[${k}] 必须为 'done' | 'learning'`)
    }
    out[k] = val
  }
  return out
}

function normalizeFavorites(v: unknown): Record<string, boolean> {
  if (v == null) return {}
  if (typeof v !== 'object' || Array.isArray(v)) throw new TypeError('favorites 字段必须是对象')
  const out: Record<string, boolean> = {}
  for (const [k, val] of Object.entries(v as Record<string, unknown>)) {
    if (typeof val !== 'boolean') throw new TypeError(`favorites[${k}] 必须为 boolean`)
    out[k] = val
  }
  return out
}

function normalizeNotes(v: unknown): Record<string, { text: string; updatedAt: string }> {
  if (v == null) return {}
  if (typeof v !== 'object' || Array.isArray(v)) throw new TypeError('notes 字段必须是对象')
  const out: Record<string, { text: string; updatedAt: string }> = {}
  for (const [k, val] of Object.entries(v as Record<string, unknown>)) {
    if (!val || typeof val !== 'object') throw new TypeError(`notes[${k}] 格式错误`)
    const n = val as Record<string, unknown>
    if (typeof n.text !== 'string') throw new TypeError(`notes[${k}].text 必须为 string`)
    if (typeof n.updatedAt !== 'string') throw new TypeError(`notes[${k}].updatedAt 必须为 string`)
    out[k] = { text: n.text, updatedAt: n.updatedAt }
  }
  return out
}

// ---- 工厂 ----

export function createLearningRepository(opts: CreateLearningRepositoryOptions): LearningRepository {
  const appId = opts.appId
  const totalChapters = opts.totalChapters
  const defaultRevision = opts.contentRevision ?? 'unknown'
  const newKey = `hb.v1.${appId}.learning`

  const storage = resolveStorage(opts.storage)

  const state = reactive({
    progress: {} as Record<string, ChapterStatus>,
    favorites: {} as Record<string, boolean>,
    notes: {} as Record<string, { text: string; updatedAt: string }>
  })

  // 已知章节集合：启动时从已持久化数据播种；UI 经 getChapter/写方法访问的 id 也登记。
  // 导入时不在此集合的 id 视为未知章节（旧版已删除/改名的章）→ 进 tombstone，不落库、不计完成率。
  const knownIds = new Set<string>()

  function seedKnown(): void {
    for (const k of Object.keys(state.progress)) knownIds.add(k)
    for (const k of Object.keys(state.favorites)) knownIds.add(k)
    for (const k of Object.keys(state.notes)) knownIds.add(k)
  }

  function registerKnown(id: string): void {
    knownIds.add(id)
  }

  function persist(): void {
    try {
      const payload: PersistedShape = {
        schemaVersion: SCHEMA_VERSION,
        appId,
        progress: state.progress,
        favorites: state.favorites,
        notes: state.notes
      }
      storage.setItem(newKey, JSON.stringify(payload))
    } catch (e) {
      warn('写入本地数据失败', e)
    }
  }

  // ---- 启动：加载新键，或一次性迁移旧键（保留旧键）----
  function boot(): void {
    try {
      const rawNew = storage.getItem(newKey)
      if (rawNew) {
        const parsed = safeParse(rawNew) as PersistedShape | null
        if (parsed && parsed.schemaVersion === SCHEMA_VERSION && parsed.appId === appId) {
          state.progress = normalizeProgress(parsed.progress)
          state.favorites = normalizeFavorites(parsed.favorites)
          state.notes = normalizeNotes(parsed.notes)
          seedKnown()
          return
        }
        warn('新格式数据缺失或损坏，按空数据启动', parsed)
        return
      }
      // 新键不存在 → 尝试迁移旧键
      const rawOld = storage.getItem(OLD_KEY)
      if (rawOld) {
        const old = safeParse(rawOld) as OldShape | null
        if (old && old.version === 1) {
          migrateFromOld(old)
          // 注意：保留旧键，不调用 removeItem(OLD_KEY)
        }
      }
    } catch (e) {
      warn('启动加载失败', e)
    }
  }

  function migrateFromOld(old: OldShape): void {
    const now = new Date().toISOString()
    state.progress = normalizeProgress(old.progress)
    state.favorites = normalizeFavorites(old.favorites)
    const notes: PersistedShape['notes'] = {}
    for (const [id, text] of Object.entries(old.notes ?? {})) {
      if (typeof text === 'string' && text) notes[id] = { text, updatedAt: now }
    }
    state.notes = notes
    seedKnown()
    persist() // 写新键；旧键保留
  }

  // ---- 仓储方法 ----

  function getChapter(id: string): ChapterRecord {
    registerKnown(id)
    const rec: ChapterRecord = {}
    if (id in state.progress) rec.status = state.progress[id]
    if (state.favorites[id]) rec.favorite = true
    if (state.notes[id]) rec.note = { ...state.notes[id] }
    return rec
  }

  function setChapter(id: string, rec: ChapterRecord): void {
    registerKnown(id)
    if (rec.status === undefined) delete state.progress[id]
    else state.progress[id] = rec.status
    if (rec.favorite === undefined) delete state.favorites[id]
    else if (rec.favorite) state.favorites[id] = true
    else delete state.favorites[id]
    if (rec.note === undefined) delete state.notes[id]
    else state.notes[id] = { text: rec.note.text, updatedAt: rec.note.updatedAt }
    persist()
  }

  function setStatus(id: string, status: ChapterStatus | null): void {
    registerKnown(id)
    if (status === null) delete state.progress[id]
    else state.progress[id] = status
    persist()
  }

  function setFavorite(id: string, fav: boolean): void {
    registerKnown(id)
    if (fav) state.favorites[id] = true
    else delete state.favorites[id]
    persist()
  }

  function setNote(id: string, text: string): void {
    registerKnown(id)
    const t = (text ?? '').trim()
    if (t) state.notes[id] = { text: t, updatedAt: new Date().toISOString() }
    else delete state.notes[id]
    persist()
  }

  function stats(): RepositoryStats {
    let done = 0
    let learning = 0
    for (const s of Object.values(state.progress)) {
      if (s === 'done') done++
      else if (s === 'learning') learning++
    }
    let favCount = 0
    for (const f of Object.values(state.favorites)) if (f) favCount++
    return {
      total: totalChapters,
      done,
      learning,
      favCount,
      pct: totalChapters ? Math.round((done / totalChapters) * 100) : 0
    }
  }

  function exportData(contentRevision?: string): LearningExport {
    const notes: LearningExport['notes'] = {}
    for (const [id, n] of Object.entries(state.notes)) {
      notes[id] = { text: n.text, updatedAt: n.updatedAt }
    }
    return {
      schemaVersion: SCHEMA_VERSION,
      appId,
      contentRevision: contentRevision ?? defaultRevision,
      exportedAt: new Date().toISOString(),
      progress: { ...state.progress },
      favorites: { ...state.favorites },
      notes
    }
  }

  function importData(data: unknown, mode: 'merge' | 'replace'): ImportResult {
    let parsed: unknown = data
    if (typeof data === 'string') {
      try {
        parsed = JSON.parse(data)
      } catch (e) {
        return { ok: false, message: `导入失败：JSON 解析错误（${(e as Error)?.message ?? e}）` }
      }
    }
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
      return { ok: false, message: '导入失败：不是合法的 JSON 对象' }
    }
    const p = parsed as Record<string, unknown>
    if (p.appId !== appId) {
      return { ok: false, message: `导入失败：appId 不匹配（文件为 ${String(p.appId)}，当前为 ${appId}）` }
    }
    if (p.schemaVersion !== SCHEMA_VERSION) {
      return { ok: false, message: '导入失败：版本不兼容（需要 schemaVersion=1）' }
    }

    let progress: Record<string, ChapterStatus>
    let favorites: Record<string, boolean>
    let notes: Record<string, { text: string; updatedAt: string }>
    try {
      progress = normalizeProgress(p.progress)
      favorites = normalizeFavorites(p.favorites)
      notes = normalizeNotes(p.notes)
    } catch (e) {
      return { ok: false, message: `导入失败：${(e as Error).message}` }
    }

    // 大小上限
    let totalNoteSize = 0
    for (const n of Object.values(notes)) {
      if (n.text.length > NOTE_MAX_LEN) {
        return { ok: false, message: `导入失败：单条笔记超过 ${NOTE_MAX_LEN} 字符上限` }
      }
      totalNoteSize += n.text.length
    }
    if (totalNoteSize > NOTES_TOTAL_MAX) {
      return { ok: false, message: `导入失败：笔记总大小超过 ${NOTES_TOTAL_MAX} 字符上限` }
    }

    // 收集未知章节（tombstone）：不在已知集合
    const tombset = new Set<string>()
    const ids = new Set<string>([
      ...Object.keys(progress),
      ...Object.keys(favorites),
      ...Object.keys(notes)
    ])
    for (const id of ids) if (!knownIds.has(id)) tombset.add(id)

    if (mode === 'replace') {
      state.progress = {}
      state.favorites = {}
      state.notes = {}
    }
    for (const [id, s] of Object.entries(progress)) {
      if (knownIds.has(id)) state.progress[id] = s
    }
    for (const [id, f] of Object.entries(favorites)) {
      if (!knownIds.has(id)) continue
      if (f) state.favorites[id] = true
      else delete state.favorites[id]
    }
    for (const [id, n] of Object.entries(notes)) {
      if (knownIds.has(id)) state.notes[id] = { text: n.text, updatedAt: n.updatedAt }
    }
    persist()

    const tombstones = Array.from(tombset).sort()
    return {
      ok: true,
      message: tombstones.length
        ? `导入成功（${mode}），${tombstones.length} 个未知章节已忽略`
        : `导入成功（${mode}）`,
      ...(tombstones.length ? { tombstones } : {})
    }
  }

  function clearAll(): void {
    state.progress = {}
    state.favorites = {}
    state.notes = {}
    persist()
  }

  boot()

  return {
    appId,
    getChapter,
    setChapter,
    setStatus,
    setFavorite,
    setNote,
    stats,
    export: exportData,
    importData,
    clearAll
  }
}

export const OLD_STORAGE_KEY = OLD_KEY
