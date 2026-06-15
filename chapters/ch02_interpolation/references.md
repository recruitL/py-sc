# 参考文献：数据插值

## 数值分析教材

* Richard L. Burden, J. Douglas Faires, Annette M. Burden, *Numerical Analysis*。
* Kendall Atkinson, *An Introduction to Numerical Analysis*。
* Gene H. Golub and Charles F. Van Loan, *Matrix Computations*。
* David Kincaid and Ward Cheney, *Numerical Analysis: Mathematics of Scientific Computing*。
* Alfio Quarteroni, Riccardo Sacco, and Fausto Saleri, *Numerical Mathematics*。
* Lloyd N. Trefethen, *Approximation Theory and Approximation Practice*。
* Lloyd N. Trefethen, *Spectral Methods in MATLAB*。
* Carl de Boor, *A Practical Guide to Splines*。
* M. J. D. Powell, *Approximation Theory and Methods*。
* Jean-Paul Berrut and Lloyd N. Trefethen, *Barycentric Lagrange Interpolation*。

Atkinson、Burden 和 Kincaid/Cheney 的教材适合作为本章多项式插值、误差公式和样条插值推导的基础参考。Trefethen 的书更适合理解切比雪夫节点、逼近论和后续谱方法之间的关系。de Boor 的书是学习样条理论的重要参考。

## 拉格朗日插值的理论来源

本章关于拉格朗日插值的推导采用数值分析教材中的标准讲法：先从两点直线插值出发，构造满足 \(\ell_j(x_i)=\delta_{ij}\) 的基函数，再用这些基函数拼出插值多项式。这个构造和唯一性证明可参考 Atkinson、Burden/Faires/Burden、Kincaid/Cheney 和 Quarteroni/Sacco/Saleri 的数值分析教材。

本章只简要说明拉格朗日基函数与切比雪夫微分矩阵之间的关系。相关谱方法背景可参考 Trefethen 的 *Spectral Methods in MATLAB*。其中的核心思路是：先在切比雪夫节点上构造拉格朗日插值多项式，再对插值多项式求导，从而得到微分矩阵。

Berrut 和 Trefethen 关于重心形式拉格朗日插值的文章适合作为后续扩展阅读。本轮仍保留普通拉格朗日形式，因为它更适合解释插值基函数和开关函数思想。

## Python 与科学计算资料

* NumPy 文档：数组运算、网格采样和基础数值操作。
* SciPy 文档：`scipy.interpolate` 中的标准插值接口，可用于与手写实现对照。
* Matplotlib 文档：用于绘制误差曲线、插值曲线和二维插值图像。
* Jupyter 文档：用于维护可运行、可复现实验的电子讲义。

## 本章主题线索

* 拉格朗日插值和多项式插值误差公式；
* 牛顿差商和等距节点下的差分插值；
* Runge 函数和等距节点端点振荡；
* 切比雪夫节点与全局多项式插值稳定性；
* 自然三次样条和三对角线性方程组；
* 三次 Hermite 插值、PCHIP 和保单调分段方法；
* 三次均匀 B 样条和局部支撑；
* 双线性插值和三角形单元上的二维一次插值。

## 使用说明

本章中，SciPy 应主要作为对照和验证工具。核心算法仍应保留在 `src/py_sc/interpolation.py` 中，用手写实现突出算法结构和教学清晰度。

切比雪夫微分矩阵只作为扩展提示出现。它更适合在后续“谱方法”章节中系统展开。
