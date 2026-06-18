# 第四章：数值积分

数值积分研究如何用有限次函数计算或有限个离散样本近似积分。它既是数值分析课程中的基础主题，也是后续物理计算、概率计算、常微分方程、偏微分方程和谱方法中的常用工具。

本章主线是：

```text
数值求积基本原理
  -> Newton-Cotes 求积
  -> 复合求积
  -> Richardson 外推与 Romberg 求积
  -> 自适应 Simpson 积分
  -> 高斯型求积
  -> 离散数据积分
  -> 多重积分
  -> 高维 Monte Carlo 积分
  -> 实验、小结和参考文献
```

## 本章导言

解析积分并不总是可获得。实际计算中常见困难包括：被积函数没有初等原函数、函数来自仿真程序或实验数据、积分区域复杂、维数较高、函数在局部存在尖峰或快速变化。因此数值积分的核心问题是：在有限计算成本下，如何用节点和权重构造稳定、可控、可验证的近似。

本章区分两类输入：

* **函数型积分**：可以按需计算 \(f(x)\)，重点是如何选择节点、权重和误差控制策略；
* **离散数据积分**：只给出采样点 \((x_i,y_i)\)，重点是如何在数据间进行局部插值或平滑近似。

本章也区分三类区域：

* **一维积分**：节点和权重容易分析，是理解误差阶的基础；
* **多重积分**：可以用累次积分、张量积求积和坐标变换处理；
* **高维积分**：张量积节点数随维数指数增长，通常需要 Monte Carlo 或拟 Monte Carlo 思想。

第二章的插值多项式给出了插值型求积公式的来源；第三章的正交多项式给出了高斯型求积公式的来源。阅读本章时应持续关注这两条联系。

## 主要问题

* 求积节点和权重如何决定公式？
* 插值型求积公式为什么能精确积分低次多项式？
* 复合中点、梯形和 Simpson 公式的收敛阶如何通过实验验证？
* Richardson 外推如何把低阶公式提升为 Romberg 求积表？
* 自适应 Simpson 如何把计算资源集中到变化剧烈的区间？
* Gauss-Legendre 节点为什么来自 Legendre 多项式的零点？
* 离散数据积分与可调用函数积分有什么本质区别？
* 多重积分为什么容易遇到维数灾难？
* Monte Carlo 积分为什么在高维问题中仍然有价值？

## 主要算法

本轮已经建立并可运行：

* 中点公式、梯形公式、Simpson 公式、Simpson 3/8 公式；
* 闭型和开型 Newton-Cotes 权重构造；
* 复合中点、复合梯形、复合 Simpson；
* Romberg 求积表；
* 自适应 Simpson 积分和接受区间记录；
* Gauss-Legendre 节点权重的 Golub-Welsch 教学实现；
* Gauss-Chebyshev、Gauss-Laguerre、Gauss-Hermite 的标准权函数求积；
* 离散梯形、局部二次 Simpson、平均抛物线、自然三次样条积分；
* 矩形区域张量积 Gauss-Legendre 和二维复合 Simpson；
* 变限积分和高维 Monte Carlo / 指示函数 Monte Carlo 的基础实现。

保留后续扩展入口：

* 高阶 Newton-Cotes 公式稳定性专题；
* Gauss-Laguerre 和 Gauss-Hermite 节点构造的完整正交多项式推导；
* 一般不规则区域积分的系统处理；
* 奇异积分、振荡积分和无限区间变换；
* 拟 Monte Carlo、重要性采样和方差缩减。

## 阅读顺序

1. `notebooks/01_integration_overview.ipynb`
2. `notebooks/02_newton_cotes_and_composite.ipynb`
3. `notebooks/03_romberg_and_adaptive.ipynb`
4. `notebooks/04_gaussian_quadrature.ipynb`
5. `notebooks/05_discrete_data_integration.ipynb`
6. `notebooks/06_multiple_and_monte_carlo_framework.ipynb`
7. `notebooks/07_experiments.ipynb`
8. `notes/theory.md`
9. `references.md`

## Notebook 对照表

| Notebook | 作用 |
| --- | --- |
| `01_integration_overview.ipynb` | 引入数值积分问题、求积节点与权重、插值型公式、代数精度和误差观念。 |
| `02_newton_cotes_and_composite.ipynb` | 推导 Newton-Cotes 典型公式，比较复合梯形和复合 Simpson 的误差阶。 |
| `03_romberg_and_adaptive.ipynb` | 讲解 Richardson 外推、Romberg 求积表和自适应 Simpson 的区间细分。 |
| `04_gaussian_quadrature.ipynb` | 从正交多项式解释高斯型求积，重点实现 Gauss-Legendre，并给出带权公式对照。 |
| `05_discrete_data_integration.ipynb` | 讨论离散采样数据上的梯形、局部二次、平均抛物线和样条积分。 |
| `06_multiple_and_monte_carlo_framework.ipynb` | 建立多重积分、张量积求积、变限积分、高维 Monte Carlo 的统一框架；部分高级内容待完善。 |
| `07_experiments.ipynb` | 汇总收敛阶、Romberg 表、自适应区间、Gauss 对比、离散积分、二维积分和 Monte Carlo 实验。 |

## 可运行脚本

在仓库根目录运行：

```bash
python chapters/ch04_numerical_integration/scripts/integration_methods.py
```

脚本是 Notebook 实验的紧凑版本，用于快速检查核心算法和典型结果。Notebook 中仍保留教学式实现和推导，不依赖脚本替代讲义内容。

## 代码实现

可复用实现位于：

```text
src/py_sc/integration.py
```

主要函数包括：

* `composite_trapezoid`
* `composite_simpson`
* `romberg_integrate`
* `adaptive_simpson`
* `gauss_legendre_nodes_weights`
* `gauss_legendre_integrate`
* `discrete_trapezoid`
* `discrete_simpson`
* `natural_cubic_spline_integral`
* `tensor_product_gauss_legendre`
* `monte_carlo_integrate`

Notebook 中会先给出简洁的教学式实现，再调用这些可复用函数做对照和复用。

## 当前范围

本轮已经完整完成：

* 第四章统一入口；
* 数值求积基本原理；
* Newton-Cotes 典型公式和复合求积；
* Romberg 求积；
* 自适应 Simpson 求积；
* Gauss-Legendre 求积的较完整教学式实现；
* 离散数据积分基础；
* 实验入口和参考文献；
* 可复用公共算法与回归测试。

暂时作为框架、后续继续完善：

* Gauss-Laguerre 和 Gauss-Hermite 的完整节点构造推导；
* 一般区域多重积分的系统算法；
* 高维 Monte Carlo 的方差缩减、重要性采样和拟 Monte Carlo；
* 奇异积分、振荡积分和无限区间积分专题。

## 和前后章节的关系

第二章从插值多项式出发，说明如何用有限节点重构函数。Newton-Cotes 公式正是把插值多项式积分后得到的求积公式。

第三章从正交多项式和投影观点出发，说明基函数正交性如何改善逼近稳定性。Gauss-Legendre、Gauss-Chebyshev、Gauss-Laguerre 和 Gauss-Hermite 求积都依赖正交多项式的节点和权重。

后续数值微分、常微分方程和偏微分方程会继续使用本章思想：误差阶、局部细分、外推、加权残差和高维积分都会反复出现。
