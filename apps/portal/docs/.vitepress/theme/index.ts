// 门户主题：无学习/目录，渲染路书品牌 + 分册卡片（数据来自 content.config）。
import { createPortalTheme } from '@lubook/theme'
import { PORTAL_CARDS, TAGLINE, INTRO } from '../../../content.config'

export default createPortalTheme({
  cards: PORTAL_CARDS,
  tagline: TAGLINE,
  intro: INTRO
})
