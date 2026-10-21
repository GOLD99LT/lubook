// 门户薄 config：通用规则来自 @lubook/shared-config；无侧边栏/导航（门户无章节目录）。
// base 由 VP_BASE 派生（portal -> base=VP_BASE）。
import { defineBookConfig } from '@lubook/shared-config'
import { APP_ID, TITLE, DESCRIPTION, FAVICON } from '../../content.config'

export default defineBookConfig({
  appId: APP_ID,
  title: TITLE,
  description: DESCRIPTION,
  partRegistry: {},
  favicon: FAVICON
})
