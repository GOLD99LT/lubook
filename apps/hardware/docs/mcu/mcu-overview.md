---
id: mcu-overview
title: MCU 概览
part: 5
chapter: MCU 基础
order: 5
tags: [MCU, 单片机, 嵌入式, Cortex-M, 架构]
difficulty: 1
status: published
sources:
  - STMicroelectronics RM0008（STM32F1 参考手册）
  - Espressif ESP32 Series Datasheet
  - https://github.com/espressif
---

# MCU 概览 MCU Overview

## 1. 设计动机

::: motivation 为什么先要理解 MCU 的硬件架构
单片机（Microcontroller Unit，MCU）不是"一台装在芯片里的小电脑"那么简单——它把 **CPU 内核、存储器、片上外设、时钟与复位、以及大量可配置 IO** 全部封进一颗芯片。硬件工程师画 MCU 板子时，要决定的不是"写什么代码"，而是：这颗芯片有多少电源脚要去耦、晶振怎么接、哪些引脚复用成什么功能、外设引脚的电气能不能直接驱动外部器件。

不理解架构就动手画板，最典型的后果是：电源脚只接了一只电容、晶振负载电容没算、把 ADC 输入接到了普通 5V 容忍脚、BOOT 脚悬空导致烧不进程序。本章先建立"一颗 MCU 内部长什么样、对外要接什么"的整体地图，后面各章再逐个外设深入。
:::

## 2. 原理图

下图是一颗通用 MCU 的片上系统（System on Chip，SoC）框图：内核经内部总线挂接 Flash、SRAM 和各种外设，对外只露出电源脚（VDD/VSS）、复位、时钟与 IO 引脚。

![通用 MCU 片上系统框图：CPU 内核经内部总线连接 Flash/SRAM 与 GPIO/定时器/ADC/通信外设](../assets/schematics/mcu-overview.svg)

## 3. 静态分析（DC）

从硬件供电角度看，MCU 对外的直流连接只有几类：

- **电源脚（VDD/VSS，部分细分 VDDA/VSSA/VREF+）**：典型工作电压 $3.3\text{V}$（老式 51 为 $5\text{V}$）。每个电源对都要就近放去耦电容，见 [最小系统](minimum-system.md)。
- **复位脚（NRST）**：上电时保持低电平让芯片复位，随后被内部上拉拉高。稳态下它是一个高阻输入，不是输出。
- **BOOT 脚**：决定上电后从哪里启动（内置 Flash / 系统存储器 / 外部 SRAM），必须给确定电平。
- **IO 脚**：上电默认多为高阻输入态（浮空），静态电流几乎为零；只有配置成推挽输出或上下拉后才有确定直流电平。

静态功耗的主要来源是**悬空输入脚**——CMOS 输入悬空时电平在阈值附近反复穿越，输入级上下管同时导通，形成可观的 shoot-through（直通电流）。这就是"未用引脚要妥善处理"的硬件根因。

## 4. 动态分析（AC / 瞬态）

MCU 内部一切动作都由**时钟**驱动：内核每来一个时钟沿执行取指/取数，外设按时钟分频后工作。对外可见的动态现象是：

- 引脚在时钟沿附近翻转，产生 $di/dt$ 与 $dv/dt$，叠加在电源上形成**瞬态电流尖峰**（尤其多脚同时翻转、或驱动射频发射时）。
- 工作电流随主频近似线性上升：$I_{dd}\propto f$。同一颗芯片跑 80MHz 比跑 8MHz 明显更耗电、更烫。
- 复位释放后，芯片需要一段**启动时间**（数 ms，含内部电源稳定、晶振起振）才开始从 Flash 取指。

```echarts
{
  "tooltip": {"trigger": "axis"},
  "legend": {"data": ["工作电流 Idd"], "bottom": 0, "textStyle": {"fontSize": 13}},
  "grid": {"left": 60, "right": 24, "top": 30, "bottom": 56},
  "xAxis": {"type": "category", "name": "主频 MHz", "data": [4, 8, 16, 32, 64, 80], "axisLabel": {"fontSize": 11}},
  "yAxis": {"type": "value", "name": "电流 mA", "min": 0, "max": 60, "axisLabel": {"fontSize": 11}},
  "series": [
    {"name": "工作电流 Idd", "type": "line", "smooth": true, "showSymbol": true,
     "lineStyle": {"width": 2.6, "color": "#1a4f8b"}, "itemStyle": {"color": "#1a4f8b"},
     "data": [6, 10, 16, 26, 42, 54]}
  ]
}
```

## 5. 环路分析

::: advanced 进阶：为什么现代 MCU 都用哈佛结构加多层总线
早期 MCU（经典 8051）是冯·诺依曼结构：指令和数据共用一条总线，取指和取数不能并行，每个指令周期要分多个机器周期。现代 ARM Cortex-M 类 MCU 采用**哈佛改进结构**：指令总线与数据总线分离，配合总线矩阵（Bus Matrix）让内核、DMA、外设同时访问不同存储区，从而做到单周期乘加、零等待取指。

对硬件工程师的意义：内核快不等于总线不瓶颈。当 DMA 大批量搬数据、而 CPU 同时取指时，会发生总线竞争；高端型号靠多层总线 + Cache 缓解，低端型号在满带宽时主频"虚高"。选型时看内核 DMIPS/MHz，比看绝对主频更靠谱。
:::

## 6. 元件取值与工程权衡

- **供电电压**：$3.3\text{V}$ 是主流；5V 器件与 3.3V MCU 混用时必须做电平转换，不能直接对接。
- **主频 vs 功耗/EMI**：主频越高性能越好，但瞬态电流越大、辐射越强、对去耦和电源完整性要求越高。电池设备常在空闲时把主频降到几十 kHz。
- **Flash/SRAM 容量**：决定能跑多大程序、开多大缓冲；选大不选小，但要权衡成本。
- **外设资源**：需要几路 ADC、几路 UART、是否带 CAN/USB，直接决定型号与封装——这是硬件选型的第一驱动力。

## 7. 完整设计示例

::: example 从需求到选一颗 MCU
1. **需求**：采集 4 路模拟量（温度/电压），驱动 2 路 PWM 控制风扇，经 UART 上报，电池供电。
2. **盘点外设**：≥4 通道 12bit ADC、2 路 PWM 定时器、1 路 UART、低功耗模式。
3. **选型**：一颗 $3.3\text{V}$、Cortex-M0+/M3、内置 12bit ADC、主频 24~48MHz 的通用 MCU（STM32G0/G4 或同档）即可，不必上带 FPU、USB 的高端型号。
4. **供电**：3.3V LDO，每 VDD 脚 100nF 去耦。
5. **时钟**：内部 RC 振荡器精度够串口通信吗？不够（±1% 以内才稳），串口对波特率敏感时换外部晶振。
6. **验算**：4 路 ADC + 2 路 PWM + 1 UART 的中断负荷很低，24MHz 完全够用。
:::

## 8. 仿真与实验

- 先用厂商**参考手册（Reference Manual）的数据手册**确认封装引脚分配，画一张最小系统草图：VDD/VSS、去耦、晶振（或用内部 RC）、NRST、BOOT、SWD 排针。
- 上电前用万用表量 VDD 对 VSS 的电阻，确认没有短路；再上电量 3.3V 是否稳定。
- 用 SWD 口连接调试器，能识别到芯片 ID 说明最小系统（供电+复位+时钟+调试）已通，再往下调外设。

## 扩展与变种电路

### 扩展1：哈佛与冯·诺依曼总线架构 Harvard vs Von Neumann

定位：理解"为什么取指和取数会打架"，解释现代 MCU 为什么做双总线。

![左：冯·诺依曼单一共享总线；右：哈佛指令总线与数据总线分离](../assets/schematics/mcu-overview-bus-arch.svg)

::: example 工作原理与时序
- **冯·诺依曼**：CPU 用一条总线既取指令又读/写数据存储器，两个操作分时复用，存在"总线瓶颈"，指令周期常需 4~12 个时钟。
- **哈佛**：指令和数据各走独立总线，CPU 可在执行当前指令的同时预取指，多数指令单周期完成。
- 三种典型 MCU 对照：经典 8051 是 8 位 CISC、冯氏改良、机器周期多；STM32（ARM Cortex-M）是 32 位 RISC、哈佛结构 + 总线矩阵；ESP32 是双核 Xtensa/RISC-V + 额外射频子系统，存储器与外设划分更复杂。
:::

取值/选型对比：

| 维度 | 经典 8051 | STM32 (Cortex-M) | ESP32 |
|---|---|---|---|
| 位宽/内核 | 8 位 8051 | 32 位 Cortex-M0~M7 | 32 位双核 Xtensa/RISC-V |
| 架构 | 冯氏改良 | 哈佛+总线矩阵 | 哈佛+多核+RF 子系统 |
| 典型主频 | 11~24MHz | 24~480MHz | 160~240MHz |
| 供电 | 5V（老）/3.3V | 3.3V | 3.3V（RF 峰值≥500mA） |
| 适用 | 极简单控制 | 通用工业/消费 | Wi-Fi/Bluetooth 物联网 |

::: pitfall 把 ESP32 当普通 MCU 供电
- **现象**：上电后 Wi-Fi 一发射就复位、或随机看门狗复位。
- **原因**：射频发射瞬时电流可达数百 mA，普通 3.3V LDO 或去耦不足导致电压瞬间跌穿 BOR 阈值。
- **解决**：电源入口留 ≥10µF 储能电容，供电能力 ≥500mA（ESP32-S3 建议 600mA），见 [最小系统](minimum-system.md)。
:::

## 9. 常见坑与故障现象

::: pitfall 常见坑
- **悬空 IO 额外耗电**：现象是电池设备待机电流远大于手册典型值。原因是 CMOS 输入悬空在阈值区来回穿越。解决：未用脚设为模拟输入或固定电平/弱上下拉。
- **用内部 RC 串口导致波特率漂移**：内部 RC 室温约 ±1%，全温域(−40~85°C)可达 ±4~5%，长距离/高波特率通信误码。解决：对波特率敏感的通信改用外部晶振。
- **BOOT 脚悬空**：上电随机进入系统存储器 Boot 模式，"程序跑不起来"。解决：BOOT0 下拉到确定电平。
- **只看主频选料**：被高主频低 DMIPS/MHz 的型号坑。解决：按内核/MIPS 与实际外设带宽选料。
:::

## 10. 自测题

<details><summary>为什么未使用的 CMOS 输入脚不能悬空，悬空会产生什么额外电流？</summary>
悬空时输入电平在 VIH/VIL 阈值之间摆动，输入级 PMOS/NMOS 同时微导通，形成 shoot-through 直通电流。应设为模拟输入、固定电平或弱上下拉。
</details>

<details><summary>同一颗 MCU，主频从 8MHz 提到 64MHz，工作电流大致怎么变？为什么？</summary>
近似线性上升。CMOS 动态功耗 $P\approx C_L V_{DD}^2 f$，电流随频率近似正比增加；高频翻转更多、瞬态电流也更大。
</details>

## 11. 参考资料

- STMicroelectronics RM0008《STM32F101/103 参考手册》
- Espressif《ESP32 Series Datasheet》与《Hardware Design Guidelines》
- ARM《Cortex-M3/M4 技术参考手册》
