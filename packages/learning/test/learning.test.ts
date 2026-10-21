// @lubook/learning 自验：node 直跑（node test/learning.test.ts），注入内存 fake Storage。
import { createLearningRepository } from '../src/index.ts'

class MemStorage {
  private m = new Map<string, string>()
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

console.log('[1] 多键迁移合并：hh.v1.learning + hb.v1.handbook.learning -> lubook.v1.hardware.learning')
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

console.log('[1b] 仅旧全局键（无 app 键）也能迁移，旧笔记保留')
{
  const s = new MemStorage()
  s.setItem('hh.v1.learning', JSON.stringify({
    version: 1,
    progress: { 'a/ch1.md': 'done' },
    notes: { 'a/ch1.md': '只有全局笔记' },
    favorites: {}
  }))
  const repo = createLearningRepository({
    appId: 'hardware',
    totalChapters: 10,
    storage: s as unknown as Storage
  })
  assert(repo.getChapter('a/ch1.md').note?.text === '只有全局笔记', '仅全局键时笔记保留')
  assert(!!s.getItem('lubook.v1.hardware.learning'), '新键已写入')
}

console.log('[2] 导出：contentRevision / exportedAt')
{
  const s = new MemStorage()
  const repo = createLearningRepository({ appId: 'hardware', totalChapters: 10, contentRevision: 'rev-abc', storage: s as unknown as Storage })
  repo.setStatus('a/ch1.md', 'done')
  const exp = repo.export()
  assert(exp.schemaVersion === 1 && exp.appId === 'hardware', 'export schemaVersion=1 / appId=hardware')
  assert(exp.contentRevision === 'rev-abc', 'export contentRevision 取自 opts')
  assert(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/.test(exp.exportedAt), `export exportedAt 为 ISO（实际 ${exp.exportedAt}）`)
  assert(exp.progress['a/ch1.md'] === 'done', 'export 含进度')
  const exp2 = repo.export('override-rev')
  assert(exp2.contentRevision === 'override-rev', 'export(contentRevision) 入参可覆盖')
  const repo2 = createLearningRepository({ appId: 'hardware', totalChapters: 10, storage: new MemStorage() as unknown as Storage })
  assert(repo2.export().contentRevision === 'unknown', '默认 contentRevision=unknown')
}

console.log('[3] merge vs replace 差异 + 未知章节 tombstone（不计完成率）')
{
  const s = new MemStorage()
  const repo = createLearningRepository({ appId: 'hardware', totalChapters: 10, storage: s as unknown as Storage })
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
  const repo = createLearningRepository({ appId: 'hardware', totalChapters: 10, storage: s as unknown as Storage })
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

console.log('[5] 写操作语义：setNote 空串清除 / setStatus null 清除 / clearAll')
{
  const s = new MemStorage()
  const repo = createLearningRepository({ appId: 'hardware', totalChapters: 10, storage: s as unknown as Storage })
  repo.setStatus('a/ch1.md', 'done')
  repo.setNote('a/ch1.md', '  hello  ')
  assert(repo.getChapter('a/ch1.md').note?.text === 'hello', 'setNote 写入并 trim')
  const upd = repo.getChapter('a/ch1.md').note?.updatedAt
  assert(typeof upd === 'string' && upd.length > 0, 'setNote 生成 updatedAt')
  repo.setNote('a/ch1.md', '   ')
  assert(repo.getChapter('a/ch1.md').note === undefined, 'setNote 空串清除笔记')
  repo.setStatus('a/ch1.md', null)
  assert(repo.getChapter('a/ch1.md').status === undefined, 'setStatus null 清除进度')
  repo.clearAll()
  const st = repo.stats()
  assert(st.done === 0 && st.learning === 0 && st.favCount === 0, 'clearAll 后全清零')
}

console.log(`\n结果: ${passed} passed, ${failed} failed`)
process.exit(failed ? 1 : 0)
