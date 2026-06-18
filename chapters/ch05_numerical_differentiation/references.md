# 第五章参考文献

本章参考资料以数值分析教材、有限差分资料、样条教材和 Python 科学计算文档为主。参考文献用于支撑差分公式推导、误差阶分析、Richardson 外推、样条微分和噪声敏感性等内容。

## 数值分析与科学计算教材

* Richard L. Burden, J. Douglas Faires, Annette M. Burden, *Numerical Analysis*. 其中数值微分章节系统介绍三点公式、五点公式、误差项和 Richardson 外推。
* Kendall E. Atkinson, *An Introduction to Numerical Analysis*. 可参考有限差分公式、插值多项式推导和误差分析。
* David Kincaid, Ward Cheney, *Numerical Analysis: Mathematics of Scientific Computing*. 适合补充科学计算视角下的舍入误差、差分格式和外推思想。
* Nicholas J. Higham, *Accuracy and Stability of Numerical Algorithms*. 可用于理解相消、舍入误差和病态问题在数值微分中的影响。
* Lloyd N. Trefethen, *Finite Difference and Spectral Methods for Ordinary and Partial Differential Equations*. 可作为紧致差分、微分矩阵和后续 PDE 离散化的拓展资料。

## 样条与 B 样条

* Carl de Boor, *A Practical Guide to Splines*. 经典样条教材，适合深入理解 B 样条基函数、局部支撑性和样条导数。
* Larry L. Schumaker, *Spline Functions: Basic Theory*. 可作为三次样条、B 样条和样条空间理论的系统参考。
* Les Piegl, Wayne Tiller, *The NURBS Book*. 适合进一步学习 B 样条、NURBS、控制点和曲线导数。

## Python 科学计算资料

* NumPy 文档中的数组运算、`numpy.gradient` 和 `numpy.polynomial` 可作为离散数据微分和多项式操作的接口参考。
* SciPy 文档中的 `scipy.interpolate.CubicSpline`、`scipy.interpolate.BSpline` 和 `scipy.misc.derivative` 的历史说明可作为工程接口和版本差异参考。
* Matplotlib 文档用于绘制误差曲线、双对数收敛图、步长 U 形曲线和含噪声数据对比图。

## 与本仓库前后章节的联系

* 第二章“数据插值”给出 Lagrange 插值、牛顿差商、三次样条和 B 样条入口，是有限差分权重和样条微分的基础。
* 第四章“数值积分”中的 Richardson 外推和 Romberg 求积为本章外推微分提供直接类比。
* 后续常微分方程、偏微分方程和谱方法章节会继续使用本章的差分格式、误差阶、边界处理和微分矩阵思想。
