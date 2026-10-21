---
id: quiz-mcu
title: 单片机与嵌入式硬件测试题
part: 9
chapter: 硬件测试与面试题库
order: 25
tags: [题库, 自测, 单片机, 嵌入式]
difficulty: 2
status: published
sources:
  - STM32 Reference Manual (RM0008 / RM0383)
  - NXP / Microchip 微控制器应用笔记
  - Jan Axelson, Serial Port / USB Complete
---

# 单片机与嵌入式硬件测试题

本题库覆盖 MCU 架构、最小系统、GPIO 驱动、中断、ADC/DAC、定时器与 PWM、UART/RS-232、RS-485/CAN、I²C/SPI、USB/以太网物理层、看门狗/RTC/低功耗、外设设计。题型分为「概念判断」「填空」「计算」「简答与情景」四组。

## 一、概念判断

<details><summary>判断：MCU 的最小系统只需要芯片本身就能工作，不需要外部晶振、复位和电源去耦。</summary>

**错误。**最小系统（Minimum System）包括：供电（含去耦电容）、时钟（内部 RC 或外部晶振）、复位电路、调试接口（SWD/JTAG）。多数现代 MCU 有内部 RC 振荡器可省外部晶振，但去耦电容与复位必须有。

</details>

<details><summary>判断：GPIO 设为推挽输出可以可靠地输出高/低电平；设为开漏输出时必须外接上拉电阻才能输出高电平。</summary>

**正确。**推挽（Push-Pull）由上下两个 MOS 驱动，主动输出 0/1。开漏（Open-Drain）只能主动拉低，高电平靠外部上拉电阻，常用于 I²C 总线、电平转换、多线与。

</details>

<details><summary>判断：中断优先级高的可以打断正在执行的优先级低的中断（中断嵌套），但同级或更高级不能被低级打断。</summary>

**正确。**中断控制器（NVIC）按优先级裁决，高优先级可抢占低优先级实现嵌套；同级一般不互相抢占（除非子优先级）。设计时要避免在高优先级中断里做耗时操作，否则阻塞低优先级。

</details>

<details><summary>判断：ADC 的分辨率是 12 位、参考电压 3.3V，则 1LSB 对应的电压约为 0.8mV。</summary>

**正确。**$1\text{LSB}=V_{ref}/2^n=3.3/4096\approx 0.805\text{mV}$。量化误差 ±1/2 LSB ≈ ±0.4mV。

</details>

<details><summary>判断：PWM 的频率由定时器溢出决定，占空比由比较寄存器与自动重装值的比值决定。</summary>

**正确。**PWM（脉宽调制）：定时器计数到自动重装值 ARR 产生周期，计数到比较值 CCR 时翻转输出。频率 $f_{PWM}=f_{clk}/((ARR+1)(PSC+1))$，占空比 = CCR/ARR。

</details>

<details><summary>判断：I²C 是开漏、双线、多主总线，靠设备地址寻址；SPI 是四线、通常单主多从，靠片选寻址。</summary>

**正确。**I²C：SCL/SDA 两线、开漏上拉、7/10 位地址、半双工。SPI：MOSI/MISO/SCLK/CS 四线、推挽、全双工、速率高、无内置地址协议靠片选。

</details>

<details><summary>判断：RS-485 用差分信号传输，抗共模干扰强、可远距离（数百米）和多节点组网；RS-232 单端、距离短（约 15m）、点对点。</summary>

**正确。**RS-485 差分（A/B 线），±2V 阈值，多点半双工；RS-232 单端 ±12V 电平，点对点、距离短。CAN 是差分、多主、带错误检测的总线，用于汽车/工业。

</details>

<details><summary>判断：看门狗（Watchdog）必须由软件定期"喂狗"，否则溢出后复位 MCU，用于防止程序跑飞。</summary>

**正确。**看门狗定时器递增，若软件在设定时间内未喂狗，发生系统复位。硬件看门狗独立于主 MCU，可靠性更高，用于工业现场防死机。

</details>

## 二、填空

<details><summary>GPIO 常见工作模式：输入 ____ / ____ / ____；输出 ____ / ____。</summary>

输入：浮空、上拉、下拉；输出：推挽、开漏。模拟输入模式（接 ADC）应配置为模拟、断开数字输入缓冲。

</details>

<details><summary>ADC 采样前必须保证 ____ 建立时间；采样速率受 ____ 与 ____ 限制。多通道扫描时需注意 ____。</summary>

保持电容充电建立（采样电容）。受时钟 $ADCCLK$ 与采样时间限制；多通道切换需加通道间转换延迟/采样时间以等待源阻抗建立。高内阻信号源要加大采样时间或加缓冲。

</details>

<details><summary>UART 四要素：____、____、____、____ 必须收发双方一致。</summary>

波特率（Baud Rate）、数据位（5~9）、停止位（1/1.5/2）、校验位（无/奇/偶）。缺一个就乱码。

</details>

<details><summary>低功耗模式按功耗由高到低：运行 → ____ → ____ → 停机/待机；唤醒源通常为 ____、____、RTC。</summary>

运行 → 睡眠（Sleep，CPU 停、外设跑）→ 停止（Stop，时钟停、RAM 保持）→ 待机（Standby，RAM 丢失）。唤醒源：外部中断（EXTI）、RTC、复位脚。

</details>

<details><summary>RTC（实时时钟）靠 ____ 供电走时；后备电池 VBAT 在主电源掉电后维持 ____。</summary>

32.768kHz 晶振（分频 $2^{15}=32768$ 得 1Hz）。VBAT 维持 RTC 与后备寄存器走时，主电掉电不丢时间。

</details>

## 三、计算

<details><summary>12 位 ADC，$V_{ref}=3.3\text{V}$，采样得到数字量 $D=2048$。求输入电压；若输入 1.65V，理论数字量是多少？</summary>

$V_{in}=D\cdot V_{ref}/2^{12}=2048\times 3.3/4096=1.65\text{V}$。
输入 1.65V 对应 $D=1.65/3.3\times 4096=2048$（正好一半）。
注意这是理想值，实际有 ±1/2 LSB 量化误差与 INL/DNL。

</details>

<details><summary>PWM：定时器时钟 72MHz，预分频 PSC=71（分频后 1MHz），自动重装 ARR=999。求 PWM 频率与占空比 50% 时的 CCR 值。</summary>

计数频率 $f_{cnt}=72\text{MHz}/(71+1)=1\text{MHz}$。
PWM 频率 $f_{PWM}=f_{cnt}/(ARR+1)=1\text{MHz}/1000=1\text{kHz}$。
占空比 50%：CCR = 0.5 × (ARR+1) = 500（向上计数模式）。

</details>

<details><summary>UART 波特率 9600，传输 1 字节（含起始位、8 数据位、1 停止位，共 10 位）需要多少时间？</summary>

每比特时间 $T_b=1/9600\approx 104.2\,\mu\text{s}$。
1 帧 10 位：$T_{frame}=10/9600\approx 1.04\text{ms}$。
1 秒约传 960 字节（9600/10）。115200 时单字节约 $10/115200\approx 86.8\,\mu\text{s}$。

</details>

<details><summary>STM32 I²C 标准模式 100kHz，传输 1 字节（含 ACK）需要多少时间？若 400kHz 快速模式呢？</summary>

1 字节数据 8 位 + 起始/地址 + ACK，粗略按 9 位（数据+应答）算：
100kHz：$9/100\text{k}=90\,\mu\text{s}$（不含起始位与地址字节开销，实际更长）。
400kHz：$9/400\text{k}=22.5\,\mu\text{s}$。
注意 I²C 还有起始、地址字节、重复起始等开销，整帧传输时间要按完整帧位宽算。

</details>

<details><summary>某 MCU 每路 GPIO 高电平可吸收/输出 8mA。一只 LED 接 3.3V、正向压降 2V、要 5mA。求限流电阻；GPIO 是否够驱动？</summary>

$R=(V_{dd}-V_F)/I=(3.3-2)/0.005=260\,\Omega$，取 270Ω。
GPIO 输出 5mA < 8mA 额定，足够；但要查数据手册总灌/拉电流限制（如单端口 ≤ 25mA），多只 LED 同时亮需核算总量。

</details>

## 四、简答与情景

<details><summary>情景：PCB 上 MCU 偶尔复位，断电重开正常，现场长时间运行后概率上升。怀疑看门狗或电源，如何区分？</summary>

(1) 先测电源：用示波器看掉电瞬间 $V_{dd}$ 是否跌出 BOR/POR 阈值（欠压复位），纹波是否过大；(2) 查复位脚波形，区分是看门狗复位、BOR 复位还是外部噪声；(3) 读复位原因寄存器（RCC_CSR），看是 IWDG/WWDG/POR/低功耗复位标志；(4) 检查程序是否在中断/循环里漏喂狗。对策：加强去耦、合理喂狗、加硬件看门狗。

</details>

<details><summary>简答：I²C 总线挂多个设备拉不起来（SDA 一直低），硬件排查顺序？</summary>

(1) 查上拉电阻取值（100kHz 一般 4.7k，400kHz 需更小）与是否焊接；(2) 查某设备是否拉死 SDA（从机异常或寻址错误导致时钟拉伸/锁死），逐个断电定位；(3) 查地址冲突；(4) 查 SDA/SCL 是否接反；(5) 总线电容过大时降速。常见复位办法：主机手动发 9 个时钟脉冲释放从机状态。

</details>

<details><summary>情景：ADC 采集的温度信号在静止时数值跳动十几 mV。硬件与软件上如何稳定？</summary>

硬件：(1) 信号源阻抗高时加运放缓冲；(2) RC 低通滤波（如 1k + 0.1µF，截止约 1.6kHz）；(3) PCB 上模拟地/数字地单点连接，避开数字噪声；(4) $V_{ref}$ 加去耦、用独立基准源。
软件：(1) 多次采样取平均/中值滤波；(2) 过采样提高有效位数；(3) 看门狗式异常剔除。

</details>

<details><summary>简答：为什么 USB、以太网这类高速接口需要严格的阻抗匹配和差分走线，而普通 UART 不需要？</summary>

USB（Full/High Speed）、以太网（MII/RGMII、1000BASE-T）速率达数百 Mbps，信号边沿快，传输线效应明显：阻抗不连续产生反射、串扰导致误码。必须按差分阻抗 90Ω（USB）/100Ω（以太网）等控制走线。UART 几十 kbps~几 Mbps，边沿慢、线长短，反射与串扰可忽略，普通走线即可。

</details>
