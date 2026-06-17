# 参考文献：函数逼近与曲线拟合

## 数值分析与逼近论教材

* Kendall Atkinson, *An Introduction to Numerical Analysis*。
* Richard L. Burden, J. Douglas Faires, Annette M. Burden, *Numerical Analysis*。
* David Kincaid and Ward Cheney, *Numerical Analysis: Mathematics of Scientific Computing*。
* Alfio Quarteroni, Riccardo Sacco, and Fausto Saleri, *Numerical Mathematics*。
* Lloyd N. Trefethen, *Approximation Theory and Approximation Practice*。
* Lloyd N. Trefethen, *Spectral Methods in MATLAB*。
* Elliott Ward Cheney, *Introduction to Approximation Theory*。
* M. J. D. Powell, *Approximation Theory and Methods*。
* John P. Boyd, *Chebyshev and Fourier Spectral Methods*。
* Gene H. Golub and Charles F. Van Loan, *Matrix Computations*。

Atkinson、Burden/Faires/Burden 和 Kincaid/Cheney 适合作为最小二乘、正交多项式和数值线性代数基础参考。Trefethen 的逼近论教材非常适合理解 Chebyshev 多项式、最佳逼近、谱方法和函数逼近的整体结构。Boyd 的书更偏谱方法和 Fourier/Chebyshev 计算，适合作为后续扩展材料。

## Chebyshev 与 Legendre 逼近

Chebyshev 多项式、Chebyshev 节点和 Chebyshev 级数可参考 Trefethen 的 *Approximation Theory and Approximation Practice* 与 *Spectral Methods in MATLAB*。这些资料强调“函数逼近”和“谱方法”之间的联系，适合理解为什么 Chebyshev 方法在光滑函数上收敛很快。

Legendre 多项式和正交投影可参考 Atkinson、Quarteroni/Sacco/Saleri 和 Kincaid/Cheney 的数值分析教材。本章采用投影观点：

$$
\langle f-p_n,q\rangle=0,\qquad q\in \mathcal P_n.
$$

这也是后续 Galerkin 方法和谱方法的重要背景。

本轮理论扩充中，Chebyshev 部分重点参考三角定义 \(T_n(\cos\theta)=\cos(n\theta)\)、递推关系、带权正交性和 Chebyshev 系数计算思想；Legendre 部分重点参考普通 \(L^2\) 内积下的正交投影、系数公式和 Gauss-Legendre 求积近似。

## 最佳一致逼近

最佳一致逼近、多项式极小极大思想和 Chebyshev 交错定理可参考 Cheney 的逼近论教材和 Powell 的 *Approximation Theory and Methods*。本轮只保留概念入口，后续如果实现 Remez 算法，可以继续补充这些资料。

交错定理和 Remez 算法在本章中暂时作为理论入口出现，主要用于说明一致范数下的“最好”与平方范数投影不同。后续若加入 Remez 实现，应补充误差交错点的选择、线性系统构造和迭代更新规则。

## Fourier、FFT 与 Gibbs 现象

Fourier 级数和三角多项式逼近可参考 Trefethen 和 Boyd。FFT 的算法细节可参考经典科学计算教材，也可参考 NumPy 的 `numpy.fft` 文档。本章第一轮把 FFT 放在“三角多项式逼近的计算工具”这一位置，而不是孤立的算法章节。

Gibbs 现象可参考 Fourier 分析教材和谱方法资料。后续专题实验应展示阶跃函数或分段光滑周期函数在不连续点附近的过冲现象，并解释为什么增加项数不会消除过冲高度，只会压缩振荡区域。

## 最小二乘与曲线拟合

离散最小二乘、法方程、QR 分解、SVD 和矩阵病态性可参考 Golub/Van Loan 的 *Matrix Computations*。本章教学实现采用 `np.linalg.lstsq`，避免显式求解病态法方程。

多项式拟合的过拟合现象和正则化思想可参考数值线性代数、统计学习和科学计算教材。本章只给出简单入口，后续可以加入 Ridge 正则化和交叉验证示例。

本轮补充了最小二乘的几何解释：最小二乘解是把观测向量投影到设计矩阵列空间上，残差与列空间正交。法方程适合理论推导，但实际计算应优先使用 QR、SVD 或 `np.linalg.lstsq`。这一处理方式可参考 Golub/Van Loan，也与 NumPy 线性代数接口的推荐用法一致。

## Padé 逼近

Padé 有理逼近可参考 Atkinson 和 Baker/Graves-Morris 的有理逼近资料：

* George A. Baker Jr. and Peter Graves-Morris, *Padé Approximants*。

本章第一轮只讨论由 Taylor 系数构造 Padé 逼近的线性方程，并通过 \(e^x\) 和 \(\log(1+x)\) 等例子展示 Taylor 多项式与有理函数逼近的差异。

本轮理论扩充中，Padé 部分补充了从

$$
Q_n(x)f(x)-P_m(x)=O(x^{m+n+1})
$$

到分母系数线性方程的逐项推导，并强调虚假极点检查。后续可继续加入分母零点可视化和不同 \([m/n]\) 阶数组合的误差比较。

## 自适应逼近与正则化扩展

自适应逼近可参考数值分析教材中关于自适应求积、分片多项式逼近和误差估计的章节。本章当前只使用中点误差估计展示“误差驱动局部加密”的基本思想。后续可以把这一思想推广到自适应三次样条、局部 Chebyshev 逼近和多层网格策略。

正则化拟合可参考数值线性代数、反问题和统计学习资料。当前只引入 Ridge/Tikhonov 形式，用于说明在病态和噪声数据中，单纯最小化训练残差并不总是可靠。

## Python 与科学计算资料

* NumPy 文档：`numpy.polynomial.chebyshev`、`numpy.polynomial.legendre`、`numpy.linalg.lstsq`、`numpy.fft`。
* Matplotlib 文档：误差曲线、拟合曲线和实验图像。
* Jupyter 文档：维护可运行、可复现实验讲义。

## 本章使用说明

SciPy 可作为后续对照工具，但本章第一轮核心实现只依赖 NumPy 和 Matplotlib。这样可以更清楚地展示正交基、Vandermonde 矩阵、最小二乘和 Padé 线性方程的算法结构。
