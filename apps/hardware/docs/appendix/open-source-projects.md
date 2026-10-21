---
id: open-source-projects
title: 开源优秀硬件作品赏析
part: 10
chapter: 附录
order: 45
tags: [开源硬件, GitHub, Arduino, KiCad, SDR, RTOS, 学习]
difficulty: 2
status: published
sources:
  - https://github.com/kitspace/awesome-electronics
  - https://github.com/nhivp/Awesome-Embedded
---

# 附录 I · 开源优秀硬件作品赏析

精选 19 个真实可查的开源硬件与嵌入式生态项目，按类别分组。每条给出仓库链接、一句话简介、License 与可学点。star 数随时间变化，不标注以免过时；链接均为官方仓库。

## I.1 开源硬件设备

| 项目 | 仓库 | 简介 | License | 可学点 |
|---|---|---|---|---|
| Arduino Core AVR | https://github.com/arduino/ArduinoCore-avr | Arduino AVR 平台核心源码与板级定义 | LGPL-2.1 | MCU 板级支持包（BSP）如何组织 |
| HackRF One | https://github.com/greatscottgadgets/hackrf | 开源软件无线电（SDR）硬件，1MHz–6GHz | GPL-2.0 | 宽带射频前端、FPGA+MCU 架构 |
| GreatFET One | https://github.com/greatscottgadgets/greatfet | 开源 USB 多用途硬件工具（协议分析/调试） | GPL-3.0 | LPC4330 双核架构、可扩展外设 |
| PortaPack Mayhem | https://github.com/portapack-mayhem/mayhem-firmware | 配合 HackRF 的手持 SDR 固件与 UI（活跃 fork） | GPL-3.0 | MCU 驱动 LCD/触摸屏、实时信号处理 |
| DSView | https://github.com/DreamSourceLab/DSView | 开源 USB 逻辑分析仪软件（原 DSLogic 上位机） | GPL-3.0 | 高速采样、协议解析、USB 传输 |

## I.2 调试与测量工具

| 项目 | 仓库 | 简介 | License | 可学点 |
|---|---|---|---|---|
| Black Magic Debug | https://github.com/blackmagic-debug/blackmagic | 开源 JTAG/SWD 调试器固件（用于 STM32/ARM） | BSD-3-Clause | SWD 协议、CMSIS-DAP、调试器架构 |
| OpenOCD | https://github.com/openocd-org/openocd | 开源片上调试（On-Chip Debugging）工具 | GPL-2.0 | JTAG/SWD 协议栈、与 GDB 配合 |
| sigrok PulseView | https://github.com/sigrokproject/pulseview | 开源信号分析 GUI，解析 I²C/SPI/UART | GPL-3.0 | 多协议解码、跨硬件抽象 |
| logisim-evolution | https://github.com/logisim-evolution/logisim-evolution | 开源数字逻辑设计与仿真工具 | GPL-3.0 | 门电路建模、时序仿真引擎 |

## I.3 EDA 与设计工具

| 项目 | 仓库 | 简介 | License | 可学点 |
|---|---|---|---|---|
| KiCad | https://github.com/KiCad/kicad-source-mirror | 开源 EDA 套件，原理图+PCB 全流程 | GPL-3.0 | 原理图/PCB 数据模型、封装体系 |
| awesome-electronics | https://github.com/kitspace/awesome-electronics | 电子工程师资源精选清单 | CC0-1.0 | 如何检索与评估学习资源 |

## I.4 MCU 开发框架与 RTOS

| 项目 | 仓库 | 简介 | License | 可学点 |
|---|---|---|---|---|
| ESP-IDF | https://github.com/espressif/esp-idf | 乐鑫 ESP32 官方开发框架 | Apache-2.0 | WiFi/BLE 协议栈、MCU 驱动架构 |
| STM32duino Core | https://github.com/stm32duino/Arduino_Core_STM32 | 在 STM32 上跑 Arduino API | LGPL-2.1 | 如何把 HAL 封装成易用 API |
| ChibiOS | https://github.com/ChibiOS/ChibiOS | 轻量嵌入式 RTOS | GPLv3 / Apache-2.0 双许可 | 实时内核调度、线程模型 |
| FreeRTOS | https://github.com/FreeRTOS/FreeRTOS | 最广泛使用的开源实时内核 | MIT | 任务调度、队列、信号量实现 |
| CircuitPython | https://github.com/adafruit/circuitpython | 在微控制器上跑 Python | MIT | 解释器移植、硬件抽象设计 |

## I.5 图形与中间件

| 项目 | 仓库 | 简介 | License | 可学点 |
|---|---|---|---|---|
| LVGL | https://github.com/lvgl/lvgl | 开源嵌入式图形库（GUI） | MIT | 小屏幕 UI 渲染、控件体系 |
| TinyUSB | https://github.com/hathach/tinyusb | 开源 USB 协议栈（Device/Host） | MIT | USB 枚举、类驱动、多设备支持 |
| Awesome-Embedded | https://github.com/nhivp/Awesome-Embedded | 嵌入式学习资源精选清单 | Unlicense | 嵌入式学习路径与工具链选型 |

## I.6 学习建议

::: motivation 怎么"赏析"开源硬件
- **先读 README 与硬件设计文档**：看它解决什么问题、架构怎么分（MCU/FPGA/模拟前端）。
- **Clone 仓库看目录结构**：固件怎么分层（BSP/驱动/中间件/应用），可直接套用到自己项目。
- **重点看 schematic 与 layout**：如 HackRF/GreatFET 的射频前端、去耦、屏蔽做法，比书本直观。
- **License 意识**：GPL 类传染性强，商业产品直接抄代码要小心；MIT/BSD/Apache 宽松，可放心参考。
- **从能跑的最小 demo 开始**：先把 Blinky/串口跑通，再逐层读驱动。
:::

> 以上项目均为公开活跃仓库；若某仓库已归档或更名，请以 GitHub 搜索最新官方地址为准。不编造 star 数与下载量。
