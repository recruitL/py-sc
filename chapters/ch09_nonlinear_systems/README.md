# 第九章：非线性方程组解法

本章研究多元非线性方程组

$$
F(x)=0,\qquad F:\mathbb{R}^n\to\mathbb{R}^n.
$$

与第八章的标量求根相比，非线性方程组的主要新困难是变量之间相互耦合。Newton 法不再除以一个导数，而是每步求解一个线性方程组；不动点迭代也需要关注向量映射的压缩性、范数选择和残差停止准则。

## 学习目标

读完本章后，应能：

* 将简单非线性方程组改写为向量不动点迭代；
* 写出多元 Newton 法的线性化方程；
* 用残差范数和步长范数判断收敛；
* 理解 Jacobian 奇异、初值敏感和阻尼保护的必要性；
* 为后续拟 Newton、Broyden 和延拓思想建立基础。

## 与前面章节的联系

第八章的标量 Newton 法在本章推广为线性系统求解问题。第七章的迭代线性方程组方法可用于大型 Newton 步的内层求解；第五章的数值微分可用于近似 Jacobian。

## 阅读顺序

1. `notebooks/01_fixed_point_and_newton_systems.ipynb`
2. 后续将继续补充阻尼 Newton、弦 Newton、Broyden 与延拓思想。

## Notebook 对照表

| Notebook | 作用 | 状态 |
| --- | --- | --- |
| `01_fixed_point_and_newton_systems.ipynb` | 向量不动点迭代、多元 Newton 法、残差和奇异 Jacobian。 | 已建设 |
| `02_damped_and_chord_newton.ipynb` | 阻尼 Newton、弦 Newton、有限差分 Jacobian。 | 待建设 |
| `03_broyden_and_continuation.ipynb` | Broyden 拟 Newton、参数延拓和路径跟踪入口。 | 待建设 |

## 可运行脚本

在仓库根目录运行：

```bash
python chapters/ch09_nonlinear_systems/scripts/nonlinear_system_methods.py
```

## 代码实现

可复用实现位于：

```text
src/py_sc/nonlinear_systems.py
```

当前已包含：

* `fixed_point_system_iteration`
* `newton_system_method`

## 本章小结

非线性方程组方法把标量求根的“导数”推广为 Jacobian 矩阵。向量不动点迭代形式简单，但依赖映射的局部压缩性；Newton 法通常收敛更快，但每步都需要组装并求解线性化方程。第九章后续内容将围绕“如何让 Newton 步更稳健、更便宜”展开。
