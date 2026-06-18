# 第四章参考文献

本章参考资料以数值分析教材、科学计算教材和 Python 科学计算资料为主。参考文献用于支撑求积公式推导、误差分析、Romberg 外推、自适应积分、高斯型求积和 Monte Carlo 积分等内容。

## 数值分析与科学计算教材

* Richard L. Burden, J. Douglas Faires, Annette M. Burden, *Numerical Analysis*. 其中数值积分章节系统介绍 Newton-Cotes、复合公式、Romberg 和自适应积分。
* Kendall E. Atkinson, *An Introduction to Numerical Analysis*. 可参考其中插值型求积、误差项和自适应积分的分析。
* David Kincaid, Ward Cheney, *Numerical Analysis: Mathematics of Scientific Computing*. 适合补充高斯求积、误差估计和科学计算视角。
* Lloyd N. Trefethen, *Approximation Theory and Approximation Practice*. 可帮助理解插值、正交多项式、Chebyshev 思想与高精度求积之间的联系。
* Gene H. Golub, John H. Welsch, Calculation of Gauss quadrature rules, *Mathematics of Computation*, 1969. 经典论文，说明如何由 Jacobi 矩阵特征值问题构造高斯求积节点和权重。

## 概率计算与 Monte Carlo

* Nicholas J. Higham, *Accuracy and Stability of Numerical Algorithms*. 可用于理解舍入误差、稳定性和高阶公式的数值风险。
* Christian P. Robert, George Casella, *Monte Carlo Statistical Methods*. 可作为 Monte Carlo 积分、方差和随机估计的拓展资料。
* Art B. Owen, *Monte Carlo Theory, Methods and Examples*. 适合进一步学习重要性采样、方差缩减和拟 Monte Carlo 方法。

## Python 科学计算资料

* NumPy 文档中的 `numpy.trapezoid`、`numpy.polynomial.legendre.leggauss`、`numpy.polynomial.laguerre.laggauss` 和 `numpy.polynomial.hermite.hermgauss` 可作为标准库对照。
* SciPy 文档中的 `scipy.integrate.quad`、`scipy.integrate.romb`、`scipy.integrate.simpson` 和 `scipy.integrate.nquad` 可用于工程实践中的验证和接口学习。
* Matplotlib 文档用于绘制误差收敛图、自适应区间划分图和 Monte Carlo 收敛图。

## 与本仓库前后章节的联系

* 第二章“数据插值”给出 Lagrange 插值、多项式插值误差和样条插值，是 Newton-Cotes 与离散数据积分的基础。
* 第三章“函数逼近与曲线拟合”给出 Chebyshev、Legendre 和正交投影思想，是 Gauss 型求积的基础。
* 后续常微分方程、偏微分方程和谱方法章节会继续使用误差阶、外推、自适应细分和高斯节点等思想。
