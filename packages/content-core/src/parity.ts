// parity 校验 —— 证明 @lubook/content-core（TS）与 packages/tooling（Python）两个独立解析器
// 对同一份 Markdown 产出一致的内容清单。
//
// 背景：历史上这个脚本写死了 P0 基线里的旧指纹（sha256-4c852176…），还依赖一个已不存在的
// .generated/p0-reference.json，且没有任何 workflow 调用它——等于从未真正对账过。
// 现在改为与本轮 freeze_manifest.py 生成的清单逐字段比对，并与入库快照核对基线。
//
// 用法：
//   node packages/content-core/src/parity.ts --app hardware
//
// 比对项：
//   1. appId / revision
//   2. 章节数与逐章字段（id/path/url/title/part/order/tags/images/checksum/difficulty）
//   3. 与 tests/<app>.manifest.snapshot.json 的基线（revision/docCount/imageTotal/svgCount/titles）

import * as fs from 'node:fs'
import * as path from 'node:path'
import { buildManifest, countSvg } from './index.ts'

function arg(name: string, fallback: string): string {
  const i = process.argv.indexOf(`--${name}`)
  return i >= 0 && i + 1 < process.argv.length ? process.argv[i + 1] : fallback
}

const app = arg('app', 'hardware')
const src = arg('src', path.join('apps', app, 'docs'))
const pyPath = arg('py', path.join('.generated', `${app}-content-manifest.json`))
const snapPath = arg('snapshot', path.join('tests', `${app}.manifest.snapshot.json`))
const outTs = arg('out', path.join('.generated', `${app}-content-manifest.ts.json`))

if (!fs.existsSync(pyPath)) {
  console.error(`[PARITY FAIL] 未找到 Python 清单：${pyPath}`)
  console.error(`  先运行：python packages/tooling/src/freeze_manifest.py --app ${app}`)
  process.exit(1)
}

const py = JSON.parse(fs.readFileSync(pyPath, 'utf8'))
const ts = buildManifest(src, py.appId ?? app)
fs.mkdirSync(path.dirname(outTs), { recursive: true })
fs.writeFileSync(outTs, JSON.stringify(ts, null, 2) + '\n', 'utf8')

const problems: string[] = []
const check = (label: string, got: unknown, want: unknown) => {
  if (JSON.stringify(got) !== JSON.stringify(want)) {
    problems.push(`${label}: python=${JSON.stringify(want)} ts=${JSON.stringify(got)}`)
  }
}

/** 按 key 排序后再序列化，避免字段顺序差异造成假不一致。 */
function canon(v: unknown): string {
  if (v === null || typeof v !== 'object') return JSON.stringify(v)
  if (Array.isArray(v)) return '[' + v.map(canon).join(',') + ']'
  const o = v as Record<string, unknown>
  return '{' + Object.keys(o).sort().map((k) => JSON.stringify(k) + ':' + canon(o[k])).join(',') + '}'
}

check('appId', ts.appId, py.appId)
check('revision', ts.revision, py.revision)
check('docCount', ts.docs.length, (py.docs || []).length)

const imageTotalTs = ts.docs.reduce((a, d) => a + d.images.length, 0)
const imageTotalPy = (py.docs || []).reduce((a: number, d: any) => a + (d.images || []).length, 0)
check('imageTotal', imageTotalTs, imageTotalPy)

const n = Math.max((py.docs || []).length, ts.docs.length)
for (let i = 0; i < n; i++) {
  const a = py.docs?.[i]
  const b = ts.docs[i]
  if (!a || !b) {
    problems.push(`docs[${i}] 缺失：python=${!!a} ts=${!!b}`)
    continue
  }
  const ka = canon(a)
  const kb = canon(b)
  if (ka !== kb) {
    problems.push(`docs[${i}](${a.id}) 字段不一致`)
    if (problems.length <= 3) {
      console.error('  python:', ka.slice(0, 400))
      console.error('  ts    :', kb.slice(0, 400))
    }
  }
}

// 与入库快照的基线核对（防"两个解析器一起漂移"）
let snap: any = null
if (fs.existsSync(snapPath)) {
  snap = JSON.parse(fs.readFileSync(snapPath, 'utf8'))
  check('baseline.revision', ts.revision, snap.revision)
  check('baseline.docCount', ts.docs.length, snap.docCount)
  check('baseline.imageTotal', imageTotalTs, snap.imageTotal)
  check('baseline.svgCount', countSvg(src), snap.svgCount)
  check('baseline.titles', ts.docs.map((d) => d.title), snap.titles)
} else {
  console.warn(`[parity] 未找到快照基线，跳过基线核对：${snapPath}`)
}

console.log('---- parity 结果 ----')
console.log(`app        = ${app}`)
console.log(`revision   = ${ts.revision}`)
console.log(`docCount   = ${ts.docs.length}`)
console.log(`imageTotal = ${imageTotalTs}`)
console.log(`svgCount   = ${countSvg(src)}`)
console.log(`TS 产物    = ${outTs}`)

if (problems.length) {
  console.error(`\n[PARITY FAIL] ${problems.length} 处不一致：`)
  for (const p of problems) console.error('  - ' + p)
  process.exit(1)
}
console.log('\n[PARITY PASS] TS 与 Python 两个解析器的内容清单逐字段一致')
