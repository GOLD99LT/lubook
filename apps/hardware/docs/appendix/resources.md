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
  - Horowitz and Hill, The Art of Electronics, 3rd ed. — bibliography and further reading
  - IPC-7351B Surface Mount Design and Land Pattern Standard
  - KiCad documentation, Getting Started guide
---

# 附录 G · 推荐 GitHub 仓库、书单与官方文档

精选经本手册调研核实的学习资源，按类别给出真实链接与一句话简介。链接在修订时逐条用 HTTP 请求核验（200/重定向）；对脚本返回 403/406 的站点（反爬）保留 URL 但不作为唯一依据；无法核实具体文档编号的条目**只写编号/名称、不给 URL**，避免拼造链接。

## G.1 开源工具与 EDA

| 名称 | 链接 | 简介 |
|---|---|---|
| KiCad | https://www.kicad.org/ | 开源 EDA 套件，原理图+PCB 设计，社区生态最完善 |
| KiCad 源码镜像 | https://github.com/KiCad/kicad-source-mirror | KiCad GitHub 只读镜像（主开发在 GitLab） |
| LibrePCB | https://librepcb.org/ | 另一款开源 EDA，库管理简洁，适合入门 |
| EasyEDA / 嘉立创EDA | https://easyeda.com/ | 在线 EDA，与国内 PCB 打样衔接（站点对脚本返回 403，浏览器可访问） |
| LTspice 官方下载 | https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html | ADI 免费 SPICE 仿真器，行业标准 |
| Saturn PCB Toolkit | https://saturnpcb.com/saturn-pcb-toolkit/ | 免费 PCB 计算器集：线宽/阻抗/过孔/散热（脚本 406，浏览器可访问） |
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
| PulseView (sigrok) | https://github.com/sigrokproject/pulseview | 开源信号分析 GUI，配合廉价 USB 逻辑分析仪 |
| awesome-hdl | https://github.com/hdl/awesome | HDL 设计与验证工具索引（Verilator/Yosys/cocotb） |

## G.3 经典书籍

| 书名 | 作者 | 简介 |
|---|---|---|
| The Art of Electronics (3rd ed.) | Horowitz & Hill | 硬件百科全书，器件与模拟设计案头权威 |
| Practical Electronics for Inventors (4th ed.) | Scherz & Monk | 入门到实战图解，器件与电路直观 |
| Op Amps for Everyone (3rd ed., Newnes 2009) | Ron Mancini & Bruce Carter | 运放设计经典，TI 早期 SLOD006B 指南的成书版 |
| Design with Operational Amplifiers and Analog Integrated Circuits (4th ed.) | Sergio Franco | 运放反馈与稳定性经典教材 |
| Microelectronic Circuits (8th ed.) | Sedra, Smith, Carusone, Gaudet | 全球广泛采用的模电教材 |
| Switching Power Supplies A–Z (2nd ed.) | Sanjaya Maniktala | 开关电源极其实操指南 |
| Switching Power Supply Design (3rd ed.) | Pressman, Billings, Morey | 开关电源设计权威参考 |
| Fundamentals of Power Electronics (2nd ed.) | Erickson & Maksimovic | 电力电子理论教材，环路建模根基 |
| Electromagnetic Compatibility Engineering | Henry W. Ott | EMC 工程最实用权威著作 |
| High Speed Digital Design | Howard Johnson & Graham | 高速数字设计“黑魔法”经典 |
| Digital Design (6th ed.) | Mano & Ciletti | 数电经典教材，含 Verilog 入门 |
| The Definitive Guide to ARM Cortex-M3/M4 (3rd ed.) | Joseph Yiu | Cortex-M 内核权威指南 |
| Troubleshooting Analog Circuits | Robert A. Pease | 模拟排障经验集，经典老资料 |
| The Circuit Designer's Companion (3rd ed.) | Peter Wilson（前两版 Tim Williams） | 工程师实践手册：去耦/供电/PCB |

## G.4 官方文档与应用笔记

| 名称 | 链接 | 简介 |
|---|---|---|
| TI Precision Labs – Op Amps | https://www.ti.com/video/series/precision-labs/ti-precision-labs-op-amps.html | TI 免费视频+文档课程，运放/电源/ADC 系统教学 |
| TI 运放设计参考 SLOD006B | 文献编号 SLOD006B（TI 公开链接已 404，按编号检索存档） | 经典《Op Amps for Everyone》Design Guide |
| TI Buck 功率级计算 (SLVA477A/B) | https://www.ti.com/lit/an/slva477a/slva477a.pdf | Buck 全套工程公式（在线为 A 版，B 版为同一文献修订） |
| TI RS-485 Design Guide (SLLA272D) | https://www.ti.com/lit/an/slla272d/slla272d.pdf | RS-485 总线设计权威指南 |
| TI CAN 入门 (SLOA101B) | https://www.ti.com/lit/an/sloa101b/sloa101b.pdf | CAN 总线入门应用笔记 |
| ADI 模拟对话（Analog Dialogue） | https://www.analog.com/en/resources/analog-dialogue.html | ADI 免费技术文章库，运放/数据转换器 |
| ADI 仪表放大器产品与设计资源 | https://www.analog.com/en/product-category/instrumentation-amplifiers.html | 三运放仪放结构与传感器接口 |
| STM32 硬件设计 Wiki | https://wiki.stmicroelectronics.cn/stm32mcu/wiki/ | ST 官方 MCU 电源/去耦/原理图自查 |
| ESP32 硬件设计指南 | https://docs.espressif.com/projects/esp-hardware-design-guidelines/ | 乐鑫官方原理图/PCB 检查清单 |
| Tektronix 探头入门白皮书 | https://www.tek.com/en/documents/whitepaper/abcs-probes-primer | 示波器探头带宽/接地/补偿入门 |
| Keysight 函数发生器指南 | 厂商文档，具体编号未核实，不提供 URL | 信号发生器使用与带载测试 |
| IPC 标准与技术资源 | https://www.electronics.org/knowledge-hub | IPC 标准与知识库（ipc.org 已跳转到 electronics.org） |
| IEC 标准在线商店 | https://webstore.iec.ch/ | IEC 62368-1 等安规标准的官方入口 |

## G.5 在线课程与教程

| 名称 | 链接 | 简介 |
|---|---|---|
| Lessons In Electric Circuits | https://www.ibiblio.org/kuphaldt/electricCircuits/ | 6 卷开源电路教材，苏格拉底式习题 |
| Nand2Tetris | https://www.nand2tetris.org/ | 从与非门搭出 CPU 的公开课 |
| MIT Op-Amps: Theory and Practice | https://web.mit.edu/klund/www/books/op2e.html | MIT 免费在线运放教材 |
| Khan Academy EE | https://www.khanacademy.org/science/electrical-engineering | 互动式电路入门 |
| SparkFun Learn | https://learn.sparkfun.com/ | 大量图文教程：焊接/串口/I2C/FPGA |
| CircuitLab Textbook | https://www.circuitlab.com/textbook/ | 免费在线书，原理图可交互仿真 |
| NEETS 海军电子教材 | 公版教材，原 tpub 镜像当前无法访问，按 NEETS 模块编号检索 | 公版工程图多的培训教材 |
| 江协科技 STM32 教程 | https://jiangxiekeji.com/ | 中文免费 STM32 入门视频课 |

## G.6 仿真与计算工具

| 名称 | 链接 | 简介 |
|---|---|---|
| LTspice | https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html | ADI 免费 SPICE，本手册仿真首选 |
| ADI 电源设计工具（LTpowerCAD 等） | https://www.analog.com/en/design-center/design-tools-and-calculators.html | ADI 电源设计工具入口，可导出 LTspice |
| TI WEBENCH | https://www.ti.com/tool/WEBENCH-CIRCUIT-DESIGNER | 在线电源选型与热仿真 |
| Falstad | https://www.falstad.com/circuit/ | 浏览器实时仿真，教学直观 |
| sigrok 平台 | https://sigrok.org/ | 开源信号分析生态（逻辑分析仪/示波器） |
| Saturn PCB Toolkit | https://saturnpcb.com/saturn-pcb-toolkit/ | 线宽/阻抗/过孔/散热计算器 |

> 链接会失效、仓库会改名。判断一个资源是否还值得跟，先看最近一次提交/更新、issue 活跃度与 License，而不是 star 数；本表不标注 star，避免过时。

## G.7 使用建议

::: motivation 资源不在多，在能用
- **一个 EDA 用熟**：KiCad 足够覆盖从原理图到 Gerber 的全流程，换来换去最浪费时间。
- **一本书读透**：模拟主线按《The Art of Electronics》→《Microelectronic Circuits》→ 具体 datasheet/应用笔记，比收藏十个书单有效。
- **官方文档优先**：器件行为以 datasheet 和应用笔记为准，博客/视频只用来建立直觉。
- **链接核验**：下载 PDF 后本地归档并记录版本号/日期；厂商改版后旧链接经常 404。
:::

> 以上链接均经修订时核验；仓库 star 数随时间变化，未在此标注以免过时。选型前请再次确认仓库活跃度与许可证。
