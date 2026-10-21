---
id: chip-selection
title: 常用芯片选型速查
part: 10
chapter: 附录
order: 20
tags: [芯片选型, 运放, LDO, DC-DC, MOSFET, 接口, MCU, 速查]
difficulty: 2
status: published
sources:
  - https://github.com/kitspace/awesome-electronics
  - https://www.ti.com/lit/an/slod006b/slod006b.pdf
---

# 附录 D · 常用芯片选型速查

按功能分类列出工程中最常见、最易采购的型号。参数为典型值，正式设计前务必核对最新 datasheet（数据手册）。厂商型号归各自所有。

## D.1 运算放大器 Op-Amp

| 型号 | 厂商 | 关键参数 | 典型用途/备注 |
|---|---|---|---|
| LM358 / LM2904 | TI / onsemi | 双运放，单电源 3~32V，GBP ≈ 1MHz，便宜 | 入门通用、面包板首选，BJT 输入 |
| TL072 / TL082 | TI / onsemi | 双 JFET 输入运放，GBP ≈ 3MHz，低噪声 | 音频、传感器高阻输入 |
| NE5532 | TI / onsemi | 双低噪声音频运放，GBP ≈ 10MHz | 音频前置、发烧级 |
| OPA2333 | TI | CMOS 零漂移，$V_{OS}<10\mu V$，1.8~5.5V 单电源 | 精密小信号、电池设备 |
| MCP6002 | Microchip | CMOS 双运放，1.8~5.5V，轨到轨 I/O | 低成本 3.3V/5V 通用 |
| AD8051 | ADI | 高速电压反馈型，−3dB 带宽 110MHz(G=+1)，SR 145V/µs | 高速缓冲、视频 |
| LM324 | TI / onsemi | 四运放，单电源，最便宜通用 | 多通道低成本模拟 |
| OPA2188 | TI | 零漂移精密运放，36V 供电，低偏置 | 工业精密测量 |

## D.2 比较器 Comparator

| 型号 | 厂商 | 关键参数 | 典型用途/备注 |
|---|---|---|---|
| LM339 | TI / onsemi | 四比较器，集电极开路输出，单电源 | 最通用、最便宜 |
| LM311 | TI / onsemi | 单高速比较器，可调输出 | 电压检测、过流保护 |
| TLV3201 | TI | 单高速比较器，40ns，推挽输出 | 高速阈值检测 |
| MCP6541 | Microchip | 纳安功耗比较器，开漏 | 电池供电省电检测 |

## D.3 电压基准 Voltage Reference

| 型号 | 厂商 | 关键参数 | 典型用途/备注 |
|---|---|---|---|
| LM4040 | TI / Microchip | 2.5V/4.096V/5V，±0.1%，低功耗 | ADC 基准常用 |
| REF3030 | TI | 3.0V 基准，±0.2%，SOT-23 | 3.3V 系统 ADC 基准 |
| ADR4525 | ADI | 2.5V 超高精度基准，低噪声 | 精密仪器、校准 |
| TL431 | TI / 多家 | 可调并联基准（2.5V 起步），2.5~36V | 可调稳压、电源反馈 |

## D.4 LDO 线性稳压器

| 型号 | 厂商 | 关键参数 | 典型用途/备注 |
|---|---|---|---|
| AMS1117-3.3 | AMS / 多家 | 1A，固定 3.3V/5V，压差 ≈ 1.2V | 最常见、最便宜，注意散热 |
| XC6206-3.3 | Torex | 200mA，压差 ≈ 250mV，SOT-23 | 小电流 3.3V，电池设备 |
| HT7333 | Holtek | 250mA，低功耗，SOT-89 | 低成本 3.3V |
| TPS73633 | TI | 400mA，低噪声，高 PSRR | 模拟/ADC 干净电源 |
| LT1763 | ADI (Linear) | 500mA，低噪声，高 PSRR | 精密模拟供电 |
| ME6211 | 南京微盟 | 500mA，低压差，SOT-23-5 | 国产常用替代 |

## D.5 DC-DC 开关电源

| 型号 | 厂商 | 关键参数 | 典型用途/备注 |
|---|---|---|---|
| LM2596 | TI | 3A Buck，固定/可调，150kHz | 经典模块，效率一般但好做 |
| MP1584 | MPS | 3A Buck，1.5MHz，可调 0.8~VIN | 模块/小板常用，体积小 |
| XL4015 | 芯龙 | 5A Buck，180kHz，4~38V 输入 | 大电流降压模块 |
| TPS5430 | TI | 3A Buck，宽输入 5.5~36V | 工业宽压 |
| SY8120 | Silergy | 2A 同步 Buck，高频 | 手机/便携设备 |
| MT3608 | 西安民展 | 升压 Boost，2A，2~24V | 常用升压模块 |
| XL6009 | 芯龙 | 升压 Boost，4A 开关管 | 大电流升压模块 |
| LM2577 | TI | 升压 Flyback/Buck-Boost | 经典升压 |

## D.6 MOSFET 栅极驱动器

| 型号 | 厂商 | 关键参数 | 典型用途/备注 |
|---|---|---|---|
| TC4427 | Microchip | 双 1.5A 栅驱，反相/同相可选 | 驱动功率 MOSFET |
| UCC27511 | TI | 单 4A 栅驱，高速 | 高频同步 Buck 上管 |
| IRS2003 | Infineon | 半桥栅驱，自举 | H 桥/半桥驱动 |
| EG2133 | 屹晶微 | 半桥驱动，国产替代 IR2103 | 电机驱动 |

## D.7 逻辑电平转换

| 型号 | 厂商 | 关键参数 | 典型用途/备注 |
|---|---|---|---|
| TXS0108E | TI | 8 路双向电压转换，1.65~5.5V | 3.3V↔5V 通用双向 |
| 74LVC1T45 | TI | 单路双向方向控制 | 1 位电平转换 |
| BSS138 分立 | ON/Vishay | 单 NMOS 双向转换 | I²C 电平转换经典电路 |
| 74LVC245 | TI | 8 路总线收发器，方向控制 | 5V→3.3V 单向缓冲 |

## D.8 接口收发器

| 型号 | 厂商 | 关键参数 | 典型用途/备注 |
|---|---|---|---|
| MAX485 / SP3485 | Maxim / Sipex | RS-485 收发器，半双工 | 工业总线最常用 |
| MAX3232 | Maxim / 多家 | RS-232 收发器，3.3V/5V | TTL↔RS-232 串口 |
| ADM2483 | ADI | 隔离型 RS-485 | 隔离工业总线 |
| CH340G | 沁恒 | USB↔UART 桥 | 最常见 USB 转串口 |
| CP2102 | Silicon Labs | USB↔UART 桥 | 替代 FT232，常用 |
| FT232RL | FTDI | USB↔UART 桥 | 工业级经典 |
| SN65HVD230 | TI | CAN 收发器 | 汽车/工业 CAN |
| ADUM1201 | ADI | 双通道数字隔离器 | 隔离 SPI/UART |

## D.9 MCU 微控制器

| 型号 | 厂商 | 关键参数 | 典型用途/备注 |
|---|---|---|---|
| STM32F103C8T6 | ST | Cortex-M3 72MHz，64KB Flash，LQFP48 | 最流行学习/产品 MCU |
| STM32G030K8T6 | ST | Cortex-M0+ 64MHz，低成本 | 国产替代、入门 |
| ESP32-C3 | 乐鑫 | RISC-V 160MHz，WiFi/BLE | 物联网、无线 |
| ESP32-WROOM-32 | 乐鑫 | Xtensa 双核 240MHz，WiFi/BLE | IoT、智能家居 |
| CH32V203 | 沁恒 | RISC-V 144MHz，国产 | STM32 替代 |
| ATmega328P | Microchip | AVR 16MHz，Arduino Uno | 经典开源硬件 |
| STM32F407VGT6 | ST | Cortex-M4 168MHz，高性能 | 高级应用、FPU |

## D.10 存储器 Memory

| 型号 | 厂商 | 关键参数 | 典型用途/备注 |
|---|---|---|---|
| W25Q64JV | Winbond | 8MB（64Mbit）SPI Flash | 外部程序/数据存储 |
| W25Q128JV | Winbond | 16MB SPI Flash | 大容量存储 |
| 24C02 | 多家 | 2Kbit I²C EEPROM | 小参数存储（校准数据） |
| 25LC256 | Microchip | 32KB SPI EEPROM | 大参数存储 |
| FM24V02 | Cypress | 2Kbit I²C FRAM | 高速写入、无限擦写 |

## D.11 电池充电管理

| 型号 | 厂商 | 关键参数 | 典型用途/备注 |
|---|---|---|---|
| TP4056 | 南京拓微 | 1A 线性锂电池充电，SOP-8 | 最常见 18650 充电模块 |
| MCP73831 | Microchip | 500mA 线性充电，SOT-23 | 小电流便携设备 |
| BQ24072 | TI | 1.5A 带电源路径管理充电 | 边充边放、OTG |
| CN3065 | 如韵 | 1A 锂电充电，国产 | TP4056 替代 |
| TP5000 | 南京拓微 | 2A 开关充电 | 大电流充电 |

::: pitfall 选型注意：别只看标称参数
- **电源电流余量**：LDO/DC-DC 标称 1A 不等于能持续输出 1A，需算散热与铜箔。
- **逻辑电平不匹配**：3.3V MCU 直连 5V 传感器可能读不到高电平或损坏 IO，加电平转换。
- **最小负载**：某些 DC-DC（尤其是不连续模式）轻载时效率暴跌或输出飘，加假负载。
- **替代型号封装/引脚**：即使同型号名，不同厂商或尾缀可能引脚不同，换料务必核对脚图。
:::

> 以上型号仅为工程常用代表，不构成选型保证；具体设计请以最新 datasheet 与应用笔记为准。
