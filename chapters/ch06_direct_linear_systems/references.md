# 第六章参考文献

本章参考资料以数值分析、数值线性代数和矩阵计算教材为主。参考文献用于支撑高斯消元、主元选择、LU/PLU、Cholesky、\(LDL^T\)、追赶法、QR 分解、误差指标和稳定性分析等内容。

## 数值分析与数值线性代数教材

* Gene H. Golub, Charles F. Van Loan, *Matrix Computations*. 经典矩阵计算教材，可参考 LU、Cholesky、QR、Householder、Givens 和稳定性分析。
* Lloyd N. Trefethen, David Bau III, *Numerical Linear Algebra*. 适合理解正交变换、QR 分解、条件数和稳定性。
* James W. Demmel, *Applied Numerical Linear Algebra*. 可参考主元选择、误差分析、结构化线性系统和高性能线性代数背景。
* Nicholas J. Higham, *Accuracy and Stability of Numerical Algorithms*. 可用于深入理解舍入误差、后向稳定性、病态矩阵和残差解释。
* Richard L. Burden, J. Douglas Faires, Annette M. Burden, *Numerical Analysis*. 其中线性方程组章节系统介绍高斯消元、LU、Cholesky 和三对角系统。
* Kendall E. Atkinson, *An Introduction to Numerical Analysis*. 可参考直接法、误差、条件数和基础数值分析视角。

## 软件和标准库资料

* LAPACK Users' Guide. LAPACK 是 dense numerical linear algebra 的核心库，可作为理解实际工程接口、主元选择和分解例程命名的资料。
* NumPy 文档中的 `numpy.linalg.solve`、`numpy.linalg.cholesky`、`numpy.linalg.qr` 和 `numpy.linalg.cond` 可用于 Notebook 中的标准库对照。
* SciPy 文档中的 `scipy.linalg.lu`、`scipy.linalg.solve_triangular`、`scipy.linalg.cho_factor`、`scipy.linalg.solve_banded` 和稀疏线性代数接口可作为工程实践拓展。

## 与本仓库前后章节的联系

* 第二章自然三次样条会产生三对角线性系统，本章的 Thomas 追赶法给出对应直接求解器。
* 第三章最小二乘拟合可以通过 QR 分解求解，本章提供 Gram-Schmidt、Householder 和 Givens 的基础。
* 第五章隐式紧致差分会产生线性方程组，本章的三角分解和结构化求解是后续差分方法的基础。
* 第七章迭代法会与本章直接法形成对照：直接法强调分解和有限步求解，迭代法强调收敛性、停止准则和大规模稀疏系统。
