# 第十一章：常微分方程初值问题

本章研究常微分方程初值问题

$$
y'(t)=f(t,y(t)),\qquad y(t_0)=y_0.
$$

与前面章节的一次性代数问题不同，初值问题通过时间步进逐点推进数值解。局部截断误差、全局误差、稳定性和步长选择是本章的核心主题。

## 学习目标

读完本章后，应能：

* 写出显式 Euler 方法的几何意义和误差来源；
* 区分 Heun 法、中点法和经典四阶 Runge-Kutta 法的采样方式；
* 用统一的固定步长求解器比较不同时间步进方法；
* 通过精确解误差估计观察全局收敛阶；
* 用嵌入式方法估计局部误差并自动调整步长；
* 为后续自适应步长、多步法和刚性问题建立基础。

## 与前面章节的联系

数值积分章节提供了“用加权函数值近似积分”的观点；ODE 初值问题可以看成对

$$
y(t_{n+1})=y(t_n)+\int_{t_n}^{t_{n+1}} f(t,y(t))\,dt
$$

的逐步近似。第八、九章的非线性思想会在隐式方法中再次出现，第七章的线性系统求解会服务于刚性问题和隐式步进。

## 阅读顺序

1. `notebooks/01_euler_and_runge_kutta.ipynb`
2. `notebooks/02_adaptive_step_control.ipynb`

## Notebook 对照表

| Notebook | 作用 | 状态 |
| --- | --- | --- |
| `01_euler_and_runge_kutta.ipynb` | Euler、Heun、中点法、RK4、固定步长求解和收敛阶估计。 | 已建设 |
| `02_adaptive_step_control.ipynb` | Heun-Euler 嵌入式误差估计、自适应步长接受/拒绝和容差控制。 | 已建设 |

## 可运行脚本

在仓库根目录运行：

```bash
python chapters/ch11_ode_initial_value/scripts/ode_ivp_methods.py
```

## 代码实现

可复用实现位于：

```text
src/py_sc/ode_ivp.py
```

当前已包含：

* `euler_step`
* `heun_step`
* `midpoint_step`
* `rk4_step`
* `heun_euler_embedded_step`
* `solve_ivp_fixed_step`
* `solve_ivp_adaptive_heun`
* `global_error`
* `estimate_convergence_order`

## 本章小结

Euler 方法只使用区间左端斜率，结构简单但误差较大。Heun 法和中点法通过额外采样达到二阶精度，经典 RK4 用四个阶段在成本和精度之间取得很好的平衡。固定步长实验可以清楚展示全局误差随步长缩小而下降的速度；自适应 Heun-Euler 方法进一步把低阶和高阶估计之差转化为局部误差指标，根据容差自动接受、拒绝和放大/缩小步长，为后续讨论稳定性限制和刚性问题提供基准。
