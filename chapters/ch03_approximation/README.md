# 第三章：函数逼近与曲线拟合

函数逼近与曲线拟合关心的是：如何用一个结构较简单、可计算、可存储的函数去近似一个复杂函数或一组离散数据。本章延续第二章“数据插值”的主题，但重点从“严格通过节点”转向“在某种误差意义下整体接近”。

本章第一轮建设的主线是：

```text
插值、逼近、拟合的区别
  -> 逼近空间与误差范数
  -> Chebyshev 多项式逼近
  -> Legendre 级数逼近
  -> 最佳逼近多项式的基本框架
  -> 多项式最小二乘曲线拟合
  -> Padé 有理分式逼近
  -> Fourier/FFT 与自适应逼近扩展框架
```

## 本章导言

第二章的数据插值要求

$$
p(x_i)=f(x_i),\qquad i=0,1,\dots,n.
$$

这在查表、无噪声函数采样和局部重构中很自然，但它不是所有问题的最佳选择。若目标是用低维函数空间近似连续函数，或用简单模型描述含噪声数据，通常更关心整体误差，而不是每个节点都精确相等。

本章把三类问题区分开：

* **插值**：给定节点，构造函数严格通过所有数据点；
* **函数逼近**：给定目标函数 \(f\)，在某个函数空间 \(V_n\) 中寻找 \(p_n\)，使误差 \(\|f-p_n\|\) 小；
* **曲线拟合**：给定离散观测数据，允许残差，寻找整体上最能解释数据的模型。

常用误差度量包括：

$$
\|f-g\|_\infty=\max_{x\in[a,b]}|f(x)-g(x)|,
$$

$$
\|f-g\|_2=\left(\int_a^b |f(x)-g(x)|^2 w(x)\,dx\right)^{1/2},
$$

以及离散数据上的二范数

$$
\|r\|_2=\left(\sum_{i=1}^m r_i^2\right)^{1/2}.
$$

不同范数对应不同意义下的“最好”。一致范数强调最坏点误差，平方范数强调平均意义，离散二范数则是最小二乘拟合的基础。

## 主要问题

* 逼近与插值有什么关系？什么时候应该避免强制插值？
* 为什么 Chebyshev 多项式适合控制区间上的整体误差？
* 为什么 Legendre 多项式自然对应平方范数投影？
* 最小二乘拟合如何从法方程和投影观点得到？
* 为什么 Vandermonde 矩阵会导致高次多项式拟合不稳定？
* Padé 逼近为什么能比 Taylor 多项式更好地处理极点或远离展开点的行为？
* Fourier/FFT 和自适应逼近在本章体系中处于什么位置？

## 主要算法

本轮已经建立并可运行：

* Chebyshev 多项式基函数与 Chebyshev 级数拟合；
* Legendre 多项式投影逼近；
* 幂基多项式最小二乘拟合；
* Padé 有理分式逼近；
* 自适应分段线性逼近的基本框架。

保留后续扩展入口：

* 最佳一致逼近与极小极大思想；
* Remez 算法；
* Fourier 级数、离散 Fourier 变换与 FFT；
* Gibbs 现象专题实验；
* 自适应三次样条逼近；
* 正交多项式最小二乘拟合；
* 正则化曲线拟合。

## 阅读顺序

1. `notebooks/01_approximation_overview.ipynb`
2. `notebooks/02_chebyshev_legendre_approximation.ipynb`
3. `notebooks/03_least_squares_fitting.ipynb`
4. `notebooks/04_pade_approximation.ipynb`
5. `notebooks/05_experiments_framework.ipynb`
6. `notes/theory.md`
7. `references.md`

## Notebook 对照表

| Notebook | 作用 |
| --- | --- |
| `01_approximation_overview.ipynb` | 区分插值、函数逼近和曲线拟合，引入逼近空间与误差范数。 |
| `02_chebyshev_legendre_approximation.ipynb` | 从正交多项式出发，讲解 Chebyshev 和 Legendre 级数逼近，并展示误差图像。 |
| `03_least_squares_fitting.ipynb` | 讨论离散最小二乘、多项式拟合、法方程、Vandermonde 病态性和过拟合。 |
| `04_pade_approximation.ipynb` | 推导 Padé 系数方程，并与 Taylor 多项式做对比实验。 |
| `05_experiments_framework.ipynb` | 建立 Fourier/FFT、自适应逼近、Gibbs 现象和正交拟合等后续实验入口。 |

## 可运行脚本

在仓库根目录运行：

```bash
python chapters/ch03_approximation/scripts/orthogonal_approximation.py
python chapters/ch03_approximation/scripts/least_squares_fitting.py
python chapters/ch03_approximation/scripts/pade_approximation.py
python chapters/ch03_approximation/scripts/adaptive_linear_demo.py
```

这些脚本是 Notebook 示例的紧凑版本，用于快速检查核心算法和图像是否能运行。Notebook 中仍保留了教学式实现和推导，不依赖脚本替代讲义内容。

## 代码实现

可复用实现位于：

```text
src/py_sc/approximation.py
```

主要函数包括：

* `chebyshev_fit_function`
* `chebyshev_series_eval`
* `legendre_fit_function`
* `legendre_series_eval`
* `polynomial_least_squares`
* `polynomial_eval`
* `pade_from_taylor`
* `pade_eval`
* `adaptive_piecewise_linear`

Notebook 中会先给出简洁的教学式实现，再调用这些可复用函数做对照和复用。

## 当前范围

本轮已经完成：

* 第三章统一入口；
* 插值、逼近、拟合区别的导言；
* 一致范数、平方范数和离散二范数的基本说明；
* Chebyshev 多项式与 Chebyshev 级数逼近；
* Legendre 级数逼近的基本框架；
* 多项式最小二乘拟合；
* Padé 逼近基本框架；
* 若干可运行实验脚本；
* 第三章参考文献。

暂时只建立框架，后续继续扩展：

* 最佳一致逼近与 Remez 算法；
* FFT 的完整推导；
* Gibbs 现象专题实验；
* 自适应三次样条逼近；
* 正交多项式最小二乘拟合；
* 正则化拟合的系统讨论。

## 和第二章的关系

第二章强调由离散节点构造插值函数。第三章保留 Chebyshev 节点和多项式插值的联系，但重点转向逼近空间、误差范数和整体最优思想。Chebyshev 零点插值在本章中被看作函数逼近工具，而不是简单重复第二章的插值公式。
