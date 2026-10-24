# 嵌入式软件手册（MCU）

> 本文件是装配清单：页面顺序、编号、导航由它决定。新增章节 = 写 Markdown + 在此加一行。

## 第一篇 · 嵌入式基础

* [嵌入式软件全景：从寄存器到 RTOS](basics/embedded-overview.md)
* [工具链与调试：从源码到芯片的最后一公里 Toolchain and Debug](basics/toolchain-debug.md)
* [存储器与外设寄存器：Flash、SRAM 与寄存器语义 Memory and Peripheral Registers](basics/memory-registers.md)
* [启动流程：从复位向量到 main Startup and Boot](basics/startup-boot.md)

## 第二篇 · Cortex-M 与 MCU 外设

* [Cortex-M 内核：寄存器、特权级与异常模型 | Cortex-M Core Architecture](mcu/cortex-m-arch.md)
* [时钟树与低层初始化：从 HSE 到 SysTick | Clock Tree and Low-Level Initialization](mcu/clock-tree.md)
* [GPIO 电气与驱动：从推挽输出到按键消抖 | GPIO Electrical Behavior and Driver Design](mcu/gpio.md)
* [中断与 NVIC：向量表、优先级与响应延迟](mcu/interrupt-nvic.md)
* [定时器与 PWM：预分频、频率与死区](mcu/timer-pwm.md)
* [DMA：通道映射、双缓冲与带宽](mcu/dma.md)
* [ADC/DAC：采样保持、量化误差与重建滤波](mcu/adc-dac.md)
* [看门狗、RTC 与低功耗定时：独立看门狗、窗口看门狗与 ppm 校准 | Watchdog, RTC and Low-Power Timers](mcu/watchdog-rtc.md)

## 第三篇 · 通信接口与协议

* [UART 与 USART：帧格式、波特率误差与收发缓冲 | UART and USART: Framing, Baud Error, and Receive Buffering](comm/uart.md)
* [I²C 总线：起止条件、时钟同步与总线恢复 | I²C Bus: START/STOP, Clock Synchronization, and Bus Recovery](comm/i2c.md)
* [SPI 总线：四种模式、片选与环形 DMA | SPI Bus: Clock Modes, Chip Select, and Ring DMA](comm/spi.md)

## 第四篇 · RTOS 与并发

* [RTOS 调度：任务状态机、优先级抢占与可调度性 RTOS Scheduling](rtos/rtos-scheduling.md)
* [同步原语：临界区、互斥量、事件组与死锁预防 Synchronization Primitives](rtos/sync-primitives.md)
* [优先级反转与实时性：继承、天花板与微秒级抖动 Priority Inversion and Jitter](rtos/priority-inversion.md)

## 第五篇 · 存储、启动与升级

* [Flash 与 EEPROM：擦写粒度、寿命与掉电安全写入 | Flash and EEPROM: Granularity, Endurance and Fail-Safe Writes](storage/flash-eeprom.md)
* [Bootloader 与 OTA：A/B 双区、镜像校验与回滚 Bootloader and OTA](storage/bootloader-ota.md)

## 第六篇 · 工程实践与量产

* [低功耗设计：功耗构成、睡眠模式与电池寿命 | Low-Power Design: Power Budget, Sleep Modes and Battery Life](practice/low-power.md)
* [可靠性与看门狗体系：故障模型、双看门狗与复位取证 | Reliability and Watchdog Systems](practice/reliability.md)
* [测试与静态分析：单元测试、MISRA C、覆盖率与 HIL | Testing and Static Analysis](practice/testing-static.md)
* [软件能做的 EMC：抖频、边沿控制、采样同步与安全状态 | EMC Measures in Software](practice/emc-software.md)
