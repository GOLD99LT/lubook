// 本 app 主题：catalog 与学习仓储均来自 content.config（已在其中装配/注册）。
// 如需覆盖品牌 Logo，可传 createBookTheme({ catalog, repository, logo })。
import { createBookTheme } from '@lubook/theme'
import { catalog, repository } from '../../../content.config'

export default createBookTheme({ catalog, repository })
