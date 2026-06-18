# py-sc

`py-sc` 是一个面向 Python 数值计算的课程型 / 书籍型代码库。

本仓库的目标不是只保存代码片段，而是形成一套可以长期更新的可运行电子讲义：先说明数学问题和算法动机，再给出 Python 实现，最后通过 Jupyter Notebook 中的数值实验和图像理解方法的适用范围。

## 仓库结构

```text
py-sc/
  AGENTS.md                 # 仓库维护和写作规则
  chapters/
    ch02_interpolation/     # 第二章：数据插值
      notebooks/            # 主要教学 Notebook
      notes/                # 理论笔记和补充说明
      scripts/              # 与 Notebook 对应的可运行脚本
      references.md         # 本章参考文献
    ch03_approximation/     # 第三章：函数逼近与曲线拟合
      notebooks/            # 主要教学 Notebook
      notes/                # 理论笔记和补充说明
      scripts/              # 与 Notebook 对应的可运行脚本
      references.md         # 本章参考文献
    ch04_numerical_integration/ # 第四章：数值积分
      notebooks/            # 主要教学 Notebook
      notes/                # 理论笔记和补充说明
      scripts/              # 与 Notebook 对应的可运行脚本
      references.md         # 本章参考文献
    ch05_numerical_differentiation/ # 第五章：数值微分
      notebooks/            # 主要教学 Notebook
      notes/                # 理论笔记和补充说明
      scripts/              # 与 Notebook 对应的可运行脚本
      references.md         # 本章参考文献
    ch07_iterative_linear_systems/ # 第七章：解线性方程组的迭代法
      notebooks/            # 主要教学 Notebook
      scripts/              # 与 Notebook 对应的可运行脚本
  docs/                     # 课程层面的说明和路线图
  references/               # 跨章节共享参考文献说明
  src/
    py_sc/                  # 可复用的教学实现
  tests/                    # 轻量回归测试
```

## 当前章节

| 章节 | 主题 | 状态 |
| --- | --- | --- |
| 第二章 | 数据插值 | 系统建设：插值基本形式、全局多项式插值、Runge 现象、切比雪夫节点、牛顿差商、分段线性插值、分段三次 Hermite、自然三次样条、PCHIP、三次均匀 B 样条、二维插值和切比雪夫微分矩阵入口 |
| 第三章 | 函数逼近与曲线拟合 | 理论扩充：逼近空间、误差范数、投影观点，Chebyshev/Legendre 级数，最小二乘、正则化、Padé、Fourier/FFT 与自适应逼近框架 |
| 第四章 | 数值积分 | 新增建设：求积基本原理、Newton-Cotes、复合求积、Romberg、自适应 Simpson、Gauss-Legendre、带权高斯公式、离散数据积分、多重积分和高维 Monte Carlo 框架 |
| 第五章 | 数值微分 | 新增建设：有限差分、函数型和离散数据微分、非等距权重、Richardson 外推、隐式紧致格式入口、样条微分、B 样条微分框架、二阶微分和误差实验 |
| 第七章 | 解线性方程组的迭代法 | 建设中：Jacobi、Gauss-Seidel、SOR、块迭代、最速下降、CG、PCG、二维 Poisson 五点差分、矩阵分裂、谱半径和残差停止准则 |

## 阅读顺序

建议先读章节入口，再按编号阅读 Notebook：

1. `chapters/ch02_interpolation/README.md`
2. `chapters/ch02_interpolation/notebooks/01_interpolation_overview.ipynb`
3. `chapters/ch02_interpolation/notebooks/02_polynomial_interpolation.ipynb`
4. `chapters/ch02_interpolation/notebooks/03_piecewise_and_spline.ipynb`
5. `chapters/ch02_interpolation/notebooks/04_experiments.ipynb`
6. `chapters/ch02_interpolation/notebooks/05_extensions_framework.ipynb`
7. `chapters/ch03_approximation/README.md`
8. `chapters/ch03_approximation/notebooks/01_approximation_overview.ipynb`
9. `chapters/ch03_approximation/notebooks/02_chebyshev_legendre_approximation.ipynb`
10. `chapters/ch03_approximation/notebooks/03_least_squares_fitting.ipynb`
11. `chapters/ch03_approximation/notebooks/04_pade_approximation.ipynb`
12. `chapters/ch03_approximation/notebooks/05_experiments_framework.ipynb`
13. `chapters/ch04_numerical_integration/README.md`
14. `chapters/ch04_numerical_integration/notebooks/01_integration_overview.ipynb`
15. `chapters/ch04_numerical_integration/notebooks/02_newton_cotes_and_composite.ipynb`
16. `chapters/ch04_numerical_integration/notebooks/03_romberg_and_adaptive.ipynb`
17. `chapters/ch04_numerical_integration/notebooks/04_gaussian_quadrature.ipynb`
18. `chapters/ch04_numerical_integration/notebooks/05_discrete_data_integration.ipynb`
19. `chapters/ch04_numerical_integration/notebooks/06_multiple_and_monte_carlo_framework.ipynb`
20. `chapters/ch04_numerical_integration/notebooks/07_experiments.ipynb`
21. `chapters/ch05_numerical_differentiation/README.md`
22. `chapters/ch05_numerical_differentiation/notebooks/01_differentiation_overview.ipynb`
23. `chapters/ch05_numerical_differentiation/notebooks/02_finite_difference_formulas.ipynb`
24. `chapters/ch05_numerical_differentiation/notebooks/03_discrete_data_differentiation.ipynb`
25. `chapters/ch05_numerical_differentiation/notebooks/04_spline_differentiation.ipynb`
26. `chapters/ch05_numerical_differentiation/notebooks/05_richardson_and_implicit.ipynb`
27. `chapters/ch05_numerical_differentiation/notebooks/06_second_derivatives.ipynb`
28. `chapters/ch05_numerical_differentiation/notebooks/07_experiments.ipynb`
29. `chapters/ch07_iterative_linear_systems/README.md`
30. `chapters/ch07_iterative_linear_systems/notebooks/01_stationary_iterations.ipynb`
31. `chapters/ch07_iterative_linear_systems/notebooks/02_sor_and_block_iterations.ipynb`
32. `chapters/ch07_iterative_linear_systems/notebooks/03_cg_and_pcg.ipynb`
33. `chapters/ch07_iterative_linear_systems/notebooks/04_poisson_sparse_iterations.ipynb`

运行脚本示例：

```bash
python chapters/ch02_interpolation/scripts/compare_interpolation.py
python chapters/ch03_approximation/scripts/orthogonal_approximation.py
python chapters/ch04_numerical_integration/scripts/integration_methods.py
python chapters/ch05_numerical_differentiation/scripts/differentiation_methods.py
python chapters/ch07_iterative_linear_systems/scripts/iterative_linear_methods.py
```

运行测试：

```bash
python -m pytest
```

## 环境配置

建议创建独立环境，并以可编辑模式安装本项目：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```
