# 第七章：解线性方程组的迭代法

本章研究如何用迭代方法求解线性方程组

$$
Ax=b.
$$

与直接法相比，迭代法通常不追求有限步精确消元，而是构造一列近似解 \(x^{(0)},x^{(1)},\ldots\)，使残差

$$
r^{(k)}=b-Ax^{(k)}
$$

逐步减小。对于大规模稀疏线性系统，特别是来自微分方程离散化的系统，迭代法常比直接法更节省内存，也更容易利用矩阵结构。

## 学习目标

读完本章后，应能：

* 用矩阵分裂 \(A=M-N\) 解释平稳迭代法；
* 写出 Jacobi、Gauss-Seidel 和 SOR 的迭代公式；
* 用谱半径、对角占优和 SPD 条件判断典型收敛情形；
* 用残差历史和相对残差设置停止准则；
* 理解最速下降法、共轭梯度法和预处理共轭梯度法的基本差别；
* 构造二维 Poisson 方程五点差分系统，并比较不同迭代法。

## 与前面章节的联系

第七章会反复使用矩阵范数、残差、条件数和线性代数基础。第五章的差分思想会在二维 Poisson 方程离散中出现；后续第十二章的椭圆型 PDE 求解会继续使用本章的 Jacobi、Gauss-Seidel、SOR 和 CG 思想。

当前仓库尚未建设第六章直接法，因此本章中涉及追赶法、直接分解和稀疏直接法时，只作为后续补齐的连接点，不把它们作为本章主线。

## 阅读顺序

1. `notebooks/01_stationary_iterations.ipynb`
2. `notebooks/02_sor_and_block_iterations.ipynb`
3. 后续将继续补充 CG 与 PCG、二维 Poisson 稀疏迭代。

## Notebook 对照表

| Notebook | 作用 | 状态 |
| --- | --- | --- |
| `01_stationary_iterations.ipynb` | Jacobi 与 Gauss-Seidel、矩阵分裂、谱半径、残差停止准则和收敛/发散对比。 | 已建设 |
| `02_sor_and_block_iterations.ipynb` | SOR、松弛因子扫描、块 Jacobi、块 Gauss-Seidel 和块迭代适用条件。 | 已建设 |
| `03_cg_and_pcg.ipynb` | 最速下降、CG、PCG、条件数影响和预处理效果。 | 待建设 |
| `04_poisson_sparse_iterations.ipynb` | 二维 Poisson 五点差分稀疏系统和多种迭代法比较。 | 待建设 |

## 可运行脚本

在仓库根目录运行：

```bash
python chapters/ch07_iterative_linear_systems/scripts/iterative_linear_methods.py
```

脚本是 Notebook 实验的紧凑版本，用于快速检查核心算法和典型结果。Notebook 中仍保留教学式推导和实现，不依赖脚本替代讲义内容。

## 代码实现

可复用实现位于：

```text
src/py_sc/iterative_linear.py
```

当前已包含：

* `jacobi_iteration`
* `gauss_seidel_iteration`
* `jacobi_iteration_matrix`
* `gauss_seidel_iteration_matrix`
* `sor_iteration`
* `sor_iteration_matrix`
* `scan_sor_omega`
* `block_jacobi_iteration`
* `block_gauss_seidel_iteration`
* `spectral_radius`
* `relative_residual`
* `is_strictly_diagonally_dominant`
* `is_symmetric_positive_definite`

## 本章小结

平稳迭代法把 \(Ax=b\) 改写为 \(Mx^{(k+1)}=Nx^{(k)}+b\)。Jacobi 方法每一步只使用上一轮全部分量，便于并行但通常较慢；Gauss-Seidel 方法在同一轮中立即使用新分量，常收敛更快，但顺序依赖更强。SOR 在 Gauss-Seidel 的候选更新上加入松弛因子，可能显著减少迭代次数，但需要选择合适的 \(\omega\)。块迭代用小线性系统替代标量更新，适合有自然分组结构的问题。谱半径 \(\rho(B)<1\) 是线性定常迭代收敛的核心判据，严格对角占优和 SPD 条件则给出常用的充分条件。实际计算中应使用相对残差、最大迭代次数和残差历史共同判断算法行为。
