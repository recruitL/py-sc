# 第十二章：偏微分方程数值解法

本章研究偏微分方程的有限差分数值解法。与常微分方程只沿时间推进不同，偏微分方程同时涉及空间网格、时间网格、初始条件、边界条件和方程类型。数值格式必须同时关注一致性、稳定性和收敛性。

## 学习目标

读完本章后，应能：

* 区分双曲型、抛物型和椭圆型方程的典型数值困难；
* 为简单 PDE 建立空间-时间网格；
* 写出一维常系数对流方程的上风、Lax-Friedrichs 和 Lax-Wendroff 格式；
* 理解 CFL 条件、数值耗散和数值色散；
* 用中心差分求解一维波动方程并监控能量变化；
* 用解析解或制造解检查 PDE 离散结果。

## 与前面章节的联系

第七章的迭代法和第十章的谱观点解释了稳定性与离散算子的关系；第十一章的时间步进方法为显式 PDE 格式提供了基础。第十二章把这些思想放到空间网格上，连接对流、扩散、波动和 Poisson 方程。

## 阅读顺序

1. `notebooks/01_hyperbolic_advection_and_wave.ipynb`

## Notebook 对照表

| Notebook | 作用 | 状态 |
| --- | --- | --- |
| `01_hyperbolic_advection_and_wave.ipynb` | 一维/二维对流方程、CFL 条件、上风/Lax 系列格式和一维波动方程。 | 已建设 |

## 可运行脚本

在仓库根目录运行：

```bash
python chapters/ch12_pde_methods/scripts/pde_methods.py
```

## 代码实现

可复用实现位于：

```text
src/py_sc/pde.py
```

当前已包含：

* `periodic_grid_1d`
* `advection_cfl`
* `upwind_advection_1d`
* `lax_friedrichs_advection_1d`
* `lax_wendroff_advection_1d`
* `upwind_advection_2d`
* `wave_cfl`
* `solve_wave_1d_dirichlet`
* `wave_discrete_energy`

## 本章小结

双曲型方程的核心是信息沿特征传播。上风格式把传播方向嵌入差分模板，通常更稳健但有数值耗散；Lax-Friedrichs 增加平均项，耗散更明显；Lax-Wendroff 利用二阶 Taylor 展开降低耗散，但可能带来色散振荡。波动方程的中心差分格式需要用初始位移和初始速度构造第一时间层，并满足 CFL 条件。后续抛物型和椭圆型问题将进一步强调稳定性、隐式线性系统和稀疏矩阵结构。
