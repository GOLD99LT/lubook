// book-manifest CLI —— 由 SUMMARY.md + frontmatter + 磁盘扫描生成 content-manifest.json。
// 用法：node src/cli.ts [--src <docs目录>] [--out <输出JSON>] [--appId <id>]
// 默认：--src docs  --out .generated/content-manifest.json  --appId book（各 app 均显式传 --appId）

import * as fs from 'node:fs'
import * as path from 'node:path'
import { buildManifest, countSvg } from './index.ts'

function arg(name: string, fallback: string): string {
  const i = process.argv.indexOf(`--${name}`)
  return i >= 0 && i + 1 < process.argv.length ? process.argv[i + 1] : fallback
}

const src = arg('src', 'docs')
const out = arg('out', path.join('.generated', 'content-manifest.json'))
const catalogOut = arg('catalogOut', '')
const appId = arg('appId', 'book')

const manifest = buildManifest(src, appId)
const imageTotal = manifest.docs.reduce((a, d) => a + d.images.length, 0)

fs.mkdirSync(path.dirname(out), { recursive: true })
fs.writeFileSync(out, JSON.stringify(manifest, null, 2) + '\n', 'utf8')

// 可选：输出一个【纯数据、无 fs】的 ESM 模块到 VitePress .vitepress，
// 供 config（服务端）与 theme（浏览器端）共同 import，避免在客户端运行 node:fs。
if (catalogOut) {
  const entries = manifest.docs.map((d) => ({ id: d.id, title: d.title, link: d.url }))
  const titleById: Record<string, string> = {}
  const linkById: Record<string, string> = {}
  for (const d of manifest.docs) {
    titleById[d.id] = d.title
    linkById[d.id] = d.url
  }
  const payload = {
    contentRevision: manifest.revision,
    totalChapters: manifest.docs.length,
    catalog: { entries, titleById, linkById }
  }
  const body =
    '// 本文件由 @lubook/content-core 自动生成，请勿手改（纯数据，浏览器端可安全 import）。\n' +
    `export const contentRevision = ${JSON.stringify(payload.contentRevision)}\n` +
    `export const totalChapters = ${payload.totalChapters}\n` +
    `export const catalog = ${JSON.stringify(payload.catalog, null, 2)}\n`
  fs.mkdirSync(path.dirname(catalogOut), { recursive: true })
  fs.writeFileSync(catalogOut, body, 'utf8')
}

console.log(
  `manifest 已生成: ${manifest.docs.length} 章 / ${imageTotal} 处图片引用 / ` +
    `svg=${countSvg(src)} / revision=${manifest.revision} -> ${out}` +
    (catalogOut ? `；catalog 模块 -> ${catalogOut}` : ''),
)
