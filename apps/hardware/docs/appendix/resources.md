---
id: resources
title: 推荐 GitHub 仓库、书单与官方文档
part: 10
chapter: 附录
order: 35
tags: [资源, GitHub, 书单, 官方文档, EDA, 仿真]
difficulty: 1
status: published
sources:
  - https://github.com/kitspace/awesome-electronics
  - https://github.com/nhivp/Awesome-Embedded
---

# 附录 G · 推荐 GitHub 仓库、书单与官方文档

精选经本手册调研核实的学习资源，按类别给出真实链接与一句话简介。链接均为官方仓库或权威站点。

## G.1 开源工具与 EDA

| 名称 | 链接 | 简介 |
|---|---|---|
| KiCad | https://www.kicad.org/ | 开源 EDA 套件，原理图+PCB 设计，社区生态最完善 |
| KiCad 源码镜像 | https://github.com/KiCad/kicad-source-mirror | KiCad GitHub 只读镜像（主开发在 GitLab） |
| LibrePCB | https://librepcb.org/ | 另一款开源 EDA，库管理简洁，适合入门 |
| EasyEDA / 嘉立创EDA | https://easyeda.com/ | 在线 EDA，与国内 PCB 打样无缝衔接 |
| ltspice 官方下载 | https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html | ADI 免费 SPICE 仿真器，行业标准 |
| Saturn PCB Toolkit | https://saturnpcb.com/saturn-pcb-toolkit/ | 免费 PCB 计算器集：线宽/阻抗/过孔/散热 |
| Falstad Circuit JS | https://www.falstad.com/circuit/ | 浏览器内 SPICE 仿真，电子流动可视化 |
| CircuitLab | https://www.circuitlab.com/ | 在线原理图仿真，可交互 |
| KiCad 符号库 | https://github.com/KiCad/kicad-symbols | 官方符号库历史仓库（新版随 KiCad 分发） |

## G.2 学习仓库与清单

| 名称 | 链接 | 简介 |
|---|---|---|
| awesome-electronics | https://github.com/kitspace/awesome-electronics | 电子工程师资源总清单（EDA/教程/仿真/社区），发现一切的入口 |
| Awesome-Embedded | https://github.com/nhivp/Awesome-Embedded | 嵌入式与 MCU 生态精选：工具链/RTOS/bootloader |
| open-electronics | https://github.com/ajaymnk/open-electronics | 面向爱好者的电子资源链接集，含书单 |
| logisim-evolution | https://github.com/logisim-evolution/logisim-evolution | 开源数字逻辑仿真，拖拽搭门电路看波形 |
| pulseview (sigrok) | https://github.com/sigrokproject/pulseview | 开源信号分析 GUI，配合廉价 USB 逻辑分析仪 |
| awesome-hdl | https://github.com/hdl/awesome | HDL 设计与验证工具索引（Verilator/Yosys/cocotb） |

## G.3 经典书籍

| 书名 | 作者 | 简介 |
|---|---|---|
| The Art of Electronics (3rd ed.) | Horowitz & Hill | 硬件百科全书，器件与模拟设计案头权威 |
| Practical Electronics for Inventors (4th ed.) | Scherz & Monk | 入门到实战图解，器件与电路直观 |
| Op Amps for Everyone (TI, SLOD006B) | Ron Mancini | TI 官方免费运放设计全书（PDF） |
| Design with Operational Amplifiers | Sergio Franco | 运放反馈与稳定性经典教材 |
| Microelectronic Circuits (8th ed.) | Sedra, Smith et al. | 全球广泛采用的模电教材 |
| Switching Power Supplies A–Z (2nd ed.) | Sanjaya Maniktala | 开关电源极其实操指南 |
| Switching Power Supply Design (3rd ed.) | Pressman, Billings, Morey | 开关电源设计权威参考 |
| Fundamentals of Power Electronics (2nd ed.) | Erickson & Maksimovic | 电力电子理论教材，环路建模根基 |
| Electromagnetic Compatibility Engineering | Henry W. Ott | EMC 工程最实用权威著作 |
| High Speed Digital Design | Howard Johnson & Graham | 高速数字设计"黑魔法"经典 |
| Digital Design (6th ed.) | Mano & Ciletti | 数电经典教材，含 Verilog 入门 |
| The Definitive Guide to ARM Cortex-M3/M4 (3rd ed.) | Joseph Yiu | Cortex-M 内核权威指南 |
| Troubleshooting Analog Circuits | Robert A. Pease | 模拟排障经验集，经典老资料 |
| The Circuit Designer's Companion (3rd ed.) | Peter Wilson (Tim Williams) | 工程师实践手册：去耦/供电/PCB |

## G.4 官方文档与应用笔记

| 名称 | 链接 | 简介 |
|---|---|---|
| TI Precision Labs – Op Amps | https://www.ti.com/education/training/ | TI 免费视频+文档课程，运放/电源/ADC 系统教学 |
| TI Op Amps for Everyone (SLOD006B) | https://www.ti.com/lit/an/slod006b/slod006b.pdf | 运放设计免费全书 PDF |
| TI Buck 功率级计算 (SLVA477A) | https://www.ti.com/lit/an/slva477a/slva477a.pdf | Buck 全套工程公式 |
| TI RS-485 Design Guide (SLLA272D) | https://www.ti.com/lit/an/slla272d/slla272d.pdf | RS-485 总线设计权威指南 |
| TI CAN 入门 (SLOA101B) | https://www.ti.com/lit/an/sloa101b/sloa101b.pdf | CAN 总线入门应用笔记 |
| ADI 模拟对话与 MT 系列教程 | https://www.analog.com/en/resources/analog-dialogue.html | ADI 免费技术文章库，运放/数据转换器 |
| ADI 仪放设计指南 | https://www.analog.com/en/products/precision-instrumentation-amplifier.html | 三运放仪放结构与传感器接口 |
| STM32 硬件设计 Wiki | https://wiki.stmicroelectronics.cn/stm32mcu/wiki/ | ST 官方 MCU 电源/去耦/原理图自查 |
| ESP32 硬件设计指南 | https://docs.espressif.com/projects/esp-hardware-design-guidelines/ | 乐鑫官方原理图/PCB 检查清单 |
| Tektronix 探头入门白皮书 | https://www.tek.com/ | 示波器探头带宽/接地/补偿入门 |
| Keysight 函数发生器指南 | https://www.keysight.com/ | 信号发生器使用与带载测试 |
| IPC 标准目录 | https://www.ipc.org/ | PCB 封装/制造标准（IPC-7351 等） |
| IEC 安规认证 | https://www.iec.ch/ | IEC 62368/FCC/CE 标准体系入口 |

## G.5 在线课程与教程

| 名称 | 链接 | 简介 |
|---|---|---|
| Lessons In Electric Circuits | https://www.ibiblio.org/kuphaldt/electricCircuits/ | 6 卷开源电路教材，苏格拉底式习题 |
| Nand2Tetris | https://www.nand2tetris.org/ | 从与非门搭出 CPU 的公开课 |
| MIT Op-Amps: Theory and Practice | https://web.mit.edu/klund/www/books/op2e.html | MIT 免费在线运放教材 |
| Khan Academy EE | https://www.khanacademy.org/science/electrical-engineering | 互动式电路入门 |
| SparkFun Learn | https://learn.sparkfun.com/ | 大量图文教程：焊接/串口/I2C/FPGA |
| CircuitLab Textbook | https://www.circuitlab.com/textbook/ | 免费在线书，原理图可交互仿真 |
| NEETS 海军电子教材 | https://www.electriciantraining.tpub.com/ | 公版工程图多的培训教材 |
| 江协科技 STM32 教程 | https://jiangxiekeji.com/ | 中文免费 STM32 入门视频课 |

## G.6 仿真与计算工具

| 名称 | 链接 | 简介 |
|---|---|---|
| LTspice | https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html | ADI 免费 SPICE，本手册仿真首选 |
| LTpowerCAD | https://www.analog.com/en/design-center/design-tools-and-calculators.html | ADI 电源设计工具，可导出 LTspice |
| TI WEBENCH | https://www.ti.com/design-resources/technologies/analog-power-management/webench.html | 在线电源选型与热仿真 |
| Falstad | https://www.falstad.com/circuit/ | 浏览器实时仿真，教学直观 |
| sigrok 平台 | https://sigrok.org/ | 开源信号分析生态（逻辑分析仪/示波器） |

> 以上链接均经调研核实；仓库 star 数随时间变化，未在此标注以免过时。选型前请再次确认仓库活跃度与许可证。
