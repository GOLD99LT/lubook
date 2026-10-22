// @lubook/learning 自验：node 直跑（node test/learning.test.ts），注入内存 fake Storage。
// 覆盖 ADR-0007：§1 版本化信封与导入校验、§2 迁移来源显式声明、§3 knownIds 由 catalog 注入、
// §5 持久化结果进入仓储接口（成功/失败可感知、重试、内存不丢）。
import { createLearningRepository } from '../src/index.ts'

class MemStorage {
  protected m = new Map<string, string>()
  get length() {
    return this.m.size
  }
  key(i: number) {
    return Array.from(this.m.keys())[i] ?? null
  }
  getItem(k: string) {
    return this.m.has(k) ? (this.m.get(k) as string) : null
  }
  setItem(k: string, v: string) {
    this.m.set(k, String(v))
  }
  removeItem(k: string) {
    this.m.delete(k)
  }
  clear() {
    this.m.clear()
  }
}

/** 可切换失败状态的存储：fail=true 时 setItem 抛 QuotaExceededError（ADR-0007 §5 / 验收 1）。 */
class QuotaStorage extends MemStorage {
  fail = false
  setItem(k: string, v: string) {
    if (this.fail) {
      const e = new Error('QuotaExceededError: localStorage quota exceeded')
      e.name = 'QuotaExceededError'
      throw e
    }
    super.setItem(k, v)
  }
}

let passed = 0
let failed = 0
function assert(cond: boolean, msg: string) {
  if (cond) {
    passed++
    console.log('  ok   ' + msg)
  } else {
    failed++
    console.error('  FAIL ' + msg)
  }
}

console.log('[1] 多键迁移合并：显式 legacyKeys hh.v1.learning + hb.v1.handbook.learning -> lubook.v1.hardware.learning')
{
  const s = new MemStorage()
  // 最早全局键（OldShape：version/notes 为字符串）
  s.setItem(
    'hh.v1.learning',
    JSON.stringify({
      version: 1,
      progress: { 'a/ch1.md': 'done', 'a/ch2.md': 'learning' },
      notes: { 'a/ch1.md': '来自全局旧键' },
      favorites: { 'a/ch1.md': true }
    })
  )
  // 旧 app 键（PersistedShape：schemaVersion/appId，notes 为对象）
  s.setItem(
    'hb.v1.handbook.learning',
    JSON.stringify({
      schemaVersion: 1,
      appId: 'handbook',
      progress: { 'a/ch1.md': 'done', 'a/ch3.md': 'learning' },
      favorites: { 'a/ch3.md': true },
      notes: {
        'a/ch1.md': { text: '来自 app 旧键（更新）', updatedAt: '2026-05-01T00:00:00.000Z' }
      }
    })
  )
  const repo = createLearningRepository({
    appId: 'hardware',
    totalChapters: 10,
    storage: s as unknown as Storage,
    knownIds: ['a/ch1.md', 'a/ch2.md', 'a/ch3.md'],
    legacyKeys: ['hh.v1.learning', 'hb.v1.handbook.learning']
  })
  assert(!!s.getItem('lubook.v1.hardware.learning'), '新键 lubook.v1.hardware.learning 已写入')
  assert(!!s.getItem('hh.v1.learning'), '旧全局键 hh.v1.learning 仍保留')
  assert(!!s.getItem('hb.v1.handbook.learning'), '旧 app 键 hb.v1.handbook.learning 仍保留')
  // ch1：两源都有，笔记取 updatedAt 新者（app 键）
  const ch1 = repo.getChapter('a/ch1.md')
  assert(ch1.status === 'done', 'ch1 进度=done')
  assert(ch1.favorite === true, 'ch1 收藏（来自全局键）=true')
  assert(ch1.note?.text === '来自 app 旧键（更新）', 'ch1 笔记按 updatedAt 取 app 键的新版本')
  // ch2：仅全局键
  assert(repo.getChapter('a/ch2.md').status === 'learning', 'ch2 仅全局键，进度=learning')
  // ch3：仅 app 键
  const ch3 = repo.getChapter('a/ch3.md')
  assert(ch3.status === 'learning' && ch3.favorite === true, 'ch3 仅 app 键，进度=learning 且收藏=true')
  const st = repo.stats()
  assert(st.done === 1 && st.learning === 2 && st.favCount === 2,
    `stats done=1 learning=2 fav=2（实际 done=${st.done} learning=${st.learning} fav=${st.favCount}）`)
}

console.log('[1b] F09 迁移隔离：不传 legacyKeys 不迁移旧全局键；显式传入才迁移')
{
  // 1b-1：新分册缺省 legacyKeys=[]，即使全局键存在也不迁移（ADR-0007 §2）。
  const s1 = new MemStorage()
  s1.setItem('hh.v1.learning', JSON.stringify({
    version: 1,
    progress: { 'a/ch1.md': 'done' },
    notes: { 'a/ch1.md': '只有全局笔记' },
    favorites: {}
  }))
  const repo1 = createLearningRepository({
    appId: 'embedded',
    totalChapters: 1,
    storage: s1 as unknown as Storage
  })
  assert(repo1.getChapter('a/ch1.md').status === undefined, '未声明 legacyKeys：全局键进度未迁入')
  assert(repo1.getChapter('a/ch1.md').note === undefined, '未声明 legacyKeys：全局键笔记未迁入')
  assert(s1.getItem('lubook.v1.embedded.learning') === null, '未声明 legacyKeys：未写新键、无迁移动作')
  const st1 = repo1.stats()
  assert(st1.done === 0 && st1.learning === 0 && st1.pct === 0, `新分册 stats 清零（done=${st1.done} pct=${st1.pct}）`)

  // 1b-2：显式传 legacyKeys 才迁移全局键（硬件分册行为保留）。
  const s2 = new MemStorage()
  s2.setItem('hh.v1.learning', JSON.stringify({
    version: 1,
    progress: { 'a/ch1.md': 'done' },
    notes: { 'a/ch1.md': '只有全局笔记' },
    favorites: {}
  }))
  const repo2 = createLearningRepository({
    appId: 'hardware',
    totalChapters: 10,
    storage: s2 as unknown as Storage,
    knownIds: ['a/ch1.md'],
    legacyKeys: ['hh.v1.learning']
  })
  assert(repo2.getChapter('a/ch1.md').note?.text === '只有全局笔记', '显式 legacyKeys：全局键笔记保留')
  assert(repo2.getChapter('a/ch1.md').status === 'done', '显式 legacyKeys：全局键进度迁入')
  assert(!!s2.getItem('lubook.v1.hardware.learning'), '显式 legacyKeys：新键已写入')
}

console.log('[2] 导出：contentRevision / exportedAt')
{
  const s = new MemStorage()
  const repo = createLearningRepository({
    appId: 'hardware',
    totalChapters: 10,
    contentRevision: 'rev-abc',
    storage: s as unknown as Storage,
    knownIds: ['a/ch1.md']
  })
  repo.setStatus('a/ch1.md', 'done')
  const exp = repo.export()
  assert(exp.schemaVersion === 1 && exp.appId === 'hardware', 'export schemaVersion=1 / appId=hardware')
  assert(exp.contentRevision === 'rev-abc', 'export contentRevision 取自 opts')
  assert(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/.test(exp.exportedAt), `export exportedAt 为 ISO（实际 ${exp.exportedAt}）`)
  assert(exp.progress['a/ch1.md'] === 'done', 'export 含进度')
  const exp2 = repo.export('override-rev')
  assert(exp2.contentRevision === 'override-rev', 'export(contentRevision) 入参可覆盖')
  const repo2 = createLearningRepository({
    appId: 'hardware',
    totalChapters: 10,
    storage: new MemStorage() as unknown as Storage
  })
  assert(repo2.export().contentRevision === 'unknown', '默认 contentRevision=unknown')
}

console.log('[3] merge vs replace 差异 + 未知章节 tombstone（不计完成率）')
{
  const s = new MemStorage()
  const repo = createLearningRepository({
    appId: 'hardware',
    totalChapters: 10,
    storage: s as unknown as Storage,
    knownIds: ['a/ch1.md', 'b/ch2.md']
  })
  repo.setStatus('a/ch1.md', 'done')
  repo.setStatus('b/ch2.md', 'learning')
  repo.setFavorite('a/ch1.md', true)

  const imp = {
    schemaVersion: 1,
    appId: 'hardware',
    progress: { 'a/ch1.md': 'learning', 'gone/old.md': 'done' },
    favorites: {},
    notes: {
      'b/ch2.md': { text: 'ch2 note', updatedAt: '2026-01-01T00:00:00.000Z' },
      'gone/old.md': { text: 'x', updatedAt: '2026-01-01T00:00:00.000Z' }
    }
  }
  const r1 = repo.importData(imp, 'merge')
  assert(r1.ok, 'merge 返回 ok')
  assert(JSON.stringify(r1.tombstones) === JSON.stringify(['gone/old.md']), `merge: gone/old.md 进 tombstone（实际 ${JSON.stringify(r1.tombstones)}）`)
  assert(repo.getChapter('a/ch1.md').status === 'learning', 'merge: ch1 状态被覆盖为 learning')
  assert(repo.getChapter('b/ch2.md').status === 'learning', 'merge: ch2 未提供，保留 learning')
  assert(repo.getChapter('b/ch2.md').note?.text === 'ch2 note', 'merge: ch2 笔记写入')
  assert(repo.getChapter('a/ch1.md').favorite === true, 'merge: ch1 收藏未提供，保留 true')
  const snapMid = repo.export()
  assert(snapMid.progress['gone/old.md'] === undefined, 'tombstone 不落库：gone/old.md 无进度')
  assert(snapMid.notes['gone/old.md'] === undefined, 'tombstone 不落库：gone/old.md 无笔记')
  const st = repo.stats()
  assert(st.done === 0 && st.learning === 2, `tombstone 不计完成率: done=0 learning=2（实际 done=${st.done} learning=${st.learning}）`)

  const imp2 = {
    schemaVersion: 1,
    appId: 'hardware',
    progress: { 'a/ch1.md': 'done', 'gone/old.md': 'done' },
    favorites: {},
    notes: {}
  }
  const r2 = repo.importData(imp2, 'replace')
  assert(r2.ok, 'replace 返回 ok')
  assert(JSON.stringify(r2.tombstones) === JSON.stringify(['gone/old.md']), `replace: gone/old.md 仍 tombstone（实际 ${JSON.stringify(r2.tombstones)}）`)
  assert(repo.getChapter('a/ch1.md').status === 'done', 'replace: ch1=done')
  assert(repo.getChapter('b/ch2.md').status === undefined, 'replace: ch2 被整体替换清除')
  assert(repo.getChapter('b/ch2.md').note === undefined, 'replace: ch2 笔记清除')
  const st2 = repo.stats()
  assert(st2.done === 1 && st2.learning === 0 && st2.favCount === 0, `replace 后 stats done=1 fav=0（实际 done=${st2.done} learning=${st2.learning} fav=${st2.favCount}）`)
}

console.log('[4] 导入校验：appId / schemaVersion / 字段类型 / 笔记大小上限')
{
  const s = new MemStorage()
  const repo = createLearningRepository({
    appId: 'hardware',
    totalChapters: 10,
    storage: s as unknown as Storage,
    knownIds: ['a/ch1.md']
  })
  repo.setStatus('a/ch1.md', 'done')
  let r = repo.importData({ schemaVersion: 1, appId: 'other', progress: {}, favorites: {}, notes: {} }, 'merge')
  assert(!r.ok && /appId/.test(r.message), 'appId 不匹配被拒')
  r = repo.importData({ schemaVersion: 2, appId: 'hardware', progress: {}, favorites: {}, notes: {} }, 'merge')
  assert(!r.ok && /schemaVersion/.test(r.message), 'schemaVersion!=1 被拒')
  r = repo.importData({ schemaVersion: 1, appId: 'hardware', progress: { 'a/ch1.md': 'bogus' }, favorites: {}, notes: {} }, 'merge')
  assert(!r.ok, 'progress 非法枚举值被拒')
  r = repo.importData({ schemaVersion: 1, appId: 'hardware', progress: {}, favorites: { 'a/ch1.md': 'yes' }, notes: {} }, 'merge')
  assert(!r.ok, 'favorites 非 boolean 被拒')
  r = repo.importData(
    { schemaVersion: 1, appId: 'hardware', progress: {}, favorites: {}, notes: { 'a/ch1.md': { text: 'x'.repeat(100001), updatedAt: '2026-01-01' } } },
    'merge'
  )
  assert(!r.ok && /100000/.test(r.message), '单条笔记超 100k 被拒')
  r = repo.importData('{ not json', 'merge')
  assert(!r.ok, '非法 JSON 字符串被拒')
}

console.log('[5] 写操作语义：setNote 空串清除 / setStatus null 清除 / clearAll（成功落盘）')
{
  const s = new MemStorage()
  const repo = createLearningRepository({
    appId: 'hardware',
    totalChapters: 10,
    storage: s as unknown as Storage,
    knownIds: ['a/ch1.md']
  })
  let r = repo.setStatus('a/ch1.md', 'done')
  assert(r.ok === true, 'setStatus 返回 ok:true')
  r = repo.setNote('a/ch1.md', '  hello  ')
  assert(r.ok === true, 'setNote 返回 ok:true')
  assert(repo.getChapter('a/ch1.md').note?.text === 'hello', 'setNote 写入并 trim')
  const upd = repo.getChapter('a/ch1.md').note?.updatedAt
  assert(typeof upd === 'string' && upd.length > 0, 'setNote 生成 updatedAt')
  repo.setNote('a/ch1.md', '   ')
  assert(repo.getChapter('a/ch1.md').note === undefined, 'setNote 空串清除笔记')
  repo.setStatus('a/ch1.md', null)
  assert(repo.getChapter('a/ch1.md').status === undefined, 'setStatus null 清除进度')
  r = repo.clearAll()
  assert(r.ok === true, 'clearAll 返回 ok:true')
  const st = repo.stats()
  assert(st.done === 0 && st.learning === 0 && st.favCount === 0, 'clearAll 后全清零')
}

console.log('[6] F04 持久化失败：QuotaExceededError 时写方法 ok:false、saveState.ok=false、内存保留；恢复后 retryPersist 成功落盘')
{
  const s = new QuotaStorage()
  const repo = createLearningRepository({
    appId: 'hardware',
    totalChapters: 10,
    storage: s as unknown as Storage,
    knownIds: ['a/ch1.md']
  })
  assert(repo.saveState.ok === true, '启动无写入时 saveState.ok=true')

  s.fail = true
  const r1 = repo.setStatus('a/ch1.md', 'done')
  assert(r1.ok === false, '配额耗尽：setStatus 返回 ok:false')
  assert(r1.error !== undefined && /QuotaExceededError/.test(r1.error), `失败结果携带错误信息（${r1.error}）`)
  assert(repo.saveState.ok === false, 'saveState.ok===false')
  assert(repo.saveState.error !== null && /QuotaExceededError/.test(repo.saveState.error), `saveState.error 记录错误（${repo.saveState.error}）`)
  assert(repo.getChapter('a/ch1.md').status === 'done', '写入失败：内存状态仍保留（会话内不丢）')
  assert(s.getItem('lubook.v1.hardware.learning') === null, '写入失败：新键未落盘')

  const r2 = repo.setFavorite('a/ch1.md', true)
  assert(r2.ok === false, '配额耗尽：setFavorite 返回 ok:false')
  assert(repo.getChapter('a/ch1.md').favorite === true, '收藏同样保留在内存')

  // 存储恢复正常 → retryPersist 用当前内存状态重写一次。
  s.fail = false
  const r3 = repo.retryPersist()
  assert(r3.ok === true, '恢复后 retryPersist 返回 ok:true')
  assert(repo.saveState.ok === true, '重试成功后 saveState.ok=true')
  assert(repo.saveState.error === null, '重试成功后 saveState.error=null')
  assert(typeof repo.saveState.updatedAt === 'string' && repo.saveState.updatedAt.length > 0, '重试成功后记录 updatedAt')
  assert(!!s.getItem('lubook.v1.hardware.learning'), '重试成功：新键已写入存储')
  const persisted = JSON.parse(s.getItem('lubook.v1.hardware.learning') as string)
  assert(persisted.progress['a/ch1.md'] === 'done', '重试落盘：进度已写入')
  assert(persisted.favorites['a/ch1.md'] === true, '重试落盘：收藏已写入')
}

console.log('[7] F09 双 app 共用同一 Storage：新 app legacyKeys 为空 → 不迁移硬件旧数据，stats=0')
{
  const shared = new MemStorage()
  // 硬件历史全局键：两个硬件章节已学。
  shared.setItem('hh.v1.learning', JSON.stringify({
    version: 1,
    progress: { 'h/ch1.md': 'done', 'h/ch2.md': 'done' },
    notes: { 'h/ch1.md': '硬件笔记一', 'h/ch2.md': '硬件笔记二' },
    favorites: { 'h/ch1.md': true }
  }))

  // 硬件分册：显式声明迁移来源（基准，验证旧数据本身能被硬件 app 读取）。
  const hw = createLearningRepository({
    appId: 'hardware',
    totalChapters: 2,
    storage: shared as unknown as Storage,
    knownIds: ['h/ch1.md', 'h/ch2.md'],
    legacyKeys: ['hh.v1.learning']
  })
  const hwStats = hw.stats()
  assert(hwStats.done === 2, `硬件 app 迁移到两个已学章（done=${hwStats.done}）`)

  // 新分册 embedded：legacyKeys 缺省空、knownIds 只含自己的章节；不允许串入硬件数据。
  const em = createLearningRepository({
    appId: 'embedded',
    totalChapters: 1,
    storage: shared as unknown as Storage,
    knownIds: ['intro.md']
  })
  const emStats = em.stats()
  assert(emStats.done === 0 && emStats.learning === 0 && emStats.pct === 0,
    `新分册不迁移硬件数据（done=${emStats.done} learning=${emStats.learning} pct=${emStats.pct}）`)
  assert(em.getChapter('h/ch1.md').status === undefined, '新分册内存中无硬件章 h/ch1.md 进度')
  assert(em.getChapter('h/ch1.md').note === undefined, '新分册内存中无硬件章 h/ch1.md 笔记')
  assert(em.getChapter('h/ch2.md').status === undefined, '新分册内存中无硬件章 h/ch2.md 进度')
  const emExport = em.export()
  assert(emExport.progress['h/ch1.md'] === undefined && emExport.progress['h/ch2.md'] === undefined,
    '新分册导出信封不含硬件进度')
  assert(emExport.notes['h/ch1.md'] === undefined && emExport.notes['h/ch2.md'] === undefined,
    '新分册导出信封不含硬件笔记')
  assert(shared.getItem('lubook.v1.embedded.learning') === null, '新分册尚未写入自己的键')

  // 新分册只能写自己的已知章节。
  const r = em.setStatus('intro.md', 'learning')
  assert(r.ok === true, '新分册写自己的章节成功')
  assert(em.getChapter('intro.md').status === 'learning', '新分册 intro.md 状态=learning')
  const emStats2 = em.stats()
  assert(emStats2.done === 0 && emStats2.learning === 1, `新分册仅统计自己的章节（learning=${emStats2.learning}）`)
  const emExport2 = em.export()
  assert(emExport2.progress['intro.md'] === 'learning', '新分册键中只有自己的章节')
  assert(emExport2.progress['h/ch1.md'] === undefined, '新分册键中仍无硬件数据')
  // 硬件旧键原样保留，未被新分册改动。
  assert(shared.getItem('hh.v1.learning') !== null, '旧全局键保留未删除')
}

console.log('[8] F09 迁移/导入未知 id 落 tombstone：不落库、不计完成率')
{
  // 8-1：迁移阶段，knownIds 之外的历史章节被丢弃。
  const s = new MemStorage()
  s.setItem('hh.v1.learning', JSON.stringify({
    version: 1,
    progress: { 'm/ch1.md': 'done', 'm/gone.md': 'done' },
    notes: { 'm/ch1.md': '保留', 'm/gone.md': '丢弃笔记' },
    favorites: { 'm/ch1.md': true, 'm/gone.md': true }
  }))
  const repo = createLearningRepository({
    appId: 'hardware',
    totalChapters: 2,
    storage: s as unknown as Storage,
    knownIds: ['m/ch1.md'],
    legacyKeys: ['hh.v1.learning']
  })
  assert(repo.getChapter('m/ch1.md').status === 'done', '迁移：已知章 m/ch1.md 保留')
  assert(repo.getChapter('m/ch1.md').note?.text === '保留', '迁移：已知章笔记保留')
  assert(repo.getChapter('m/ch1.md').favorite === true, '迁移：已知章收藏保留')
  assert(repo.getChapter('m/gone.md').status === undefined, '迁移：未知章 m/gone.md 进度不落库')
  assert(repo.getChapter('m/gone.md').note === undefined, '迁移：未知章 m/gone.md 笔记不落库')
  const st = repo.stats()
  assert(st.done === 1 && st.learning === 0 && st.favCount === 1,
    `迁移：未知章不计完成率/收藏数（done=${st.done} fav=${st.favCount}）`)
  const exp = repo.export()
  assert(exp.progress['m/gone.md'] === undefined && exp.notes['m/gone.md'] === undefined,
    '迁移：导出信封不含未知章记录')

  // 8-2：导入阶段，unknown id 进 tombstones 列表、不落库、不计完成率。
  const r = repo.importData({
    schemaVersion: 1,
    appId: 'hardware',
    progress: { 'm/ch1.md': 'learning', 'old/deleted.md': 'done' },
    favorites: {},
    notes: { 'old/deleted.md': { text: 'x', updatedAt: '2026-01-01T00:00:00.000Z' } }
  }, 'merge')
  assert(r.ok === true, '导入：已知章导入成功')
  assert(JSON.stringify(r.tombstones) === JSON.stringify(['old/deleted.md']),
    `导入：old/deleted.md 进 tombstone（实际 ${JSON.stringify(r.tombstones)}）`)
  assert(repo.getChapter('old/deleted.md').status === undefined, '导入：未知章进度不落库')
  assert(repo.getChapter('old/deleted.md').note === undefined, '导入：未知章笔记不落库')
  const st2 = repo.stats()
  // merge 保留已知章 m/ch1.md 的既有收藏；未知章 old/deleted.md 不计完成率/收藏数。
  assert(st2.done === 0 && st2.learning === 1 && st2.favCount === 1,
    `导入：未知章不计完成率，已知章收藏保留（done=${st2.done} learning=${st2.learning} fav=${st2.favCount}）`)
}

console.log(`\n结果: ${passed} passed, ${failed} failed`)
process.exit(failed ? 1 : 0)
