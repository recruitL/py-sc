# 第五章：数值微分

数值微分研究如何用有限次函数计算或有限个离散采样点近似导数。它看起来像数值积分的逆问题，但在误差行为上通常更敏感：差分公式会把函数值误差、舍入误差和数据噪声除以步长，步长过大时截断误差明显，步长过小时又容易出现相消和舍入误差。

本章主线是：

```text
数值微分基本问题
  -> 前向、后向和中心差分
  -> 函数形式的三点与五点公式
  -> 离散数据形式的三点、五点和非等距权重
  -> 隐式紧致差分格式入口
  -> 三次样条与 B 样条数值微分
  -> Richardson 外推
  -> 二阶数值微分
  -> 统一实验、小结和参考文献
```

## 本章导言

解析求导要求函数表达式清楚、可微结构明确，并且推导成本可接受。实际计算中常见输入并不总是这样：函数可能来自仿真程序、黑箱模型、实验测量或离散数据表；即使函数表达式已知，解析导数也可能复杂、容易出错或不便嵌入程序。

本章区分两类输入：

* **函数型微分**：可以主动计算 \(f(x)\)，因此可以选择步长 \(h\)，并通过步长减半实验观察误差阶；
* **离散数据微分**：只能使用已有节点 \((x_i,y_i)\)，节点可能等距或非等距，数据还可能含有噪声。

典型目标是近似

$$
f'(x),\qquad f''(x),
$$

或在离散数据上估计

$$
y_i\approx f(x_i)
$$

对应的节点导数。总误差可以粗略理解为

$$
\text{总误差}\approx \text{截断误差}+\text{舍入误差}+\text{数据误差}.
$$

第二章的局部插值多项式给出了有限差分权重的来源，第二章的三次样条和 B 样条可以用于离散数据微分；第四章的 Richardson 外推思想可以直接用于提高中心差分精度；本章也为后续常微分方程和偏微分方程的离散化做准备。

## 主要问题

* 前向、后向和中心差分分别适合什么位置？
* 三点公式与五点公式如何从 Taylor 展开或局部插值得到？
* 为什么中心差分通常比单边差分更精确？
* 为什么步长 \(h\) 不是越小越好？
* 离散数据上的微分为什么会放大噪声？
* 非等距节点如何通过局部插值权重统一处理？
* 样条微分和直接有限差分有什么区别？
* Richardson 外推如何消去主导误差项？
* 二阶数值微分为什么通常比一阶微分更敏感？

## 主要算法

本轮已经建立并可运行：

* 前向差分、后向差分、中心差分和中点差分；
* 三点端点一阶导数公式；
* 五点中心和五点单边一阶导数公式；
* 三点中心、三点单边和五点中心二阶导数公式；
* 非等距节点有限差分权重；
* 离散数据节点导数估计；
* Richardson 外推表和中心差分外推；
* 周期边界上的四阶紧致差分示例；
* 自然三次样条的一阶和二阶解析求导；
* 三次均匀 B 样条基函数一阶和二阶导数；
* 误差收敛阶估计。

保留后续扩展入口：

* 一般边界条件下的隐式紧致差分系统；
* 完整 B 样条拟合和节点向量框架；
* 自适应三次均匀 B 样条微分；
* 更稳定的大规模非等距有限差分权重算法。

## 阅读顺序

1. `notebooks/01_differentiation_overview.ipynb`
2. `notebooks/02_finite_difference_formulas.ipynb`
3. `notebooks/03_discrete_data_differentiation.ipynb`
4. `notebooks/04_spline_differentiation.ipynb`
5. `notebooks/05_richardson_and_implicit.ipynb`
6. `notebooks/06_second_derivatives.ipynb`
7. `notebooks/07_experiments.ipynb`
8. `notes/theory.md`
9. `references.md`

## Notebook 对照表

| Notebook | 作用 |
| --- | --- |
| `01_differentiation_overview.ipynb` | 引入函数型和离散数据型微分、误差来源、步长选择和本章导航。 |
| `02_finite_difference_formulas.ipynb` | 推导前向、后向、中心、三点和五点一阶差分公式，并验证收敛阶。 |
| `03_discrete_data_differentiation.ipynb` | 讨论等距和非等距离散数据微分，展示噪声放大和局部插值权重。 |
| `04_spline_differentiation.ipynb` | 说明自然三次样条一阶/二阶求导，并建立 B 样条微分拓展入口。 |
| `05_richardson_and_implicit.ipynb` | 推导 Richardson 外推，给出外推表和周期紧致差分格式示例。 |
| `06_second_derivatives.ipynb` | 推导多点二阶微分公式，比较一阶和二阶微分对噪声的敏感性。 |
| `07_experiments.ipynb` | 汇总 U 形误差曲线、收敛阶、端点/内部节点、样条和外推实验。 |

## 可运行脚本

在仓库根目录运行：

```bash
python chapters/ch05_numerical_differentiation/scripts/differentiation_methods.py
```

脚本是 Notebook 实验的紧凑版本，用于快速检查核心算法和典型数值结果。Notebook 中仍保留教学式推导和实现，不依赖脚本替代讲义内容。

## 代码实现

可复用实现位于：

```text
src/py_sc/differentiation.py
```

主要函数包括：

* `forward_difference`
* `backward_difference`
* `central_difference`
* `three_point_endpoint_derivative`
* `five_point_center_derivative`
* `five_point_endpoint_derivative`
* `finite_difference_weights`
* `differentiate_discrete`
* `richardson_derivative`
* `compact_first_derivative_periodic`
* `natural_cubic_spline_derivative`
* `cubic_uniform_b_spline_basis_derivative`
* `second_derivative_three_point`
* `second_derivative_five_point`
* `observed_order`

Notebook 中会先给出简洁、清晰的教学式实现，再调用这些可复用函数做对照和复用。

## 当前范围

本轮已经完整完成：

* 第五章统一入口；
* 数值微分导言和误差模型；
* 前向、后向、中心差分；
* 函数形式的三点和五点公式；
* 离散数据形式的三点、五点和非等距局部权重；
* Richardson 外推；
* 多点二阶数值微分；
* 自然三次样条一阶和二阶数值微分；
* 统一实验入口、参考文献和回归测试。

暂时作为框架或拓展，后续继续完善：

* 一般非周期边界条件下的隐式紧致差分；
* 完整三次均匀 B 样条拟合、控制点求解和自适应节点策略；
* 面向大规模高阶模板的稳定有限差分权重算法。

## 和前后章节的关系

第二章的插值多项式说明有限差分公式可以看作局部插值多项式的导数。第二章中的自然三次样条和 B 样条为离散数据微分提供了更平滑的函数重构。

第四章的 Richardson 外推和 Romberg 求积展示了“用两个步长消去主误差项”的思想。本章把同一思想用于中心差分，并强调外推在舍入误差主导时会失效。

后续常微分方程和偏微分方程会大量使用差分近似。理解本章的截断误差、舍入误差、边界格式和噪声放大，是理解微分方程离散化稳定性的基础。
