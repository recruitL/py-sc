# 第六章：解线性方程组的直接方法

线性方程组

$$
A\boldsymbol{x}=\boldsymbol{b}
$$

几乎出现在所有数值计算主题中：样条插值需要解三对角系统，最小二乘拟合可以通过 QR 分解求解，隐式差分格式会产生线性系统，常微分方程、偏微分方程和特征值问题也都依赖数值线性代数。本章讨论“直接方法”：在有限步消元或矩阵分解后求解线性方程组。

本章主线是：

```text
线性方程组与三角方程组
  -> 高斯消元
  -> LU 三角分解
  -> 对称正定矩阵的平方根分解
  -> 三对角方程组的追赶法
  -> QR 分解
  -> 方法比较与数值实验
  -> 小结与参考文献
```

## 本章导言

直接方法在精确算术下通常可以有限步得到精确解，但在浮点运算中会受到舍入误差、病态条件数和主元选择的影响。因此本章不只比较求出的解，还会同时报告：

* 相对残差

  $$
  \frac{\|\boldsymbol{b}-A\widehat{\boldsymbol{x}}\|_2}{\|\boldsymbol{b}\|_2};
  $$

* 相对前向误差

  $$
  \frac{\|\widehat{\boldsymbol{x}}-\boldsymbol{x}\|_2}{\|\boldsymbol{x}\|_2};
  $$

* 条件数和算法稳定性的区别。

直接方法与迭代方法的区别在于：直接方法通过消元、三角分解或正交分解一次性构造求解过程；迭代方法从初值出发不断改进近似解，通常需要收敛条件和终止准则。第七章会继续讨论 Jacobi、Gauss-Seidel 和 Krylov 子空间方法等迭代法。

本章首先介绍两个基础步骤：

$$
L\boldsymbol{y}=\boldsymbol{b},
\qquad
U\boldsymbol{x}=\boldsymbol{y},
$$

即下三角方程组的前代和上三角方程组的回代。高斯消元、LU、Cholesky、LDL^T、Thomas 和 QR 求解最终都会回到这些三角求解过程。

## 主要问题

* 高斯消元和 LU 分解是什么关系？
* 为什么需要部分选主元？主元为零或很小时会发生什么？
* 多个右端项时，为什么先分解矩阵再重复前代/回代更合适？
* 对称正定矩阵为什么适合 Cholesky 或 \(LDL^T\)？
* 三对角结构为什么能把复杂度从 \(O(n^3)\) 降到 \(O(n)\)？
* Gram-Schmidt、Householder 和 Givens 三类 QR 方法各自适合什么场景？
* 小残差为什么不一定意味着小前向误差？
* 如何根据矩阵结构选择直接求解方法？

## 主要算法

本轮已经建立并可运行：

* 前代 `forward_substitution`；
* 回代 `backward_substitution`；
* 不选主元高斯消元；
* 部分选主元高斯消元；
* Doolittle LU 分解；
* 部分选主元 PLU 分解；
* Cholesky \(LL^T\) 分解；
* \(LDL^T\) 分解；
* 三对角追赶法 Thomas algorithm；
* 经典 Gram-Schmidt 和修正 Gram-Schmidt；
* Householder QR；
* Givens QR 的基础实现；
* 残差、前向误差和正交性误差工具。

保留后续拓展入口：

* 完全选主元高斯消元；
* 三对角 Crout 分解的独立实现；
* Givens QR 的稀疏矩阵高性能实现；
* 稀疏矩阵专用存储格式和直接法；
* 对称不定矩阵的带主元 \(LDL^T\) 分解。

## 阅读顺序

1. `notebooks/01_linear_systems_overview.ipynb`
2. `notebooks/02_gaussian_elimination.ipynb`
3. `notebooks/03_lu_factorization.ipynb`
4. `notebooks/04_spd_factorizations.ipynb`
5. `notebooks/05_tridiagonal_systems.ipynb`
6. `notebooks/06_qr_factorization.ipynb`
7. `notebooks/07_experiments.ipynb`
8. `notes/theory.md`
9. `references.md`

## Notebook 对照表

| Notebook | 作用 |
| --- | --- |
| `01_linear_systems_overview.ipynb` | 引入线性方程组、直接方法、矩阵结构、前代、回代、残差和前向误差。 |
| `02_gaussian_elimination.ipynb` | 展示高斯消元矩阵过程、不选主元与部分选主元实现、主元失败例子和误差比较。 |
| `03_lu_factorization.ipynb` | 从 \(A=LU\) 推导 Doolittle 递推，说明 \(PA=LU\)、置换向量和多个右端项复用。 |
| `04_spd_factorizations.ipynb` | 讨论对称正定矩阵、Cholesky \(LL^T\)、\(LDL^T\)、求解过程和失败情形。 |
| `05_tridiagonal_systems.ipynb` | 从三对角消元推导追赶法，并用样条系统和一维边值问题展示 \(O(n)\) 复杂度。 |
| `06_qr_factorization.ipynb` | 比较经典/修正 Gram-Schmidt、Householder 和 Givens QR，报告重构误差和正交性误差。 |
| `07_experiments.ipynb` | 汇总主元、LU 复用、SPD 分解、三对角效率、QR 正交性和病态矩阵实验。 |

## 可运行脚本

在仓库根目录运行：

```bash
python chapters/ch06_direct_linear_systems/scripts/direct_methods.py
```

脚本是 Notebook 实验的紧凑版本，用于快速检查核心算法和典型数值结果。Notebook 中仍保留教学式推导和实现，不依赖脚本替代讲义内容。

## 代码实现

可复用实现位于：

```text
src/py_sc/direct_linear.py
```

主要函数包括：

* `forward_substitution`
* `backward_substitution`
* `gaussian_elimination`
* `gaussian_elimination_partial_pivoting`
* `lu_doolittle`
* `plu_factorization`
* `cholesky_factorization`
* `ldlt_factorization`
* `thomas_algorithm`
* `classical_gram_schmidt`
* `modified_gram_schmidt`
* `householder_qr`
* `givens_qr`

Notebook 中会先给出简洁、清晰的教学式实现，再调用这些可复用函数做对照和复用。

## 当前范围

本轮已经完整完成：

* 第六章统一入口；
* 前代和回代；
* 高斯消元与部分选主元；
* Doolittle LU 和 PLU 分解；
* Cholesky \(LL^T\) 和 \(LDL^T\)；
* Thomas 追赶法；
* 经典和修正 Gram-Schmidt；
* Householder QR 基本实现；
* Givens QR 基础示例；
* 统一实验入口、参考文献和回归测试。

暂时作为框架或拓展，后续继续完善：

* 完全选主元高斯消元；
* 三对角 Crout 分解的独立实现；
* Givens QR 的稀疏高性能实现；
* 稀疏矩阵存储、填充减少和大型直接求解器；
* 对称不定矩阵的稳定 \(LDL^T\) 分解。

## 和前后章节的关系

第二章自然三次样条会产生三对角线性方程组，第五章隐式紧致差分也会产生周期或带状线性系统。本章的 Thomas 算法和三角分解给出这些结构化系统的直接求解基础。

第三章最小二乘拟合可以通过 QR 分解稳定求解，避免显式形成病态的法方程。后续特征值问题也会反复使用 QR 分解和正交变换。

第七章迭代法会从另一条路线求解线性系统。本章的直接法更适合中小规模稠密矩阵、结构明确的三对角矩阵和需要高可靠性的核心子问题；迭代法更适合大规模稀疏系统。
