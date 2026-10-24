# 嵌入式 Linux 手册

> 本文件是装配清单：页面顺序、编号、导航由它决定。新增章节 = 写 Markdown + 在此加一行。

## 第一篇 · 系统与构建

* [嵌入式 Linux 全景：从 SoC 上电到应用启动](basics/linux-overview.md)
* [交叉编译与工具链 Cross Compilation and Toolchains](basics/toolchain-cross.md)
* [构建系统：Buildroot 与 Yocto Build Systems: Buildroot and Yocto](basics/buildroot-yocto.md)
* [启动链：从 ROM Code 到 init Boot Flow: From ROM Code to init](basics/boot-flow.md)
* [设备树：从 DTS 到驱动 probe Device Tree](basics/device-tree.md)

## 第二篇 · 内核与驱动

* [内核模块：生命周期、符号导出与调试 Kernel Modules](kernel/kernel-module.md)
* [字符设备：file_operations、阻塞与 ioctl Character Devices](kernel/char-device.md)
* [platform 总线与驱动：匹配、probe 与资源 Platform Bus and Drivers](kernel/platform-driver.md)

## 第三篇 · 用户空间与调试

* [systemd 与启动管理：unit 依赖、启动耗时与看门狗](userspace/systemd.md)
* [网络配置：接口命名、地址、防火墙与 NTP](userspace/network-config.md)
* [调试工具链：gdb、strace、perf、ftrace 与 core dump](userspace/debugging-tools.md)

## 第四篇 · 硬件接口与板级支持

* [显示与触摸：MIPI DSI、LVDS、RGB 接口取舍与面板时序](hardware/display-touch.md)
* [音频：I2S/TDM 时序、codec 与 DAPM、时钟树与 pop 音](hardware/audio.md)

## 第五篇 · 可靠性与升级

* [看门狗与日志：/dev/watchdog、systemd 集成与 journald 落盘](reliability/watchdog-log.md)
* [A/B 升级：GPT 分区、启动计数器、镜像校验与断电回滚](reliability/ab-upgrade.md)

## 第六篇 · 板级实战

* [板级 bring-up：从裸板到第一个用户态程序 Board Bring-up](practice/bring-up.md)
* [板级移植：从参考板到量产的清单 Board Porting Checklist](practice/board-porting.md)
