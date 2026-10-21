// parity 校验 —— 证明 @lubook/content-core（TS）产物与 P0 tools/freeze_manifest.py 产物一致。
//
// 比对项：
//   1. revision 必须等于 sha256-4c8521761e575941（P0 冻结基线）
//   2. docCount=140 / imageTotal=418 / svgCount=411
//   3. 逐章 deep-compare（id/path/url/title/part/order/tags/images/checksum/difficulty）
//
// 用法：node src/parity.ts --src <docs> --p0 <P0 JSON> --out <TS JSON>

import * as fs from 'node:fs'
import * as path from 'node:path'
import { buildManifest, countSvg } from './index.ts'

function arg(name: string, fallback: string): string {
  const i = process.argv.indexOf(`--${name}`)
  return i >= 0 && i + 1 < process.argv.length ? process.argv[i + 1] : fallback
}

const EXPECTED = {
  revision: 'sha256-4c8521761e575941',
  docCount: 140,
  imageTotal: 418,
  svgCount: 411,
} as const

const src = arg('src', 'docs')
const p0Path = arg('p0', path.join('.generated', 'p0-reference.json'))
const outTs = arg('out', path.join('.generated', 'content-manifest.ts.json'))

const p0 = JSON.parse(fs.readFileSync(p0Path, 'utf8'))
const ts = buildManifest(src, p0.appId ?? 'handbook')
fs.mkdirSync(path.dirname(outTs), { recursive: true })
fs.writeFileSync(outTs, JSON.stringify(ts, null, 2) + '\n', 'utf8')

const imageTotal = ts.docs.reduce((a, d) => a + d.images.length, 0)
const svgCount = countSvg(src)

const problems: string[] = []
const check = (label: string, got: unknown, want: unknown) => {
  if (got !== want) problems.push(`${label}: 期望=${JSON.stringify(want)} 实际=${JSON.stringify(got)}`)
}

check('revision', ts.revision, EXPECTED.revision)
check('revision(vs P0文件)', ts.revision, p0.revision)
check('docCount', ts.docs.length, EXPECTED.docCount)
check('docCount(vs P0文件)', ts.docs.length, p0.docs.length)
check('imageTotal', imageTotal, EXPECTED.imageTotal)
check('svgCount', svgCount, EXPECTED.svgCount)

// 逐章 deep compare
for (let i = 0; i < Math.max(p0.docs.length, ts.docs.length); i++) {
  const a = p0.docs[i]
  const b = ts.docs[i]
  if (!a || !b) {
    problems.push(`docs[${i}] 缺失: p0=${!!a} ts=${!!b}`)
    continue
  }
  const ka = JSON.stringify(a)
  const kb = JSON.stringify(b)
  if (ka !== kb) {
    problems.push(`docs[${i}](${a.id}) 不一致`)
    if (problems.length <= 3) {
      console.error('  P0 :', ka.slice(0, 400))
      console.error('  TS :', kb.slice(0, 400))
    }
  }
}

console.log('---- parity 结果 ----')
console.log(`revision   = ${ts.revision}  (期望 ${EXPECTED.revision})`)
console.log(`docCount   = ${ts.docs.length}  (期望 ${EXPECTED.docCount})`)
console.log(`imageTotal = ${imageTotal}  (期望 ${EXPECTED.imageTotal})`)
console.log(`svgCount   = ${svgCount}  (期望 ${EXPECTED.svgCount})`)
console.log(`TS 产物    = ${outTs}`)

if (problems.length) {
  console.error(`\n[PARITY FAIL] ${problems.length} 处不一致：`)
  for (const p of problems) console.error('  - ' + p)
  process.exit(1)
}
console.log('\n[PARITY PASS] @lubook/content-core 与 P0 freeze_manifest.py 产物一致')
