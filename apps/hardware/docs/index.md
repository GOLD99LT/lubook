---
layout: home

hero:
  name: 硬件工程师手册
  text: Hardware Handbook
  tagline: 一本开源、可交互的硬件工程师学习手册 —— 从电路基础到电源、PCB 与 EMC，含原理图、公式推导、设计示例与面试题库。
  actions:
    - theme: brand
      text: 开始学习
      link: /basics/voltage-current-power
    - theme: alt
      text: 工程速查
      link: /appendix/glossary
    - theme: alt
      text: 面试刷题
      link: /quizbank/quiz-basics

features:
  - title: '<svg class="hh-feat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="5" cy="19" r="1.6"/><circle cx="19" cy="5" r="1.6"/><path d="M6.5 17.5C9 13 11 11 17.5 6.5"/></svg> 零基础路径'
    details: 第一篇电路基础 → 第二篇元器件 → 第三篇运放，按入门难度的章节循序渐进，打好底子。
    link: /basics/voltage-current-power
  - title: '<svg class="hh-feat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L4.5 13.5H11L9.5 22 19 10h-6.5L13 2z"/></svg> 电源 / PCB 专题'
    details: Buck 环路、LDO、叠层、信号完整性、EMC —— 工作中直接能用的设计要点与选型依据。
    link: /power/buck
  - title: '<svg class="hh-feat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="7" width="10" height="10" rx="1.5"/><path d="M10 7V4M14 7V4M10 20v-3M14 20v-3M7 10H4M7 14H4M20 10h-3M20 14h-3"/></svg> 数电 / MCU 专题'
    details: 时序与亚稳态、电平标准、最小系统、总线时序、ADC/DAC，把数字与嵌入式硬件讲透。
    link: /digital/timing-analysis-metastability
  - title: '<svg class="hh-feat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 6.5a4 4 0 0 1-5.3 5.3L4 17l3 3 5.2-5.2a4 4 0 0 0 5.3-5.3l-2.6 2.6-2.2-2.2 2.8-3.4z"/></svg> 工程实战'
    details: 示波器探头与触发、焊接、上电检查、故障排查案例库、可靠性与安规认证。
    link: /practice/debug-methodology
  - title: '<svg class="hh-feat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20l1.2-4.2L16.7 4.3a2 2 0 0 1 3 3L8.2 18.8 4 20z"/><path d="M13.5 6.5l3 3"/></svg> 面试题库'
    details: 九组按篇组织的测试题，答案折叠、点击即看，自测会与不会。
    link: /quizbank/quiz-system
  - title: '<svg class="hh-feat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/><path d="M8 10.5h5M10.5 8v5"/></svg> 工程速查附录'
    details: 术语中英对照、E96 取值表、SMD 封装、芯片选型、常用电路速查图集。
    link: /appendix/circuit-quick-reference
---

## 我的学习

<ClientOnly>
  <LearningPanel />
</ClientOnly>

## 全书导航

::: tip 怎么用这本手册
顶部搜索框可以按知识点、公式、元器件名全文检索；左侧目录按「篇 → 分组 → 章」组织；每章末尾有上一章 / 下一章与自测折叠题。标注「深入」的折叠块是进阶推导，初学者可先跳过。
:::

- **[第一篇 · 电路基础](/basics/voltage-current-power.md)** — 电压电流、欧姆定律、KCL/KVL、电容电感、谐振、三相电
- **[第二篇 · 元器件详解](/components/resistors.md)** — 电阻/电容/电感、二极管、BJT/MOSFET/IGBT、晶振与连接器
- **[第三篇 · 模拟电路与运放](/opamp/analog-signal-chain.md)** — 反馈与稳定性、各类运放电路、滤波、比较器、振荡器
- **[第四篇 · 数字电路与逻辑](/digital/number-systems.md)** — 逻辑代数、触发器、时序分析、存储器、电平标准、FPGA 入门
- **[第五篇 · 单片机与嵌入式硬件](/mcu/mcu-overview.md)** — 最小系统、GPIO、中断、ADC/DAC、UART/485/CAN、I²C/SPI
- **[第六篇 · 电源设计](/power/power-specs.md)** — LDO、Buck/Boost、环路补偿、反激、电池充电、地与电源完整性
- **[第七篇 · PCB 设计与 EMC](/pcb/pcb-stackup.md)** — 叠层、布局布线、信号完整性、串扰、EMI/EMC、热设计、DFM
- **[第八篇 · 测量、调试与工程实践](/practice/multimeter.md)** — 万用表/示波器、焊接、调试方法、可靠性、安规、LTspice
- **[第九篇 · 硬件测试与面试题库](/quizbank/quiz-basics.md)** — 九组分篇测试题，覆盖全册核心考点
- **[附录](/appendix/glossary.md)** — 术语表、E96 取值、封装尺寸、芯片选型、速查图集、开源作品赏析

## 许可

本站代码以 [MIT 协议](https://opensource.org/licenses/MIT) 开源；文档内容以 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 共享。源码与协作见 [GitHub 仓库](https://github.com/GOLD99LT/hardware-handbook)。
