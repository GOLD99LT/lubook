# 嵌入式 Linux 手册

> 本文件是装配清单：页面顺序、编号、导航由它决定。新增章节 = 写 Markdown + 在此加一行。

## 第一篇 · 系统与构建

* [嵌入式 Linux 全景：从 SoC 上电到应用启动](basics/linux-overview.md)
* [交叉编译与工具链 Cross Compilation and Toolchains](basics/toolchain-cross.md)
* [构建系统：Buildroot 与 Yocto Build Systems: Buildroot and Yocto](basics/buildroot-yocto.md)
* [启动链：从 ROM Code 到 init Boot Flow: From ROM Code to init](basics/boot-flow.md)
* [设备树：从 DTS 到驱动 probe Device Tree](basics/device-tree.md)
* [内核配置与裁剪：Kconfig、模块与启动时间 Kernel Configuration and Trimming](basics/kernel-config.md)

## 第二篇 · 内核与驱动

* [内核模块：生命周期、符号导出与调试 Kernel Modules](kernel/kernel-module.md)
* [字符设备：file_operations、阻塞与 ioctl Character Devices](kernel/char-device.md)
* [platform 总线与驱动：匹配、probe 与资源 Platform Bus and Drivers](kernel/platform-driver.md)
* [中断与并发：上下半部、原子上下文与锁的选择](kernel/interrupt-concurrency.md)
* [DMA 与内存：一致性、流式映射与 cache 维护](kernel/dma-memory.md)
* [电源管理：runtime PM、系统休眠与功耗账](kernel/power-management.md)

## 第三篇 · 用户空间与调试

* [systemd 与启动管理：unit 依赖、启动耗时与看门狗](userspace/systemd.md)
* [网络配置：接口命名、地址、防火墙与 NTP](userspace/network-config.md)
* [调试工具链：gdb、strace、perf、ftrace 与 core dump](userspace/debugging-tools.md)
* [OTA 客户端：RAUC/SWUpdate 的槽位、状态机与回滚 OTA Clients](userspace/ota-agent.md)
* [容器与沙箱：namespace、cgroup 与只读 rootfs Containers and Sandboxes](userspace/containers.md)

## 第四篇 · 硬件接口与板级支持

* [显示与触摸：MIPI DSI、LVDS、RGB 接口取舍与面板时序](hardware/display-touch.md)
* [音频：I2S/TDM 时序、codec 与 DAPM、时钟树与 pop 音](hardware/audio.md)
* [存储：eMMC/UFS/SD 的协议、HS 时序、分区与寿命](hardware/storage-emmc.md)
* [Camera 与 ISP：CSI-2 速率、V4L2 管线与 3A 收敛](hardware/camera-isp.md)
* [PCIe 与 USB 主机：链路训练、枚举、BAR 与带宽预算](hardware/pcie-usb.md)

## 第五篇 · 可靠性与升级

* [看门狗与日志：/dev/watchdog、systemd 集成与 journald 落盘](reliability/watchdog-log.md)
* [A/B 升级：GPT 分区、启动计数器、镜像校验与断电回滚](reliability/ab-upgrade.md)
* [安全启动：信任链、密钥层级、防回滚与验签预算](reliability/secure-boot.md)
* [产线测试与校准：测试项设计、节拍预算、良率与追溯](reliability/factory-test.md)

## 第六篇 · 板级实战

* [板级 bring-up：从裸板到第一个用户态程序 Board Bring-up](practice/bring-up.md)
* [板级移植：从参考板到量产的清单 Board Porting Checklist](practice/board-porting.md)
* [性能调优：启动剖析、CPU 与 IO、火焰图与回归](practice/performance-tuning.md)
