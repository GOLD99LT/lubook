---

id: math-basics
title: "数学基础：复数、dB 与拉氏变换直觉 Math Basics: Complex Numbers, dB, Laplace"
part: 1
chapter: 数学基础
order: 70
tags: [复数, dB, 对数, 拉氏变换, s域, 数学基础]
difficulty: 2
status: published
sources:
  - Lessons In Electric Circuits (Kuphaldt)
  - Khan Academy · Electrical Engineering
  - Design with Operational Amplifiers (Franco)
---

# 数学基础：复数、dB 与拉氏变换直觉 Math Basics: Complex Numbers, dB, Laplace

前面几章用到了复数阻抗、分贝 dB、传递函数 $H(s)$。这一章不做严格推导，只建立**够用的直觉**：复数怎么表示相位、dB 怎么算倍数、拉氏变换在工程上到底是干嘛的。推导一律折叠。

## 1. 设计动机

::: motivation 为什么要补这三个数学工具
算滤波器要写 $H(s)$，看伯德图要用 dB，分析交流要用复数。你不需要会手推拉氏变换，但必须看懂 $Z=R+jX$ 里 j 是什么意思、+20dB 代表放大几倍、传递函数里的 s 代表什么。这是阅读后续滤波、反馈、频率响应章节的门槛。
:::

## 2. 复数与阻抗（只给结论）

![复数平面：阻抗 Z = R + jX，实部是电阻、虚部是电抗，模是总阻抗大小，幅角是相位](../assets/schematics/math-basics.svg)

在交流电路里，电压电流既有大小又有相位差，用**复数**表示最方便：

- 复数 $Z=R+jX$：$R$ 是实部（电阻，与电压同相），$X$ 是虚部（电抗，电压电流差 90°）。
- $j=\sqrt{-1}$，它的物理意义是"相位转 90°"：$j$ 让阻抗超前 90°（电感），$-j$ 滞后 90°（电容）。
- **模** $|Z|=\sqrt{R^2+X^2}$ 决定电流大小；**幅角** $\theta=\arctan(X/R)$ 决定相位差。

::: analogy 复数 = 大小 + 方向
把复数想象成平面上的一根箭头：长度是"大小"，角度是"方向（相位）"。做加减看实部虚部，做乘除看长度和角度。阻抗 $Z=R+jX$ 就是"既阻碍电流、又错开相位"的合成。
:::

## 3. 分贝 dB（只记结论）

放大器增益、滤波器衰减、信噪比，都用分贝 dB 表示。功率比的分贝定义：

$$G_{dB}=10\log_{10}\frac{P_{out}}{P_{in}}$$

电压比（同阻抗下）：

$$G_{dB}=20\log_{10}\frac{V_{out}}{V_{in}}$$

记住这几个常用换算，终身够用：

| 倍数（电压/功率） | dB |
|---|---|
| ×1（不变） | 0 dB |
| ×2 | +6 dB（电压）/ +3 dB（功率） |
| ×10 | +20 dB（电压）/ +10 dB（功率） |
| ×0.5（减半） | −6 dB |
| ×0.1（衰减到 1/10） | −20 dB |

直觉：**每 +20 dB 电压放大 10 倍，每 −20 dB 衰减到 1/10**。dB 的好处是把极大/极小的倍数压成好读的数，而且级联电路的增益直接相加。

::: advanced 进阶：为什么电压用 20、功率用 10
功率正比于电压平方 $P=V^2/R$，所以 $10\log(P_o/P_i)=10\log(V_o^2/V_i^2)=20\log(V_o/V_i)$。两个定义等价，只是基不同。
:::

## 4. 拉氏变换 $s$ 的直觉

传递函数写作 $H(s)$，其中 $s=\sigma+j\omega$。工程上你只需要建立这个直觉：

- $s$ 同时编码了**频率 $\omega$**（交流多快）和**衰减 $\sigma$**（暂态怎么收敛）。
- 把微分方程 $RC\,dV/dt+V=V_{in}$ 变成代数方程：$\frac{V_{out}}{V_{in}}=\frac{1}{1+sRC}$——解电路变成了"代入 $s=j\omega$ 算复数"。
- 令 $s=j\omega$（$\sigma=0$，纯正弦稳态），就得到频率响应 $H(j\omega)$，即伯德图。

::: analogy $s$ 是"变化方式"的代号
$j\omega$ 部分说"信号以多快频率振荡"，$\sigma$ 部分说"包络是涨还是衰"。拉氏变换把"解微分方程"换成"代入代数表达式算复数"，是工程师偷懒的核心工具——你不必会积分，只要会代入 $s=j\omega$。
:::

## 5. 带数字的算例

::: example 算几个 dB
1. 电压放大 100 倍 → $20\log100=$ **+40 dB**。
2. 衰减到 1/100 → **−40 dB**。
3. 两级放大器：第一级 +20dB、第二级 +26dB → 总增益 **+46dB**（直接相加），相当于电压放大 $10^{46/20}\approx 200$ 倍。
4. 功率：发射 1W、接收 1µW → $10\log(10^{-6}/1)=-60$ dB。
:::

## 6. 常见坑

::: pitfall 常见坑
- **电压增益和功率增益的 dB 系数搞混**：现象——算出来差一倍。原因——电压用 20log、功率用 10log。解决——先问自己是电压比还是功率比，再选系数。
- **以为 dB 是绝对单位**：现象——看到 "−3dB" 不知道是相对谁。原因——dB 是**比值**，相对量。绝对功率要写 dBm（相对于 1mW）。解决——−3dB 只是"减半/半功率点"，不代表具体瓦数。
- **看到 $H(s)$ 就怕，以为要推微分方程**：现象——滤波器电路不敢碰。原因——被拉氏变换的数学外表吓到。解决——记住"$s$ 就是个代入变量，令 $s=j\omega$ 算复数即可"，手算交给仿真。
:::

## 7. 自测题

<details><summary>电压放大 1000 倍是多少 dB？</summary>

$20\log_{10}1000=20\times3=$ **+60 dB**。（每 10 倍 +20dB，1000=10³ → +60dB。）
</details>

<details><summary>阻抗 Z=3+j4 Ω，它的模是多少？</summary>

$|Z|=\sqrt{3^2+4^2}=\sqrt{25}=$ **5 Ω**。幅角 $\theta=\arctan(4/3)\approx53^{\circ}$。电流大小 $I=V/|Z|$，相位差 53°。
</details>

<details><summary>传递函数 H(s)=1/(1+sRC)，做正弦稳态频率分析时 s 代入什么？</summary>

令 $s=j\omega$，得 $H(j\omega)=1/(1+j\omega RC)$。这就是一阶 RC 低通滤波器的频率响应，后续滤波器章节反复用。
</details>

## 8. 参考资料

- [Lessons In Electric Circuits — Complex Numbers](https://www.ibiblio.org/kuphaldt/electricCircuits/)
- [Khan Academy — Electrical Engineering](https://www.khanacademy.org/science/electrical-engineering)
- Design with Operational Amplifiers (Franco) — Laplace / Frequency Response chapter
