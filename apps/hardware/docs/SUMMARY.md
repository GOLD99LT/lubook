# Hardware Handbook · 硬件工程师手册

> 本文件是全书的装配清单：页面顺序、编号、导航均由它决定。
> 新增章节 = 写 Markdown + 在此加一行；下线 = 删一行或在 frontmatter 标记 status: draft。

## 第一篇 · 电路基础

* [1.1 电压、电流、电阻与功率](basics/voltage-current-power.md)
* [1.2 欧姆定律与焦耳定律](basics/ohms-law.md)
* [1.3 串联、并联与分压分流](basics/series-parallel.md)
* [1.4 基尔霍夫定律 KCL / KVL](basics/kcl-kvl.md)
* [1.5 节点法与网孔法（进阶）](basics/nodal-mesh-analysis.md)
* [1.6 电容原理与 RC 时间常数](basics/capacitor-rc.md)
* [1.7 电感原理与 RL 暂态](basics/inductor-rl.md)
* [1.8 直流与交流、频率、相位与有效值](basics/dc-ac.md)
* [1.9 阻抗与导纳](basics/impedance.md)
* [1.10 RLC 电路与谐振](basics/rlc-resonance.md)
* [1.11 变压器原理](basics/transformer.md)
* [1.12 市电与三相电基础](basics/mains-three-phase.md)
* [1.13 安全用电与触电防护](basics/electrical-safety.md)
* [1.14 数学基础：复数、dB 与拉氏变换直觉](basics/math-basics.md)

## 第二篇 · 元器件详解

* [2.1 电阻器全解：材质、精度、功率、温漂](components/resistors.md)
* [2.2 贴片封装与 E 系列标准值](components/smd-packages-e-series.md)
* [2.3 特殊电阻：热敏、压敏、光敏、电位器](components/special-resistors.md)
* [2.4 电容器全解：MLCC、电解、钽、薄膜](components/capacitors.md)
* [2.5 电容参数：耐压、ESR、ESL 与失效模式](components/capacitor-parameters.md)
* [2.6 电感器与磁珠](components/inductors-ferrite-beads.md)
* [2.7 二极管：整流、快恢复、肖特基](components/diodes.md)
* [2.8 稳压管、LED 与 TVS/ESD 保护管](components/zener-led-tvs.md)
* [2.9 BJT 三极管：开关与放大](components/bjt.md)
* [2.10 MOSFET：参数、导通、驱动与损耗](components/mosfet.md)
* [2.11 IGBT、可控硅、继电器与光耦](components/igbt-scr-relay-optocoupler.md)
* [2.12 晶振与谐振器](components/crystal-oscillator.md)
* [2.13 开关、接插件、连接器与保险丝](components/switches-connectors-fuses.md)

## 第三篇 · 模拟电路与运放

* [3.1 模拟信号与信号链概述](opamp/analog-signal-chain.md)
* [3.2 二极管电路：整流、滤波、限幅、钳位](opamp/diode-circuits.md)
* [3.3 线性稳压与基准源](opamp/linear-regulator-reference.md)
* [3.4 BJT 三种放大组态与静态工作点](opamp/bjt-amplifiers.md)
* [3.5 小信号模型与增益、输入输出阻抗](opamp/small-signal-model.md)
* [3.6 功率放大：甲类、乙类、甲乙类与推挽](opamp/power-amplifiers.md)
* [3.7 运放概述：符号、封装与引脚](opamp/opamp-overview.md)
* [3.8 理想模型五假设与虚短、虚断](opamp/ideal-opamp.md)
* [3.9 开环、闭环增益与负反馈本质](opamp/open-loop-feedback.md)
* [3.10 反馈四拓扑与环路增益](opamp/feedback-topologies.md)
* [3.11 稳定性：伯德图、相位裕度与补偿](opamp/stability-bode.md)
* [3.12 供电轨、输出摆幅与 Rail-to-Rail](opamp/supply-rails.md)
* [3.13 共模范围、CMRR 与 PSRR](opamp/cmrr-psrr.md)
* [3.14 失调电压、偏置电流与漂移](opamp/offset-bias.md)
* [3.15 带宽 GBP、压摆率与建立时间](opamp/gbp-slew-rate.md)
* [3.16 噪声：电压噪声、电流噪声与计算](opamp/noise.md)
* [3.17 电压跟随器 Buffer](opamp/voltage-follower.md)
* [3.18 反相比例放大器](opamp/inverting-amplifier.md)
* [3.19 同相比例放大器](opamp/non-inverting-amplifier.md)
* [3.20 差分放大器与电阻匹配](opamp/differential-amplifier.md)
* [3.21 仪表放大器（三运放）](opamp/instrumentation-amplifier.md)
* [3.22 加法、减法运算电路](opamp/summing-amplifier.md)
* [3.23 积分器与微分器](opamp/integrator-differentiator.md)
* [3.24 有源滤波：一阶低通与高通](opamp/first-order-filters.md)
* [3.25 二阶滤波器 Sallen-Key 与 Q 值](opamp/sallen-key-filters.md)
* [3.26 带通与带阻滤波器入门](opamp/bandpass-bandstop.md)
* [3.27 比较器与迟滞比较器](opamp/comparator-hysteresis.md)
* [3.28 振荡器：文氏桥与晶体振荡](opamp/oscillators.md)
* [3.29 555 定时器典型应用](opamp/555-timer.md)
* [3.30 精密整流、峰值检测与采样保持](opamp/precision-rectifier-peak-samplehold.md)
* [3.31 V/I、I/V 转换与传感器接口](opamp/vi-iv-converter.md)
* [3.32 模拟开关与多路复用](opamp/analog-switch-mux.md)
* [3.33 单电源电路与电平偏置搬移](opamp/single-supply-biasing.md)

## 第四篇 · 数字电路与逻辑

* [4.1 数制、编码、补码与格雷码](digital/number-systems.md)
* [4.2 逻辑门、布尔代数与卡诺图](digital/logic-gates-boole.md)
* [4.3 组合逻辑：译码、编码、选择与加法](digital/combinational-logic.md)
* [4.4 触发器 RS / D / JK](digital/flip-flops.md)
* [4.5 寄存器、计数器与分频](digital/registers-counters.md)
* [4.6 时序分析：建立/保持时间与亚稳态](digital/timing-analysis-metastability.md)
* [4.7 三态门、总线与上拉下拉](digital/tri-state-bus-pull.md)
* [4.8 逻辑电平标准：TTL / CMOS / LVDS](digital/logic-levels.md)
* [4.9 存储器：SRAM / DRAM / Flash / EEPROM](digital/memory.md)
* [4.10 电平转换与总线缓冲](digital/level-shifter.md)
* [4.11 FPGA/CPLD 与 Verilog 入门](digital/fpga-verilog.md)
* [4.12 数字系统时钟与复位设计](digital/clock-reset-design.md)

## 第五篇 · 单片机与嵌入式硬件

* [5.1 MCU 概览：51 / STM32 / ESP32 架构](mcu/mcu-overview.md)
* [5.2 最小系统：电源、时钟、复位、调试](mcu/minimum-system.md)
* [5.3 GPIO 原理与驱动能力](mcu/gpio.md)
* [5.4 中断机制（硬件视角）](mcu/interrupts.md)
* [5.5 ADC 原理、参数与参考电压](mcu/adc.md)
* [5.6 DAC 与模拟输出](mcu/dac.md)
* [5.7 定时器与 PWM 原理](mcu/timer-pwm.md)
* [5.8 UART 与 RS-232 物理层](mcu/uart-rs232.md)
* [5.9 RS-485 与 CAN 总线硬件](mcu/rs485-can.md)
* [5.10 I²C 与 SPI 总线时序](mcu/i2c-spi.md)
* [5.11 USB 与以太网物理层概览](mcu/usb-ethernet.md)
* [5.12 看门狗、RTC 与低功耗硬件](mcu/watchdog-rtc-lowpower.md)
* [5.13 常用外设接口设计](mcu/peripheral-design.md)

## 第六篇 · 电源设计

* [6.1 电源指标：纹波、效率、调整率与时序](power/power-specs.md)
* [6.2 线性电源：变压、整流、滤波](power/linear-supply.md)
* [6.3 LDO 原理、选型与功耗计算](power/ldo.md)
* [6.4 开关电源原理与 Buck 降压](power/buck.md)
* [6.5 Boost 升压与 Buck-Boost](power/boost-buckboost.md)
* [6.6 功率电感、电容、MOS 与二极管选型](power/power-component-selection.md)
* [6.7 控制模式与环路补偿](power/smps-control-loop.md)
* [6.8 反激 Flyback 等隔离电源简介](power/flyback.md)
* [6.9 电池、充电管理与电量计](power/battery-charger.md)
* [6.10 电源监控、POR 与负载开关](power/power-monitoring-loadswitch.md)
* [6.11 地的学问与地弹](power/grounding.md)
* [6.12 电源完整性与去耦体系](power/power-integrity-decoupling.md)

## 第七篇 · PCB 设计与 EMC

* [7.1 PCB 结构、层叠与板材](pcb/pcb-stackup.md)
* [7.2 EDA 工具：KiCad / Altium 工作流](pcb/eda-tools.md)
* [7.3 原理图设计、封装与库管理](pcb/schematic-library.md)
* [7.4 布局原则与模块化](pcb/placement.md)
* [7.5 布线：线宽、载流、过孔、间距](pcb/routing.md)
* [7.6 模拟、数字、电源分区布线](pcb/analog-digital-power-routing.md)
* [7.7 信号完整性：反射、阻抗匹配与端接](pcb/signal-integrity.md)
* [7.8 串扰与差分走线](pcb/crosstalk-differential.md)
* [7.9 EMI/EMC：辐射与传导机理](pcb/emi-emc.md)
* [7.10 屏蔽、滤波与接地设计](pcb/shielding-filtering-grounding.md)
* [7.11 ESD 防护与接口保护](pcb/esd-protection.md)
* [7.12 热设计：散热、铜箔与散热器](pcb/thermal-design.md)
* [7.13 DFM 与焊接工艺](pcb/dfm-process.md)

## 第八篇 · 测量、调试与工程实践

* [8.1 万用表使用与测量技巧](practice/multimeter.md)
* [8.2 示波器：探头、触发、带宽与接地](practice/oscilloscope.md)
* [8.3 信号发生器、电子负载与稳压电源](practice/signal-generator-load.md)
* [8.4 逻辑分析仪、频谱仪与网络分析仪](practice/logic-analyzer-spectrum.md)
* [8.5 焊接：直插、贴片、拆焊与飞线](practice/soldering.md)
* [8.6 硬件调试方法论与上电检查](practice/debug-methodology.md)
* [8.7 故障排查案例库](practice/troubleshooting-cases.md)
* [8.8 可靠性：降额、老化与环境试验](practice/reliability-derating.md)
* [8.9 安规认证：3C / CE / FCC / UL](practice/safety-certification.md)
* [8.10 硬件开发流程：需求到量产](practice/development-flow.md)
* [8.11 BOM、版本、文档与成本控制](practice/bom-version-cost.md)
* [8.12 LTspice 仿真入门](practice/ltspice.md)

## 第九篇 · 硬件测试与面试题库

* [9.1 电路基础测试题](quizbank/quiz-basics.md)
* [9.2 元器件测试题](quizbank/quiz-components.md)
* [9.3 模拟电路与运放测试题](quizbank/quiz-opamp.md)
* [9.4 数字电路测试题](quizbank/quiz-digital.md)
* [9.5 单片机与嵌入式硬件测试题](quizbank/quiz-mcu.md)
* [9.6 电源设计测试题](quizbank/quiz-power.md)
* [9.7 PCB 与 EMC 测试题](quizbank/quiz-pcb.md)
* [9.8 测量调试与工程实践测试题](quizbank/quiz-practice.md)
* [9.9 综合系统设计与情景题](quizbank/quiz-system.md)

## 附录

* [A. 术语中英对照表](appendix/glossary.md)
* [B. E96 电阻与 E 系列电容取值表](appendix/e96-table.md)
* [C. SMD 封装尺寸图](appendix/smd-footprints.md)
* [D. 常用芯片选型速查](appendix/chip-selection.md)
* [E. 单位换算与常用常数](appendix/unit-conversion.md)
* [F. 常用电路速查图集](appendix/circuit-quick-reference.md)
* [G. 推荐 GitHub 仓库、书单与官方文档](appendix/resources.md)
* [H. 面包板实验清单](appendix/breadboard-experiments.md)
* [I. 开源优秀硬件作品赏析](appendix/open-source-projects.md)
