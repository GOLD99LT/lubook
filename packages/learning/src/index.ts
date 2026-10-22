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

/** 单次持久化结果（ADR-0007 §5）：写方法与 importData 统一返回，UI 据此区分成功/失败。 */
export interface PersistResult {
  ok: boolean
  error?: string
}

/** 响应式保存状态：UI 据此显示"已保存 / 未保存"，并提供重试与导出兜底。 */
export interface SaveState {
  ok: boolean
  error: string | null
  updatedAt: string | null
}

export interface LearningRepository {
  readonly appId: string
  getChapter(id: string): ChapterRecord
  setChapter(id: string, rec: ChapterRecord): PersistResult
  setStatus(id: string, status: ChapterStatus | null): PersistResult
  setFavorite(id: string, fav: boolean): PersistResult
  setNote(id: string, text: string): PersistResult
  stats(): RepositoryStats
  export(contentRevision?: string): LearningExport
  importData(data: unknown, mode: 'merge' | 'replace'): ImportResult
  clearAll(): PersistResult
  /** 只读响应式保存状态（当前会话内存状态仍保留，即使写失败）。 */
  readonly saveState: SaveState
  /** 用当前内存状态重写一次持久化，供"重试"按钮使用。 */
  retryPersist(): PersistResult
}

export interface CreateLearningRepositoryOptions {
  appId: string
  /** 已知章节总数（用于 stats.total / pct） */
  totalChapters: number
  /** 内容 revision，导出时写入；默认 'unknown' */
  contentRevision?: string
  /** 可注入的存储（测试用内存 Storage）；缺省时浏览器用 localStorage，SSR/无 localStorage 用内存实现 */
  storage?: Storage
  /**
   * 已知章节 id 集合（由 app 从 catalog.entries[].id 注入，ADR-0007 §3）。
   * 迁移、导入时不在此集合内的 id 一律落 tombstone：不写入、不计完成率。
   * 缺省为空集合（新分册不声明历史来源时，旧数据不会进入当前状态）。
   */
  knownIds?: string[]
  /**
   * 旧键列表（按从旧到新排序，完全由 app 显式声明，ADR-0007 §2）：新键不存在时，
   * 依次读取并合并，迁移后保留旧键；缺省为空数组 → 不做任何迁移。
   * 兼容两种形态：旧全局键（OldShape：version/notes 为字符串）与
   * 旧 app 键（PersistedShape：schemaVersion/appId/notes 为对象）。
   */
  legacyKeys?: string[]
}

// ---- 常量 ----

/** 最早的全局键（docs/.vitepress 旧 store，OldShape）。迁移后保留，不删除。 */
const OLD_KEY = 'hh.v1.learning'
/** 新键前缀（ADR-0006：lubook.v1.<slug>.learning）。 */
const NEW_KEY_PREFIX = 'lubook.v1'
const SCHEMA_VERSION = 1 as const
/** 无时间戳的旧全局笔记在合并时使用的纪元（低于任何真实 updatedAt）。 */
const LEGACY_EPOCH = '1970-01-01T00:00:00.000Z'
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
    console.warn('[lubook/learning]', ...args)
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
  const newKey = `${NEW_KEY_PREFIX}.${appId}.learning`
  // 迁移来源完全由 app 显式声明（ADR-0007 §2）：不再无条件前置最早全局键；新分册缺省空数组 → 不迁移。
  const legacyKeys = (opts.legacyKeys ?? []).filter((k, i, arr) => arr.indexOf(k) === i)

  const storage = resolveStorage(opts.storage)

  const state = reactive({
    progress: {} as Record<string, ChapterStatus>,
    favorites: {} as Record<string, boolean>,
    notes: {} as Record<string, { text: string; updatedAt: string }>
  })

  // 已知章节集合：由 catalog 注入（ADR-0007 §3），不随存储历史播种、不随 UI 访问扩张。
  // 迁移、导入时不在此集合的 id 视为未知章节（旧版已删除/改名的章）→ 进 tombstone，不落库、不计完成率。
  const knownIds = new Set<string>(opts.knownIds ?? [])

  // 响应式保存状态（ADR-0007 §5）：写失败时内存状态仍保留，UI 据此提示"未保存"。
  const saveState = reactive<SaveState>({ ok: true, error: null, updatedAt: null })

  // 启动时若发现本地数据损坏/版本不符，禁止自动写回：否则一次普通操作就会用空状态
  // 覆盖掉用户原有数据。此时只读不写，由用户导出或显式重置。
  let bootFailed = false

  function persist(): PersistResult {
    if (bootFailed) {
      const error = saveState.error ?? '本地数据无法解析，已停止自动保存以免覆盖原数据'
      saveState.ok = false
      saveState.error = error
      return { ok: false, error }
    }
    try {
      const payload: PersistedShape = {
        schemaVersion: SCHEMA_VERSION,
        appId,
        progress: state.progress,
        favorites: state.favorites,
        notes: state.notes
      }
      storage.setItem(newKey, JSON.stringify(payload))
      saveState.ok = true
      saveState.error = null
      saveState.updatedAt = new Date().toISOString()
      return { ok: true }
    } catch (e) {
      const error = (e as Error)?.message ?? String(e)
      saveState.ok = false
      saveState.error = error
      warn('写入本地数据失败', e)
      return { ok: false, error }
    }
  }

  /** 按 knownIds 过滤归一化形态：未知 id 一律不落库（tombstone，ADR-0007 §1/§2/§3）。 */
  function filterKnown(n: Normalized): Normalized {
    const progress: Normalized['progress'] = {}
    const favorites: Normalized['favorites'] = {}
    const notes: Normalized['notes'] = {}
    for (const [id, v] of Object.entries(n.progress)) {
      if (knownIds.has(id)) progress[id] = v
    }
    for (const [id, v] of Object.entries(n.favorites)) {
      if (knownIds.has(id)) favorites[id] = v
    }
    for (const [id, n2] of Object.entries(n.notes)) {
      if (knownIds.has(id)) notes[id] = { ...n2 }
    }
    return { progress, favorites, notes }
  }

  // ---- 启动：加载新键；不存在则合并迁移显式声明的旧键（保留旧键）----
  function boot(): void {
    try {
      const rawNew = storage.getItem(newKey)
      if (rawNew) {
        const parsed = safeParse(rawNew) as PersistedShape | null
        if (parsed && parsed.schemaVersion === SCHEMA_VERSION && parsed.appId === appId) {
          const loaded = filterKnown({
            progress: normalizeProgress(parsed.progress),
            favorites: normalizeFavorites(parsed.favorites),
            notes: normalizeNotes(parsed.notes)
          })
          state.progress = loaded.progress
          state.favorites = loaded.favorites
          state.notes = loaded.notes
          return
        }
        warn('新格式数据缺失或损坏，按空数据启动', parsed)
        // 关键：不清空、不写回。置失败态，让 UI 提示"未保存"并禁用自动保存，
        // 用户至少可以导出或人工排查，而不是被一次点击静默覆盖。
        bootFailed = true
        saveState.ok = false
        saveState.bootFailed = true
        saveState.error = '本地学习数据无法解析（可能来自旧版本或已损坏），已停止自动保存以免覆盖原数据'
        return
      }
      // 新键不存在 → 依次读取显式声明的旧键（从旧到新），归一化后合并；未知 id 落 tombstone。
      const sources: Normalized[] = []
      for (const key of legacyKeys) {
        const raw = storage.getItem(key)
        if (!raw) continue
        const n = readLegacy(raw)
        if (n) sources.push(n)
      }
      if (sources.length) {
        const merged = filterKnown(mergeSources(sources))
        state.progress = merged.progress
        state.favorites = merged.favorites
        state.notes = merged.notes
        persist() // 写新键；所有旧键保留
      }
    } catch (e) {
      warn('启动加载失败', e)
    }
  }

  /** 归一化中间形态（notes 均为 {text,updatedAt}）。 */
  interface Normalized {
    progress: Record<string, ChapterStatus>
    favorites: Record<string, boolean>
    notes: Record<string, { text: string; updatedAt: string }>
  }

  /** 读取一个旧键，自动识别 OldShape（version）/ PersistedShape（schemaVersion）。 */
  function readLegacy(raw: string): Normalized | null {
    const data = safeParse(raw)
    if (!data || typeof data !== 'object') return null
    const o = data as Record<string, unknown>
    // 旧 app 键：PersistedShape
    if (o.schemaVersion === SCHEMA_VERSION) {
      // 允许 appId 与当前不同（如 handbook -> hardware），数据按章 id 迁移。
      try {
        return {
          progress: normalizeProgress(o.progress),
          favorites: normalizeFavorites(o.favorites),
          notes: normalizeNotes(o.notes)
        }
      } catch (e) {
        warn('旧 app 键数据损坏，已跳过', e)
        return null
      }
    }
    // 最早全局键：OldShape（version=1，notes 为字符串，无时间戳）
    if (o.version === 1) {
      const old = o as unknown as OldShape
      // 无原始时间戳：标记为最早纪元，使任何带真实 updatedAt 的新来源在合并时胜出。
      const notes: Normalized['notes'] = {}
      for (const [id, text] of Object.entries(old.notes ?? {})) {
        if (typeof text === 'string' && text) notes[id] = { text, updatedAt: LEGACY_EPOCH }
      }
      try {
        return {
          progress: normalizeProgress(old.progress),
          favorites: normalizeFavorites(old.favorites),
          notes
        }
      } catch (e) {
        warn('旧全局键数据损坏，已跳过', e)
        return null
      }
    }
    return null
  }

  /** 合并多个归一化来源（从旧到新）：后者覆盖前者 progress/favorites；notes 取 updatedAt 最新。 */
  function mergeSources(sources: Normalized[]): Normalized {
    const progress: Record<string, ChapterStatus> = {}
    const favorites: Record<string, boolean> = {}
    const notes: Record<string, { text: string; updatedAt: string }> = {}
    for (const s of sources) {
      for (const [id, v] of Object.entries(s.progress)) progress[id] = v
      for (const [id, v] of Object.entries(s.favorites)) favorites[id] = v
      for (const [id, n] of Object.entries(s.notes)) {
        const prev = notes[id]
        if (!prev || n.updatedAt >= prev.updatedAt) notes[id] = { ...n }
      }
    }
    return { progress, favorites, notes }
  }

  // ---- 仓储方法 ----

  function getChapter(id: string): ChapterRecord {
    const rec: ChapterRecord = {}
    if (id in state.progress) rec.status = state.progress[id]
    if (state.favorites[id]) rec.favorite = true
    if (state.notes[id]) rec.note = { ...state.notes[id] }
    return rec
  }

  function setChapter(id: string, rec: ChapterRecord): PersistResult {
    if (rec.status === undefined) delete state.progress[id]
    else state.progress[id] = rec.status
    if (rec.favorite === undefined) delete state.favorites[id]
    else if (rec.favorite) state.favorites[id] = true
    else delete state.favorites[id]
    if (rec.note === undefined) delete state.notes[id]
    else state.notes[id] = { text: rec.note.text, updatedAt: rec.note.updatedAt }
    return persist()
  }

  function setStatus(id: string, status: ChapterStatus | null): PersistResult {
    if (status === null) delete state.progress[id]
    else state.progress[id] = status
    return persist()
  }

  function setFavorite(id: string, fav: boolean): PersistResult {
    if (fav) state.favorites[id] = true
    else delete state.favorites[id]
    return persist()
  }

  function setNote(id: string, text: string): PersistResult {
    const t = (text ?? '').trim()
    if (t) state.notes[id] = { text: t, updatedAt: new Date().toISOString() }
    else delete state.notes[id]
    return persist()
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

    // 只有持久化成功才返回 ok:true；失败时内存状态已保留（会话内不丢），返回失败结果供 UI 提示。
    const saved = persist()
    if (!saved.ok) {
      return {
        ok: false,
        message: `导入失败：本地存储写入失败（${saved.error ?? '未知错误'}），数据已保留在当前会话，可先「导出数据」兜底`
      }
    }

    const tombstones = Array.from(tombset).sort()
    return {
      ok: true,
      message: tombstones.length
        ? `导入成功（${mode}），${tombstones.length} 个未知章节已忽略`
        : `导入成功（${mode}）`,
      ...(tombstones.length ? { tombstones } : {})
    }
  }

  function clearAll(): PersistResult {
    state.progress = {}
    state.favorites = {}
    state.notes = {}
    return persist()
  }

  /**
   * 显式重置：删除无法解析的本地键，清空内存状态，解除 bootFailed 后重新落盘。
   * 只在用户确认要丢弃旧数据时调用。
   */
  function resetLocalData(): PersistResult {
    try {
      storage.removeItem(newKey)
    } catch (e) {
      warn('删除损坏的本地数据失败', e)
    }
    state.progress = {}
    state.favorites = {}
    state.notes = {}
    bootFailed = false
    saveState.bootFailed = false
    saveState.error = null
    return persist()
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
    clearAll,
    saveState,
    retryPersist: persist,
    resetLocalData
  }
}

export const OLD_STORAGE_KEY = OLD_KEY
export const NEW_STORAGE_KEY_PREFIX = NEW_KEY_PREFIX
