// @lubook/content-core —— manifest 生成器（ARCHITECTURE §3.1）。
//
// 本文件逐行移植 P0 的 tools/build_vp_sidebar.py（parse_yaml / split_frontmatter /
// parse_summary）与 tools/freeze_manifest.py 的解析/校验/checksum 逻辑，
// 保证 TS 产物与 Python 产物逐字一致（parity 校验见 parity.ts）。
//
// 数据源：<src>/SUMMARY.md + 各章 frontmatter + 磁盘扫描。
// 纯 Node/TS，不依赖 Python、不依赖第三方包。

import { createHash } from 'node:crypto'
import * as fs from 'node:fs'
import * as path from 'node:path'

// ---------------------------------------------------------------------------
// 类型（ARCHITECTURE §3.1）
// ---------------------------------------------------------------------------

export interface ContentDoc {
  id: string // = 相对路径（如 opamp/inverting-amplifier.md）
  path: string
  url: string // clean URL
  title: string
  part: string // 来自 SUMMARY 的篇名
  order: number
  tags: string[]
  difficulty?: 1 | 2 | 3
  images: string[]
  checksum: string
}

export interface ContentManifest {
  appId: string
  revision: string // 由内容 checksum 派生
  docs: ContentDoc[]
}

export interface ManifestFingerprint {
  appId: string
  revision: string
  docCount: number
  titles: string[]
  imageTotal: number
  svgCount: number
  overallChecksum: string
}

// ---------------------------------------------------------------------------
// 工具
// ---------------------------------------------------------------------------

function sha256Hex(buf: Buffer | string): string {
  return createHash('sha256').update(buf).digest('hex')
}

/**
 * 文本内容指纹的跨平台规范化：统一换行为 LF（与仓库 blob 一致）。
 * 必须在哈希前归一，否则 Windows（`* text=auto` 检出为 CRLF）与 Linux（LF）
 * 会让同一份逻辑内容算出不同 checksum，导致跨平台快照门禁失败。
 */
function normalizeTextForHash(buf: Buffer): string {
  return buf.toString('utf8').replace(/\r\n|\r/g, '\n')
}

/** opamp/inverting-amplifier.md -> /opamp/inverting-amplifier（VitePress clean URL）。 */
export function cleanUrl(rel: string): string {
  let p = rel.replace(/\\/g, '/')
  if (p.startsWith('./')) p = p.slice(2)
  if (p.endsWith('.md')) p = p.slice(0, -3)
  return '/' + p
}

// ---------------------------------------------------------------------------
// frontmatter 解析（移植 build_vp_sidebar.parse_yaml / split_frontmatter）
// ---------------------------------------------------------------------------

/** 极简 YAML 行解析，与 Python 版同口径（仅支持标量 / 行内数组 / 缩进列表）。 */
export function parseYaml(text: string): Record<string, unknown> {
  const data: Record<string, unknown> = {}
  const lines = text.split(/\r\n|\r|\n/)
  let i = 0
  while (i < lines.length) {
    const line = lines[i]
    if (!line.trim() || line.trimStart().startsWith('#')) {
      i++
      continue
    }
    const m = /^([A-Za-z_][\w-]*):\s*(.*)$/.exec(line)
    if (!m) {
      i++
      continue
    }
    const key = m[1]
    const val = m[2].trim()
    if (val === '') {
      const items: string[] = []
      let j = i + 1
      while (j < lines.length && (!lines[j].trim() || lines[j].startsWith(' '))) {
        const mm = /^\s+-\s*(.*)$/.exec(lines[j])
        if (mm) items.push(mm[1].trim())
        j++
      }
      data[key] = items
      i = j
      continue
    }
    if (val.startsWith('[') && val.endsWith(']')) {
      data[key] = val
        .slice(1, -1)
        .split(',')
        .map((x) => x.trim().replace(/^['"]+|['"]+$/g, ''))
        .filter((x) => x)
    } else {
      let v: string | number = val.replace(/^['"]+|['"]+$/g, '')
      if (/^-?\d+$/.test(v)) v = parseInt(v, 10)
      data[key] = v
    }
    i++
  }
  return data
}

/** 与 Python split_frontmatter 同口径：仅认 `---` 包裹、以 `\n---` 收尾。 */
export function splitFrontmatter(text: string): [Record<string, unknown>, string] {
  if (text.startsWith('---')) {
    const end = text.indexOf('\n---', 3)
    if (end !== -1) {
      const fm = text.slice(3, end).trim()
      const body = text.slice(end + 4)
      return [parseYaml(fm), body]
    }
  }
  return [{}, text]
}

// ---------------------------------------------------------------------------
// SUMMARY.md 解析（移植 build_vp_sidebar.parse_summary）
// ---------------------------------------------------------------------------

export interface SummaryPart {
  name: string
  items: Array<[string, string]> // [显示名, 相对路径]
}

export function parseSummary(summaryPath: string): SummaryPart[] {
  const text = fs.readFileSync(summaryPath, 'utf8')
  const parts: SummaryPart[] = []
  let cur: SummaryPart | null = null
  for (const raw of text.split('\n')) {
    // 文件可能是 CRLF：Python 侧用 rstrip('\n') 后由 .strip() 收尾；
    // JS 的 . 不匹配 \r，必须先去掉行尾 \r，否则 `$` 前的 \r 会让正则落空。
    const line = raw.replace(/\r$/, '')
    let m = /^##\s+(.*)$/.exec(line)
    if (m) {
      cur = { name: m[1].trim(), items: [] }
      parts.push(cur)
      continue
    }
    m = /^\s*[*-]\s+\[([^\]]+)\]\(([^)]+)\)\s*$/.exec(line)
    if (m && cur) {
      cur.items.push([m[1].trim(), m[2].trim()])
    }
  }
  return parts
}

// ---------------------------------------------------------------------------
// 图片引用提取（移植 freeze_manifest.extract_images）
// ---------------------------------------------------------------------------

/** 正文图片引用（与 validate.py 同口径），返回 src/ 相对路径，按出现顺序、不去重。 */
export function extractImages(body: string, docAbsPath: string, srcDir: string): string[] {
  const out: string[] = []
  const re = /!\[[^\]]*\]\(([^)]+)\)/g
  let m: RegExpExecArray | null
  while ((m = re.exec(body)) !== null) {
    const target = m[1].trim()
    if (target.startsWith('http') || target.startsWith('data:')) continue
    const t = target.split(/\s+/)[0]
    const absT = path.normalize(path.join(path.dirname(docAbsPath), t))
    out.push(path.relative(srcDir, absT).replace(/\\/g, '/'))
  }
  return out
}

// ---------------------------------------------------------------------------
// 磁盘扫描
// ---------------------------------------------------------------------------

function walk(srcDir: string, cb: (rel: string, abs: string) => void): void {
  const rec = (dir: string): void => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const abs = path.join(dir, entry.name)
      if (entry.isDirectory()) rec(abs)
      else cb(path.relative(srcDir, abs).replace(/\\/g, '/'), abs)
    }
  }
  rec(srcDir)
}

export function countSvg(srcDir: string): number {
  const base = path.join(srcDir, 'assets')
  let n = 0
  const rec = (dir: string): void => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const abs = path.join(dir, entry.name)
      if (entry.isDirectory()) rec(abs)
      else if (entry.name.endsWith('.svg')) n++
    }
  }
  if (fs.existsSync(base)) rec(base)
  return n
}

// ---------------------------------------------------------------------------
// manifest 构建（移植 freeze_manifest.build_manifest）
// ---------------------------------------------------------------------------

export function buildManifest(srcDir: string, appId = 'book'): ContentManifest {
  const errors: string[] = []
  const parts = parseSummary(path.join(srcDir, 'SUMMARY.md'))
  const docs: ContentDoc[] = []

  for (const part of parts) {
    for (const [disp, relRaw] of part.items) {
      const rel = relRaw.replace(/\\/g, '/')
      const fp = path.join(srcDir, ...rel.split('/'))
      if (!fs.existsSync(fp)) {
        errors.push(`SUMMARY 登记但磁盘缺失: ${rel}`)
        continue
      }
      const raw = fs.readFileSync(fp)
      const text = raw.toString('utf8')
      const [fm, body] = splitFrontmatter(text)

      // order：与 Python int(order) 同口径（非整数回落 0）
      let order = 0
      const ro = fm['order']
      if (typeof ro === 'number') order = Math.trunc(ro)
      else if (typeof ro === 'string' && /^-?\d+$/.test(ro.trim())) order = parseInt(ro.trim(), 10)

      const doc: ContentDoc = {
        id: rel,
        path: rel,
        url: cleanUrl(rel),
        title: (fm['title'] as string) || disp,
        part: part.name,
        order,
        tags: Array.isArray(fm['tags']) ? (fm['tags'] as unknown[]).map(String) : [],
        images: extractImages(body, fp, srcDir),
        checksum: sha256Hex(normalizeTextForHash(raw)),
      }
      // difficulty 仅在明确为 1/2/3 时输出（与 Python `in (1,2,3)` 同口径）
      const d = fm['difficulty']
      if (d === 1 || d === 2 || d === 3) doc.difficulty = d as 1 | 2 | 3
      docs.push(doc)
    }
  }

  // ---- 一致性校验（ARCHITECTURE §3.1 构建时强校验）----
  const seenId = new Set<string>()
  const seenUrl = new Set<string>()
  for (const d of docs) {
    if (seenId.has(d.id)) errors.push(`id 重复: ${d.id}`)
    if (seenUrl.has(d.url)) errors.push(`url 重复: ${d.url}`)
    seenId.add(d.id)
    seenUrl.add(d.url)
  }

  const summarySet = new Set(docs.map((d) => d.id))
  const skip = new Set(['index.md', 'SUMMARY.md', 'LICENSE-docs.md'])
  walk(srcDir, (rel) => {
    if (!rel.endsWith('.md')) return
    if (skip.has(rel) || rel.startsWith('.vitepress')) return
    if (!summarySet.has(rel)) errors.push(`磁盘有但 SUMMARY 未登记: ${rel}`)
  })

  if (errors.length) {
    for (const e of errors) console.error('[ERROR] ' + e)
    console.error(`manifest 一致性校验失败，共 ${errors.length} 处`)
    process.exit(1)
  }

  const overall = createHash('sha256')
    .update(docs.map((d) => `${d.id}\t${d.checksum}`).join('\n'), 'utf8')
    .digest('hex')

  return {
    appId,
    revision: 'sha256-' + overall.slice(0, 16),
    docs,
  }
}

export function fingerprint(manifest: ContentManifest, srcDir: string): ManifestFingerprint {
  return {
    appId: manifest.appId,
    revision: manifest.revision,
    docCount: manifest.docs.length,
    titles: manifest.docs.map((d) => d.title),
    imageTotal: manifest.docs.reduce((a, d) => a + d.images.length, 0),
    svgCount: countSvg(srcDir),
    overallChecksum: '',
  }
}
