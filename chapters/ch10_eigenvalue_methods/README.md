# 第十章：特征值计算

本章研究矩阵特征值问题

$$
A x = \lambda x,\qquad x \ne 0.
$$

与线性方程组求解相比，特征值计算关注矩阵作用下保持方向不变的向量。它是稳定性分析、主成分分析、振动模态、迭代法收敛速度和矩阵分解算法的共同基础。

## 学习目标

读完本章后，应能：

* 用 Rayleigh 商评价一个近似特征向量对应的特征值；
* 用残差范数判断近似特征对是否可信；
* 理解幂法对模最大特征值的选择机制；
* 用位移反幂法寻找靠近给定位移的特征值；
* 理解 Rayleigh 商迭代把位移动态更新后的快速收敛现象。

## 与前面章节的联系

第七章的迭代法已经展示了谱半径如何控制收敛速度；本章反过来学习如何计算这些谱信息。第六章直接法是反幂法和 Rayleigh 商迭代每步线性求解的基础；第九章 Newton 思想中的“局部线性化 + 迭代修正”也会在 Rayleigh 商迭代中再次出现。

## 阅读顺序

1. `notebooks/01_power_and_inverse_iteration.ipynb`

## Notebook 对照表

| Notebook | 作用 | 状态 |
| --- | --- | --- |
| `01_power_and_inverse_iteration.ipynb` | Rayleigh 商、幂法、位移反幂法和 Rayleigh 商迭代。 | 已建设 |

## 可运行脚本

在仓库根目录运行：

```bash
python chapters/ch10_eigenvalue_methods/scripts/eigenvalue_methods.py
```

## 代码实现

可复用实现位于：

```text
src/py_sc/eigenvalues.py
```

当前已包含：

* `rayleigh_quotient`
* `eigen_residual_norm`
* `normalize_vector`
* `power_method`
* `inverse_power_method`
* `rayleigh_quotient_iteration`

## 本章小结

幂法不断放大初始向量在主特征向量方向上的分量，因此适合估计模最大的特征值。反幂法通过反复求解带位移线性系统，把“靠近位移的特征值”转化为变换后模最大的特征值。Rayleigh 商迭代进一步把位移设为当前 Rayleigh 商，在对称矩阵和合适初值下可以非常快地收敛。三者都应配合特征残差来判断结果，而不只观察相邻特征值估计的变化。
