// 薄 config：通用规则全部来自 @lubook/shared-config，站点数据来自 content.config。
// sidebar 为预构建生成物（gen:sidebar）；nav 用 content.config 的固定导航。
import { defineBookConfig } from '@lubook/shared-config'
import sidebar from './sidebar.generated.mjs'
import {
  APP_ID,
  TITLE,
  DESCRIPTION,
  FAVICON,
  PART_REGISTRY,
  NAV,
  SOCIAL_LINKS
} from '../../content.config'

export default defineBookConfig({
  appId: APP_ID,
  title: TITLE,
  description: DESCRIPTION,
  nav: NAV,
  sidebar,
  partRegistry: PART_REGISTRY,
  socialLinks: SOCIAL_LINKS,
  favicon: FAVICON
})
