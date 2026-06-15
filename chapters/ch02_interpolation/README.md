# 第二章：数据插值

插值根据一组已知离散数据点估计未知位置的函数值。本章介绍插值问题的数学动机、基本算法、Python 实现和数值实验。阅读时应把它看作一章可运行的电子讲义，而不是若干彼此孤立的脚本。

第一轮建设的主线是：

```text
插值问题的基本形式
  -> 全局多项式插值
  -> 插值误差与 Runge 现象
  -> 切比雪夫节点
  -> 牛顿差商
  -> Hermite 插值
  -> 分段线性插值
  -> 自然三次样条插值
```

Hermite 插值已经在全局多项式插值部分给出基本入口；PCHIP、B 样条和二维插值暂时作为扩展框架保留，后续可以在不改变章节布局的前提下逐步补全。

## 主要问题

* 如何由有限个数据点重构一个函数？
* 为什么高次多项式插值可能变得不稳定？
* 分段插值牺牲了什么，又换来了什么？
* 三次样条如何在相邻区间之间施加光滑性？

## 主要算法

* 拉格朗日插值（Lagrange interpolation）
* 牛顿差商（Newton divided differences）
* 切比雪夫节点（Chebyshev nodes）
* 分段线性插值
* 自然三次样条插值
* Hermite 插值的基本形式
* 扩展路线：PCHIP、三次均匀 B 样条、双线性插值和三角形单元上的二维一次插值

## 阅读顺序

1. `notebooks/01_interpolation_overview.ipynb`
2. `notebooks/02_polynomial_interpolation.ipynb`
3. `notebooks/03_piecewise_and_spline.ipynb`
4. `notebooks/04_experiments.ipynb`
5. `notebooks/05_extensions_framework.ipynb`
6. `notes/theory.md`
7. `references.md`

## Notebook 对照表

| Notebook | 作用 |
| --- | --- |
| `01_interpolation_overview.ipynb` | 定义插值问题，比较插值与拟合，并引入插值空间。 |
| `02_polynomial_interpolation.ipynb` | 讨论拉格朗日形式、牛顿差商、Hermite 插值、Runge 现象和切比雪夫节点。 |
| `03_piecewise_and_spline.ipynb` | 比较局部分段线性插值和自然三次样条插值。 |
| `04_experiments.ipynb` | 用可复现实验观察误差变化和方法局限。 |
| `05_extensions_framework.ipynb` | 为 Hermite、PCHIP、B 样条和二维插值保留可运行扩展入口。 |

## 可运行脚本

在仓库根目录运行：

```bash
python chapters/ch02_interpolation/scripts/polynomial_interpolation.py
python chapters/ch02_interpolation/scripts/piecewise_interpolation.py
python chapters/ch02_interpolation/scripts/cubic_spline_interpolation.py
python chapters/ch02_interpolation/scripts/compare_interpolation.py
```

这些脚本是 Notebook 示例的紧凑版本，适合快速检查算法是否能运行。

## 代码实现

可复用的教学实现位于：

```text
src/py_sc/interpolation.py
```

这些函数优先服务于教学清晰度，不追求过度工程化。

## 当前范围

本轮已经完成：

* 插值问题的基本形式；
* 插值与最小二乘拟合的区别；
* 拉格朗日插值与插值基函数；
* 插值误差和 Runge 现象；
* 切比雪夫节点与切比雪夫节点插值；
* 牛顿差商；
* Hermite 插值的基本条件和单区间三次 Hermite 示例；
* 分段线性插值；
* 自然三次样条的构造和三对角线性方程组求解；
* 带误差比较的实验 Notebook。

暂时只建立框架，后续继续扩展：

* PCHIP 和保形插值；
* 三次均匀 B 样条；
* 双线性插值和三角形单元上的二维插值；
* 作为后续谱方法章节内容的切比雪夫微分矩阵。
