// @lubook/shared-config —— defineBookConfig：VitePress 通用 markdown/搜索/插件工厂。
//
// 边界铁律：本包只封装与具体站点无关的通用规则（五类容器、KaTeX、CJK 加粗、
// details 折叠、ECharts 围栏、figure 化、frontmatter 修复、本地搜索中文、
// 难度默认名、统一 vite.ssr.noExternal）。手册特有的 nav/sidebar/篇名/站名
// 一律由 options 传入，本包不读取任何 app 的私有路径。
//
// 源码即产物（TS）：VitePress 直接消费 src/index.ts，无需预构建。

import type { DefaultTheme, HeadConfig, UserConfig } from 'vitepress'
import container from 'markdown-it-container'
import katexPkg from '@vscode/markdown-it-katex'

// 兼容 CJS/ESM 互操作：可能拿到 { default: fn } 或 fn 本身
const katex: any = (katexPkg as any).default || katexPkg

// ---------------------------------------------------------------------------
// 前置插件：归一化 frontmatter 标量值中未加引号的 ": "（仅在线构建，磁盘 md 零改动）。
// 离线版用宽松 YAML 解析器可直接接受 "title: 中文 English: Sub"，但 VitePress 的
// gray-matter 是严格 YAML，遇到值里的 ": " 会报 mapping 错误。这里在构建期把这类
// 标量值补成双引号，不动源文件。
// ---------------------------------------------------------------------------
function fixFrontmatterPlugin() {
  return {
    name: 'hh-fix-frontmatter',
    enforce: 'pre',
    transform(code: string, id: string) {
      if (!id.endsWith('.md') || id.includes('.vitepress')) return null
      const m = code.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/)
      if (!m) return null
      const fm = m[1]
      const fixed = fm
        .split(/\r?\n/)
        .map((line) => {
          // 仅处理顶层标量键（非缩进、非块数组项），值里含 ": " 就补引号
          const tm = line.match(/^([A-Za-z_][\w-]*):\s*(.+)$/)
          if (!tm) return line
          const key = tm[1]
          const val = tm[2].trim()
          if (key === 'tags' || val.startsWith('[')) return line // 已是内联数组
          if (!/:\s+\S/.test(val)) return line // 无冒号分隔，安全
          if (val.startsWith('"') || val.startsWith("'")) return line // 已加引号
          const escaped = val.replace(/\\/g, '\\\\').replace(/"/g, '\\"')
          return `${key}: "${escaped}"`
        })
        .join('\n')
      if (fixed === fm) return null
      return code.replace(m[0], '---\n' + fixed + '\n---\n')
    }
  }
}

// ---------------------------------------------------------------------------
// 难度默认名（通用，与具体站点无关）
// ---------------------------------------------------------------------------
const DIFF_NAMES: Record<number, string> = { 1: '入门', 2: '进阶', 3: '深入' }

function escHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

// ---------------------------------------------------------------------------
// markdown-it 扩展：五类容器（标题表通用，站点可用 options 覆盖默认文案）
// ---------------------------------------------------------------------------
export const CONTAINER_TITLES: Record<string, string> = {
  motivation: '设计动机',
  analogy: '直觉类比',
  example: '设计示例',
  pitfall: '常见坑',
  advanced: '进阶内容（可跳过）'
}

function makeContainerRender(type: string, md: any, titles: Record<string, string>) {
  return (tokens: any[], idx: number) => {
    const token = tokens[idx]
    if (token.nesting === 1) {
      const raw = (token.info || '').trim().slice(type.length).trim()
      const title = raw || titles[type]
      // 行内渲染标题（支持 $公式$ / `代码`）
      const inline = md.renderer.renderInline(md.parseInline(title, {}), md.options, {})
      if (type === 'advanced') {
        return `<details class="hh-container hh-advanced"><summary class="hh-advanced-title">${inline}</summary>\n`
      }
      return `<div class="hh-container hh-${type}"><div class="hh-c-title">${inline}</div>\n`
    }
    return type === 'advanced' ? '</details>\n' : '</div>\n'
  }
}

// ---------------------------------------------------------------------------
// 注入面包屑 + 难度/标签徽章（在每个内容页顶部）。
// 篇名不再写死，改由 partRegistry（篇号 -> 篇名）查找。
// ---------------------------------------------------------------------------
function makePageHeadRuler(partRegistry: Record<number, string>) {
  return function pageHeadRuler(state: any) {
    // 内层渲染（折叠题答案）不应重复注入面包屑/徽章
    if (state.env && state.env.__innerBlock) return
    const fm = state.env && state.env.frontmatter
    if (!fm) return
    const hasDiff = fm.difficulty != null
    const hasTags = Array.isArray(fm.tags) && fm.tags.length > 0
    if (!hasDiff && !hasTags) return

    let html = ''
    // 面包屑
    const crumbs: string[] = []
    if (fm.part != null && partRegistry[fm.part]) crumbs.push(partRegistry[fm.part])
    if (fm.chapter) crumbs.push(String(fm.chapter))
    if (crumbs.length) {
      html +=
        '<nav class="hh-crumb">' +
        crumbs.map(escHtml).join(' <span class="hh-crumb-sep">/</span> ') +
        '</nav>'
    }
    // 徽章
    let badges = ''
    if (hasDiff) {
      badges += `<span class="hh-badge hh-diff-${fm.difficulty}">${DIFF_NAMES[fm.difficulty] || ''}</span>`
    }
    if (hasTags) {
      for (const t of fm.tags) badges += `<span class="hh-badge hh-tag">#${escHtml(String(t))}</span>`
    }
    if (badges) html += `<div class="hh-badges">${badges}</div>`

    const block = new state.Token('html_block', '', 0)
    block.block = true
    block.content = html + '\n'
    state.tokens.unshift(block)
  }
}

// ---------------------------------------------------------------------------
// ECharts 围栏 -> 全局 <EChart :option=.../>
// ---------------------------------------------------------------------------
function echartsFenceRender(defaultFence: any) {
  return (tokens: any[], idx: number, options: any, env: any, self: any) => {
    const token = tokens[idx]
    const info = (token.info || '').trim()
    const lang = info.split(/\s+/)[0]
    if (lang === 'echarts') {
      const raw = token.content.trim()
      let compact = raw
      try {
        compact = JSON.stringify(JSON.parse(raw))
      } catch (e) {
        // JSON 非法时原样抛出，由 EChart 组件 console 暴露
      }
      // 单引号转义（属性用单引号包裹）
      const safe = compact.replace(/\\/g, '\\\\').replace(/'/g, '\\u2019')
      return `<EChart :option='${safe}' />\n`
    }
    return defaultFence(tokens, idx, options, env, self)
  }
}

// ---------------------------------------------------------------------------
// CJK 加粗修复：CommonMark emphasis flanking 规则在「全角标点/CJK 紧邻 **」时
// 判失败（如 **Buck（…）**是、**正确。**虚短），导致中文加粗星号裸露。
// 替换内置 emphasis 内联规则：仍走 state.scanDelims，仅当 * 分隔符紧贴 CJK/全角
// 标点时放宽 open/close；_ 分隔符与 ASCII 边界（2*3*4、a*b）维持原判定。
// ---------------------------------------------------------------------------
function isCJKBoundary(ch: number): boolean {
  return (
    (ch >= 0x4e00 && ch <= 0x9fff) || // CJK 统一表意
    (ch >= 0x3000 && ch <= 0x303f) || // CJK 标点
    (ch >= 0xff00 && ch <= 0xffef) || // 全角形式
    (ch >= 0x3400 && ch <= 0x4dbf) // 扩展 A
  )
}
function cjkAwareEmphasis(state: any, silent: boolean): boolean {
  const marker = state.src.charCodeAt(state.pos)
  if (marker !== 0x2a /* * */ && marker !== 0x5f /* _ */) return false
  const scanned = state.scanDelims(state.pos, true)
  if (marker === 0x2a) {
    const before = state.pos > 0 ? state.src.charCodeAt(state.pos - 1) : 0
    const after =
      state.pos + scanned.length < state.src.length
        ? state.src.charCodeAt(state.pos + scanned.length)
        : 0
    if (isCJKBoundary(before) || isCJKBoundary(after)) {
      scanned.can_open = true
      scanned.can_close = true
    }
  }
  for (let i = 0; i < scanned.length; i++) {
    const token = state.push('text', '', 0)
    token.content = String.fromCharCode(marker)
    state.delimiters.push({
      marker,
      length: scanned.length,
      token: state.tokens.length - 1,
      end: -1,
      open: scanned.can_open,
      close: scanned.can_close
    })
  }
  state.pos += scanned.length
  return true
}

// ---------------------------------------------------------------------------
// 原生 <details> 折叠题内 Markdown 解析（块解析前的 core ruler）。
// markdown-it 把 <details> 当原生 HTML 块，summary 不做 inline 解析，
// 内部 $公式$ / **加粗** / 列表 无法渲染。这里在 block 分词前，按标签深度
// 平衡提取每个 <details>...</details>，summary 走 renderInline、答案正文走
// render（完整块级），输出单行 HTML（无空行，markdown-it 视为一个 html_block）。
// 递归自然支持 ::: advanced 容器内嵌套的 <details>（render 会再次走本 ruler）。
// ---------------------------------------------------------------------------
function renderDetailsBlock(block: string, md: any, env: any): string {
  let rest = block
  let q = ''
  const sm = block.match(/<summary>([\s\S]*?)<\/summary>/)
  if (sm) {
    q = sm[1].trim()
    rest = block.slice(sm.index + sm[0].length)
  }
  // 去掉首尾的 <details ...> / </details>
  rest = rest.replace(/^<details[^>]*>/, '').replace(/<\/details>\s*$/, '').trim()
  // 内层渲染：标记 env，避免重复注入面包屑/徽章
  const prev = env && env.__innerBlock
  if (env) env.__innerBlock = true
  let qHtml = ''
  let aHtml = ''
  try {
    qHtml = md.renderInline(q, env).trim()
    aHtml = md.render(rest, env).trim()
  } finally {
    if (env) env.__innerBlock = prev
  }
  // 压成单行，避免块解析器因空行把 details 拆成多个 html_block
  return `<details><summary>${qHtml}</summary>${aHtml}</details>`.replace(/\s*\n\s*/g, '')
}

// 放宽的行内数学规则：开 $ 前不能是单词字符（保持严格，防货币误配），
// 闭 $ 后允许紧跟单位字母（\mu$s、$...$V 等）。产出 math_inline token，
// 渲染器由 @vscode/markdown-it-katex 注册。
function relaxedMathInline(state: any, silent: boolean): boolean {
  if (state.src[state.pos] !== '$') return false
  const prev = state.pos > 0 ? state.src[state.pos - 1] : ''
  if (prev === '\\') return false
  if (prev && /[\w\d]/.test(prev)) return false
  const start = state.pos + 1
  let match = state.src.indexOf('$', start)
  if (match === -1) {
    if (!silent) state.pending += '$'
    state.pos++
    return true
  }
  // 跳过转义 \$
  let p = match - 1
  while (state.src[p] === '\\') p--
  if (((match - p) % 2) === 0) {
    if (!silent) state.pending += '$'
    state.pos++
    return true
  }
  if (match - start === 0) {
    if (!silent) state.pending += '$$'
    state.pos += 2
    return true
  }
  if (!silent) {
    const tok = state.push('math_inline', 'math', 0)
    tok.markup = '$'
    tok.content = state.src.slice(start, match)
  }
  state.pos = match + 1
  return true
}

function detailsRuler(md: any) {
  return (state: any) => {
    const src = state.src
    if (src.indexOf('<details') === -1) return
    let out = ''
    let pos = 0
    while (pos < src.length) {
      const open = src.indexOf('<details', pos)
      if (open === -1) {
        out += src.slice(pos)
        break
      }
      const openTagEnd = src.indexOf('>', open)
      if (openTagEnd === -1) {
        out += src.slice(pos)
        break
      }
      // 平衡匹配（支持嵌套 details）
      let depth = 1
      let j = openTagEnd + 1
      let broken = false
      while (depth > 0) {
        const nOpen = src.indexOf('<details', j)
        const nClose = src.indexOf('</details>', j)
        if (nClose === -1) {
          broken = true
          break
        }
        if (nOpen !== -1 && nOpen < nClose) {
          depth++
          j = nOpen + 8
        } else {
          depth--
          j = nClose + '</details>'.length
        }
      }
      if (broken) {
        out += src.slice(pos)
        break
      }
      out += src.slice(pos, open)
      out += renderDetailsBlock(src.slice(open, j), md, state.env) + '\n'
      pos = j
    }
    state.src = out
  }
}

// ---------------------------------------------------------------------------
// 图片 Figure 化（块级）：core ruler 把「段落内仅含一张图」的
// paragraph_open / inline / paragraph_close 三个 token 整体替换为一个
// <figure class="md-figure">…<figcaption> html_block。
// 必须块级输出：若把 <figure> 留在 <p> 内，浏览器解析时会提前闭合 <p>，
// 造成 SSR DOM 与 Vue 水合 vnode 结构不一致（hydration mismatch），
// 并连带使 EChart 等组件被重复挂载（空灰盒）。
// ---------------------------------------------------------------------------
function loneFigureRuler(md: any) {
  return (state: any) => {
    const tokens = state.tokens
    for (let i = 0; i < tokens.length; i++) {
      if (tokens[i].type !== 'paragraph_open') continue
      const inline = tokens[i + 1]
      if (!inline || inline.type !== 'inline') continue
      const ch = inline.children || []
      const meaningful = ch.filter(
        (t: any) => !(t.type === 'text' && t.content.trim() === '')
      )
      if (!(meaningful.length === 1 && meaningful[0].type === 'image')) continue
      const imgTok = meaningful[0]
      // 用默认 image 规则渲染 <img>（保留相对路径/打包/懒加载属性）
      const imgHtml = (md.renderer.rules.image as any)([imgTok], 0, md.options, state.env, md.renderer)
      const alt = imgTok.content || ''
      const fig = alt
        ? `<figure class="md-figure">${imgHtml}<figcaption>${escHtml(alt)}</figcaption></figure>`
        : `<figure class="md-figure">${imgHtml}</figure>`
      const block = new state.Token('html_block', '', 0)
      block.block = true
      block.content = fig + '\n'
      tokens.splice(i, 3, block)
    }
  }
}

// ---------------------------------------------------------------------------
// 本地搜索中文翻译（按钮/modal 文案，通用）
// ---------------------------------------------------------------------------
const DEFAULT_LOCAL_SEARCH: DefaultTheme.Config['search'] = {
  provider: 'local',
  options: {
    translations: {
      button: { buttonText: '搜索', buttonAriaLabel: '搜索文档' },
      modal: {
        displayDetails: '显示详情',
        resetButtonTitle: '清除查询',
        backButtonTitle: '关闭',
        noResultsText: '无法找到相关结果',
        footer: { selectText: '选择', navigateText: '切换' }
      }
    }
  }
}

export const PACKAGE_NAME = '@lubook/shared-config' as const
export const VERSION = '0.1.0' as const
/** 多 app 部署的默认根 base：本地 dev/build 默认根相对（门户 '/'、分册 '/<slug>/'）。 */
export const DEFAULT_VP_BASE = '/' as const

/** 归一化 base：保证以 '/' 开头、以 '/' 结尾（VitePress 要求 base 首尾为斜杠）。 */
export function normalizeBase(vp: string): string {
  let b = vp.trim()
  if (!b.startsWith('/')) b = '/' + b
  if (!b.endsWith('/')) b = b + '/'
  return b
}

/**
 * 由 VP_BASE 派生各 app 的 base（ADR-0006 / NAMING）：
 *   门户 portal  → base = VP_BASE
 *   内容分册     → base = VP_BASE + '<slug>/'
 * 部署取值：GitHub Pages VP_BASE='/lubook/'；Cloudflare VP_BASE='/'；本地默认 '/'。
 * 显式 options.base 优先（保留单点覆盖能力）。
 */
export function deriveBase(appId: string, vpBase?: string, explicit?: string): string {
  if (explicit) return normalizeBase(explicit)
  const vp = normalizeBase(vpBase || process.env.VP_BASE || DEFAULT_VP_BASE)
  if (appId === 'portal') return vp
  return vp + appId + '/'
}

/** defineBookConfig 入参：站点特有项全部由 app 传入，通用规则由本包封装。 */
export interface BookConfigOptions {
  /** 应用标识（多 app 隔离用，注入 <meta name="app-id">） */
  appId: string
  /** 站点标题 */
  title: string
  /** 站点描述 */
  description?: string
  /** base 子路径；不传则由 VP_BASE 派生（门户=VP_BASE，分册=VP_BASE+'<slug>/'） */
  base?: string
  /** 语言，默认 'zh-CN' */
  lang?: string
  /** 顶部导航（站点特有） */
  nav?: DefaultTheme.NavItem[]
  /** 侧边栏（站点特有） */
  sidebar?: DefaultTheme.Sidebar
  /** 篇号 -> 篇名映射（面包屑 pageHead 用，取代写死的 PART_NAMES） */
  partRegistry: Record<number, string>
  /** 社交链接 */
  socialLinks?: DefaultTheme.SocialLink[]
  /** favicon 路径（相对 base，如 'favicon.svg'）；不传则不注入 icon head */
  favicon?: string
  /** 自定义搜索配置；不传则默认本地搜索 + 中文文案 */
  search?: DefaultTheme.Config['search']
}

/**
 * 工厂：封装 config.mts 里的全部通用 markdown/搜索/插件规则，返回 VitePress UserConfig。
 * 站点特有的 nav/sidebar/篇名/站名不写死，全部来自 options。
 */
export function defineBookConfig(options: BookConfigOptions): UserConfig {
  const base = deriveBase(options.appId, process.env.VP_BASE, options.base)
  const lang = options.lang ?? 'zh-CN'

  const head: HeadConfig[] = [['meta', { name: 'app-id', content: options.appId }]]
  if (options.favicon) {
    const attrs: Record<string, string> = { rel: 'icon', href: base + options.favicon }
    if (options.favicon.endsWith('.svg')) attrs.type = 'image/svg+xml'
    head.push(['link', attrs])
  }

  const containerTypes = ['motivation', 'analogy', 'example', 'pitfall', 'advanced']

  return {
    base,
    lang,
    title: options.title,
    description: options.description,
    head,
    lastUpdated: false,
    cleanUrls: true,

    markdown: {
      theme: { light: 'github-light', dark: 'github-dark' },
      config(md) {
        // KaTeX（本地字体）
        md.use(katex as any, { throwOnError: false })
        // 放宽 math_inline 闭分隔符：原插件要求闭 $ 后不能紧跟单词字符，
        // 导致 $\mu$s、$...$V 这类「公式后紧跟单位字母」不渲染。本书无货币 $，
        // 开分隔符仍保持严格（$ 前不能是单词字符），仅放宽闭侧，安全。
        md.inline.ruler.at('math_inline', relaxedMathInline as any)
        // CJK 加粗修复（替换内置 emphasis）
        md.inline.ruler.at('emphasis', cjkAwareEmphasis as any)
        // 原生 <details> 内 markdown 解析（必须在 block 分词前）
        md.core.ruler.before('block', 'hh_details', detailsRuler(md))
        // 五类容器
        for (const t of containerTypes) {
          md.use(container as any, t, {
            marker: ':',
            render: makeContainerRender(t, md, CONTAINER_TITLES)
          })
        }
        // ECharts 围栏
        const defaultFence = md.renderer.rules.fence!.bind(md.renderer)
        md.renderer.rules.fence = echartsFenceRender(defaultFence)
        // 图片 Figure 化（core ruler，块级，避免 <p><figure> 嵌套导致水合失配）
        md.core.ruler.push('hh_lone_figure', loneFigureRuler(md))
        // 面包屑 + 徽章（篇名走 options.partRegistry）
        md.core.ruler.push('hh_page_head', makePageHeadRuler(options.partRegistry) as any)
      }
    },

    vite: {
      plugins: [fixFrontmatterPlugin() as any],
      // 统一：源码 TS 包（@lubook/*）不做预构建
      ssr: { noExternal: [/@lubook\//] }
    },

    themeConfig: {
      nav: options.nav,
      sidebar: options.sidebar,
      outline: { level: [2, 3], label: '本页大纲' },
      docFooter: { prev: '上一章', next: '下一章' },
      darkModeSwitchLabel: '主题',
      sidebarMenuLabel: '目录',
      returnToTopLabel: '回到顶部',
      search: options.search ?? DEFAULT_LOCAL_SEARCH,
      socialLinks: options.socialLinks
    } as DefaultTheme.Config
  }
}
