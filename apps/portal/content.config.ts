// apps/portal/content.config.ts —— 路书门户配置：品牌标题 + 分册卡片集中声明。
//
// 门户无章节目录、无学习数据；本文件只声明分册卡片（ADR-0006 §4）。
// 卡片两类：
//   internal：同站分册，链接 VP_BASE + '<slug>/'（available=false 显示「即将上线」占位）
//   external：外链新标签页（本期不实际接外部站）
import type { PortalCard } from '@lubook/theme'

export const APP_ID = 'portal'
export const TITLE = '路书'
export const DESCRIPTION = '路先生知识手册：硬件、嵌入式软件、嵌入式 Linux 等多领域学习手册合集。'
export const FAVICON = 'favicon.svg'
export const TAGLINE = '路先生知识手册'
export const INTRO = '一个开源、可交互的个人知识手册合集，按领域分册，持续更新。'

export const PORTAL_CARDS: PortalCard[] = [
  {
    type: 'internal',
    slug: 'hardware',
    title: '硬件工程师手册',
    desc: '电路基础、元器件、运放、数字电路、电源、PCB 与 EMC，含原理图、设计示例与面试题库。',
    icon: 'hardware',
    available: true
  },
  {
    type: 'internal',
    slug: 'embedded',
    title: '嵌入式软件手册（MCU）',
    desc: 'Cortex-M 裸机、HAL、RTOS 任务调度、外设驱动与 MCU 软件工程实践。',
    icon: 'embedded',
    available: true
  },
  {
    type: 'internal',
    slug: 'embedded-linux',
    title: '嵌入式 Linux 手册',
    desc: 'Cortex-A、交叉编译、启动链、设备树、内核驱动、Buildroot/Yocto 与 OTA。',
    icon: 'linux',
    available: true
  }
]
