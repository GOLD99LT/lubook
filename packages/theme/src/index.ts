// @lubook/theme —— 布局 / 品牌 / 学习 UI / EChart / 图片查看器。
//
// 边界（ARCHITECTURE §4）：只依赖 CatalogProvider（app 注入）与 @lubook/learning 的
// LearningRepository（接口）；不 import 任何 app 的 sidebar，不直接读写 localStorage。
// 默认 Logo/品牌随包提供，可被 app 经 createBookTheme({ logo }) 覆盖。
import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import type { LearningRepository } from '@lubook/learning'

import Layout from './components/brand/LayoutBrand.vue'
import PortalLayout from './components/brand/PortalLayout.vue'
import PortalHome from './components/brand/PortalHome.vue'
import Logo from './components/brand/Logo.vue'
import EChart from './components/EChart.vue'
import LearningPanel from './components/learning/HomePanel.vue'
import { createLearningFacade, setLearningContext } from './components/learning/store'
import type { CatalogProvider } from './components/learning/catalog'

import 'katex/dist/katex.min.css'
import './style.css'
import './learning.css'

export const PACKAGE_NAME = '@lubook/theme' as const
export const VERSION = '0.1.0' as const

export type { CatalogEntry, CatalogProvider } from './components/learning/catalog'
export type { LearningRepository } from '@lubook/learning'
export { default as PortalHome } from './components/brand/PortalHome.vue'
export { default as BrandMark } from './components/brand/BrandMark.vue'
export type {
  ChapterStatus,
  RepositoryStats,
  ImportResult,
  FavItem,
  LearningFacade
} from './components/learning/store'

export interface BookThemeOptions {
  /** app 构造的章节目录（来自其 sidebar / content-manifest） */
  catalog: CatalogProvider
  /** @lubook/learning 提供的学习数据仓储实例 */
  repository: LearningRepository
  /** 可选：覆盖默认品牌 Logo 组件（注册为全局 <Logo>） */
  logo?: unknown
}

// ---------------------------------------------------------------------------
// 原理图点击放大：全局事件委托（监听 .md-figure img 的点击，弹固定遮罩）
// ---------------------------------------------------------------------------
let zoomInited = false
function setupFigureZoom(): void {
  if (zoomInited || typeof document === 'undefined') return
  zoomInited = true

  let overlay: HTMLDivElement | null = null
  function open(src: string, alt: string) {
    close()
    overlay = document.createElement('div')
    overlay.className = 'hh-zoom-overlay'
    overlay.innerHTML =
      '<img alt="">' + (alt ? '<div class="hh-zoom-cap"></div>' : '')
    const img = overlay.querySelector('img')!
    img.src = src
    if (alt) (overlay.querySelector('.hh-zoom-cap')!.textContent = alt)
    overlay.addEventListener('click', close)
    document.body.appendChild(overlay)
    document.body.style.overflow = 'hidden'
  }
  function close() {
    if (overlay) {
      overlay.remove()
      overlay = null
      document.body.style.overflow = ''
    }
  }
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') close()
  })
  document.addEventListener('click', (e) => {
    const img = (e.target as HTMLElement).closest('.md-figure img') as HTMLImageElement | null
    if (!img) return
    open(img.currentSrc || img.src, img.alt || '')
  })
}

/**
 * 构造硬件手册 VitePress 主题。app 侧用法：
 *
 * ```ts
 * import { createBookTheme } from '@lubook/theme'
 * import { createLocalLearningRepository } from '@lubook/learning'
 *
 * export default createBookTheme({
 *   catalog: myCatalogProvider,          // app 从 sidebar/manifest 构造
 *   repository: createLocalLearningRepository({ appId: 'handbook' })
 * })
 * ```
 */
export function createBookTheme(opts: BookThemeOptions): Theme {
  const facade = createLearningFacade(opts.repository, opts.catalog)
  setLearningContext(facade)
  // 注：LearningRepository 在 createLearningRepository() 内已自举 boot()（加载/迁移），
  // 这里无需再次触发；SSR 下仓储自动降级为内存实现，安全。

  return {
    extends: DefaultTheme,
    Layout,
    enhanceApp({ app }) {
      app.component('EChart', EChart)
      // 默认 Logo 随包提供；app 传入 opts.logo 即覆盖全局 <Logo>
      app.component('Logo', (opts.logo as any) || Logo)
      app.component('LearningPanel', LearningPanel)
      setupFigureZoom()
    }
  } satisfies Theme
}

// ---------------------------------------------------------------------------
// 门户主题：无学习/目录，仅渲染路书品牌 + 分册卡片
// ---------------------------------------------------------------------------

/** 门户分册卡片（在门户 content.config 集中声明，ADR-0006 §4）。 */
export interface PortalCard {
  /** internal=同站分册（VP_BASE+slug/）；external=外链新标签 */
  type: 'internal' | 'external'
  /** internal：分册 slug */
  slug?: string
  /** 卡片标题 */
  title: string
  /** 卡片描述 */
  desc: string
  /** 内联线性图标名（hardware/embedded/linux/external） */
  icon: string
  /** internal：false 显示「即将上线」占位（非链接） */
  available?: boolean
  /** external：外链 URL */
  url?: string
}

export interface PortalThemeOptions {
  /** 分册卡片列表 */
  cards: PortalCard[]
  /** 副标题（默认「路先生知识手册」） */
  tagline?: string
  /** 可选简介 */
  intro?: string
}

/** 门户主题工厂：注册 PortalHome，使用 PortalLayout（无侧边栏）。 */
export function createPortalTheme(opts: PortalThemeOptions): Theme {
  return {
    extends: DefaultTheme,
    Layout: PortalLayout,
    enhanceApp({ app }) {
      app.component('PortalHome', PortalHome)
      // 卡片数据通过全局属性提供给首页 md
      app.config.globalProperties.$portalCards = opts.cards
      app.config.globalProperties.$portalTagline = opts.tagline
      app.config.globalProperties.$portalIntro = opts.intro
    }
  } satisfies Theme
}

export default createBookTheme
