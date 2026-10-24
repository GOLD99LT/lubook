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

## 第三篇 · 通信接口与协议


## 第四篇 · RTOS 与并发


## 第五篇 · 存储、启动与升级

* [Bootloader 与 OTA：A/B 双区、镜像校验与回滚 Bootloader and OTA](storage/bootloader-ota.md)

## 第六篇 · 工程实践与量产
