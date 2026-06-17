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

运行脚本示例：

```bash
python chapters/ch02_interpolation/scripts/compare_interpolation.py
python chapters/ch03_approximation/scripts/orthogonal_approximation.py
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
