// 薄 config：通用规则全部来自 @lubook/shared-config，站点数据来自 content.config。
// sidebar 为预构建生成物（gen:sidebar）；base 由 VP_BASE 环境变量派生
// （门户=VP_BASE，分册=VP_BASE+'<slug>/'，详见 ADR-0006）。
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
  base: '/',
  nav: NAV,
  sidebar,
  partRegistry: PART_REGISTRY,
  socialLinks: SOCIAL_LINKS,
  favicon: FAVICON
})
