# 第八章：非线性方程求根

本章研究标量非线性方程

$$
f(x)=0.
$$

非线性方程通常没有通用解析公式。数值求根方法需要在“可靠性”和“速度”之间权衡：二分法等括区间方法稳健但收敛较慢；Newton、弦截法等开方法可能很快，但依赖初值、导数和函数局部形状。

## 学习目标

读完本章后，应能：

* 用区间扫描隔离变号根；
* 理解二分法的区间不变量和误差上界；
* 分析不动点迭代的局部收敛条件；
* 使用 Aitken 和 Steffensen 加速线性收敛；
* 推导 Newton 法、阻尼 Newton 法和重根修正；
* 比较弦截法、Müller 抛物线法和多项式全部根方法。

## 与前面章节的联系

第七章中的迭代思想、残差停止准则和收敛历史会在本章继续出现。第五章的数值微分可用于离散 Newton 法和导数近似；第三章的插值和逼近思想会出现在弦截法、Müller 法和多项式压缩中。

## 阅读顺序

1. `notebooks/01_bracketing_methods.ipynb`
2. 后续将继续补充不动点与加速、Newton 法、弦截与抛物线法、多项式全部根拓展。

## Notebook 对照表

| Notebook | 作用 | 状态 |
| --- | --- | --- |
| `01_bracketing_methods.ipynb` | 根隔离、变号区间扫描、二分法、误差上界和偶重根局限。 | 已建设 |
| `02_fixed_point_acceleration.ipynb` | 不动点迭代、Aitken 加速和 Steffensen 方法。 | 待建设 |
| `03_newton_methods.ipynb` | Newton 法、阻尼 Newton、重根修正和收敛阶实验。 | 待建设 |
| `04_secant_and_parabolic_methods.ipynb` | 弦截法和 Müller 抛物线法。 | 待建设 |
| `05_polynomial_roots_extensions.ipynb` | Bairstow 型劈因子法和逐次压缩 Newton 求全部零点。 | 待建设 |

## 可运行脚本

在仓库根目录运行：

```bash
python chapters/ch08_nonlinear_roots/scripts/nonlinear_root_methods.py
```

脚本是 Notebook 实验的紧凑版本。Notebook 中仍保留教学式推导和实现。

## 代码实现

可复用实现位于：

```text
src/py_sc/nonlinear_roots.py
```

当前已包含：

* `find_sign_change_brackets`
* `bisection_method`

## 本章小结

标量求根方法可以先按是否保持括区间分为两类。区间分割和二分法依赖连续性与变号条件，可靠性强，并能给出清楚的区间误差上界；但它们对无变号偶重根无能为力，收敛速度也只是线性。后续开方法会尝试提高速度，但会付出初值敏感、导数要求或失败保护更复杂的代价。
