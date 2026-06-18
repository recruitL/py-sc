# ExecPlan：第 7—12 章连续建设

状态：in_progress
最后更新时间：2026-06-19T05:39:08+08:00
当前分支：codex/chapters-07-12
基准 commit：83c69e160f81e0d6d16ecb866a8b68928eb88bd8
最后安全 commit：73e93a1
当前章节：第8章
当前小节：章节级自检
当前原子任务：第8章自检通过，准备最终提交
下一项具体动作：显式暂存第8章最终状态、章节级自检日志和 Notebook metadata 清理，创建 `Add chapter 08 nonlinear root-finding methods`。
阻塞问题：无

## 总体进度

| 章节 | 状态 | 当前里程碑 | 自检状态 | 最后 commit |
|---|---|---|---|---|
| 第7章 | done | 章节自检完成 | 通过 | a3d823a |
| 第8章 | verifying | 章节级自检 | 通过 | 73e93a1 |
| 第9章 | pending | - | 未开始 | - |
| 第10章 | pending | - | 未开始 | - |
| 第11章 | pending | - | 未开始 | - |
| 第12章 | pending | - | 未开始 | - |

## 当前断点

### 已完成

* 读取用户任务附件，确认第 7—12 章必须按顺序建设和自检。
* 读取 `AGENTS.md`、根 `README.md`、`pyproject.toml`、`.gitignore`、现有章节目录、`src/py_sc` 和 `tests` 概览。
* 确认任务开始时工作树干净，起点 commit 为 `83c69e160f81e0d6d16ecb866a8b68928eb88bd8`。
* 创建本地分支 `codex/chapters-07-12`。
* 建立 `.agent` 持久化计划、日志、命令日志脚本，并创建初始化 checkpoint `acef9b0`。
* 完成第7章 README 初稿、7.1 Notebook、章节脚本、`src/py_sc/iterative_linear.py` 中的 Jacobi/Gauss-Seidel 基础实现、`tests/test_iterative_linear.py` 中的 7.1 测试。
* 创建 7.1 checkpoint commit `adb5267`。
* 完成 SOR、松弛因子扫描、块 Jacobi、块 Gauss-Seidel 公共实现、Notebook、脚本更新和测试扩展。
* 创建 7.2 checkpoint commit `7a3cd91`。
* 完成最速下降、CG、Jacobi 预处理、PCG 公共实现、Notebook、脚本更新和测试扩展。
* 创建 7.3 checkpoint commit `fb1c9db`。
* 完成二维 Poisson 五点差分矩阵、矩阵-向量乘法、右端采样、解向量还原、Notebook、脚本更新和测试扩展。
* 第7章四个 Notebook 均已执行通过，且无提交输出。
* 第7章相关测试 14 passed，全仓库测试 57 passed。
* 创建第7章最终提交 `a3d823a`。
* 完成第8章 README 初稿、8.1 Notebook、章节脚本、`src/py_sc/nonlinear_roots.py` 中的区间扫描和二分法、`tests/test_nonlinear_roots.py` 中的 8.1 测试。
* 创建第8章 8.1 checkpoint commit `836d450`。
* 完成 8.2 Notebook、脚本更新、`fixed_point_iteration`、`aitken_delta_squared`、`steffensen_method` 和对应测试。
* 创建第8章 8.2 checkpoint commit `d82400c`。
* 完成 8.3 Notebook、脚本更新、`newton_method`、`damped_newton_method`、`modified_newton_method` 和对应测试。
* 创建第8章 8.3 checkpoint commit `845c5df`。
* 完成 8.4 Notebook、脚本更新、`secant_method`、`muller_method` 和对应测试。
* 创建第8章 8.4 checkpoint commit `a5d764a`。
* 完成 8.5/8.6 Notebook、脚本更新、Horner/综合除法、Bairstow 型二次因子迭代、Newton 逐次压缩和对应测试。
* 创建第8章 8.5/8.6 checkpoint commit `73e93a1`。
* 第8章章节级自检通过：脚本、20 个 ch08 测试、五个 Notebook、Notebook 结构、全仓库 pytest、diff 空白检查均通过。

### 正在处理

* 第8章最终提交。

### 已修改但尚未验证

* 无第8章未验证修改。

### 已通过的检查

* `git status --short`：任务开始时无未提交修改。
* `git branch --show-current`：初始分支 `main`，已切换到 `codex/chapters-07-12`。
* `git log -5 --oneline`：最近提交包含第五章 `83c69e1`。
* `git diff --check`：初始化文件检查通过。
* `python -m py_compile src/py_sc/iterative_linear.py chapters/ch07_iterative_linear_systems/scripts/iterative_linear_methods.py tests/test_iterative_linear.py`：通过。
* `PYTHONPATH=src python -c "from py_sc import jacobi_iteration, gauss_seidel_iteration, spectral_radius"`：通过。
* `python chapters/ch07_iterative_linear_systems/scripts/iterative_linear_methods.py`：通过。
* `python -m pytest tests/test_iterative_linear.py`：4 passed。
* `nbclient` 执行 `chapters/ch07_iterative_linear_systems/notebooks/01_stationary_iterations.ipynb`：通过。
* `git diff --check`：通过。
* Notebook 结构检查：`01_stationary_iterations.ipynb` 无缺失 cell id，无提交输出。
* `PYTHONPATH=src python -c "from py_sc import sor_iteration, block_jacobi_iteration, block_gauss_seidel_iteration"`：通过。
* `python chapters/ch07_iterative_linear_systems/scripts/iterative_linear_methods.py`：通过。
* `python -m pytest tests/test_iterative_linear.py`：9 passed。
* `nbclient` 执行 `chapters/ch07_iterative_linear_systems/notebooks/02_sor_and_block_iterations.ipynb`：通过。
* `git diff --check`：通过。
* Notebook 结构检查：第7章两个 Notebook 均无缺失 cell id，无提交输出。
* `PYTHONPATH=src python -c "from py_sc import steepest_descent, conjugate_gradient, preconditioned_conjugate_gradient"`：通过。
* `python chapters/ch07_iterative_linear_systems/scripts/iterative_linear_methods.py`：通过。
* `python -m pytest tests/test_iterative_linear.py`：11 passed。
* `nbclient` 执行 `chapters/ch07_iterative_linear_systems/notebooks/03_cg_and_pcg.ipynb`：通过。
* `git diff --check`：通过。
* Notebook 结构检查：第7章三个 Notebook 均无缺失 cell id，无提交输出。
* `PYTHONPATH=src python -c "from py_sc import poisson_2d_dirichlet_matrix, poisson_2d_matvec, poisson_2d_rhs"`：通过。
* `python chapters/ch07_iterative_linear_systems/scripts/iterative_linear_methods.py`：通过。
* `python -m pytest tests/test_iterative_linear.py`：首次因 Poisson matvec 浮点零值容差过严失败；修复 `atol=1e-12` 后 14 passed。
* `nbclient` 执行 `chapters/ch07_iterative_linear_systems/notebooks/04_poisson_sparse_iterations.ipynb`：通过。
* `python -m pytest`：首次因同一容差问题失败；修复后 57 passed。
* `git diff --check`：通过。
* Notebook 结构检查：第7章四个 Notebook 均无缺失 cell id，无提交输出。
* `PYTHONPATH=src python -c "from py_sc import bisection_method, find_sign_change_brackets"`：通过。
* `python chapters/ch08_nonlinear_roots/scripts/nonlinear_root_methods.py`：通过。
* `python -m pytest tests/test_nonlinear_roots.py`：4 passed。
* `nbclient` 执行 `chapters/ch08_nonlinear_roots/notebooks/01_bracketing_methods.ipynb`：通过。
* `git diff --check`：通过。
* Notebook 结构检查：`01_bracketing_methods.ipynb` 无缺失 cell id，无提交输出。
* `PYTHONPATH=src python -c "from py_sc import fixed_point_iteration, aitken_delta_squared, steffensen_method"`：通过。
* `python chapters/ch08_nonlinear_roots/scripts/nonlinear_root_methods.py`：通过；偶重根示例修正为不正好采到根的 19 个子区间。
* `python -m pytest tests/test_nonlinear_roots.py`：8 passed。
* `nbclient` 执行 `chapters/ch08_nonlinear_roots/notebooks/02_fixed_point_acceleration.ipynb`：首次因教学版 Steffensen 到达根后继续计算导致 Aitken 分母退化失败；增加残差预检查后重跑通过。
* `python -m py_compile src/py_sc/nonlinear_roots.py chapters/ch08_nonlinear_roots/scripts/nonlinear_root_methods.py tests/test_nonlinear_roots.py`：通过。
* Notebook 结构检查：第8章前两个 Notebook 均无缺失 cell id，无提交输出。
* `git diff --check`：通过。
* `PYTHONPATH=src python -c "from py_sc import newton_method, damped_newton_method, modified_newton_method"`：通过。
* `python chapters/ch08_nonlinear_roots/scripts/nonlinear_root_methods.py`：通过。
* `python -m pytest tests/test_nonlinear_roots.py`：12 passed。
* `python -m py_compile src/py_sc/nonlinear_roots.py chapters/ch08_nonlinear_roots/scripts/nonlinear_root_methods.py tests/test_nonlinear_roots.py`：通过。
* `nbclient` 执行 `chapters/ch08_nonlinear_roots/notebooks/03_newton_methods.ipynb`：通过。
* Notebook 结构检查：第8章前三个 Notebook 均无缺失 cell id，无提交输出。
* `git diff --check`：通过。
* `PYTHONPATH=src python -c "from py_sc import secant_method, muller_method"`：通过。
* `python chapters/ch08_nonlinear_roots/scripts/nonlinear_root_methods.py`：通过。
* `python -m pytest tests/test_nonlinear_roots.py`：16 passed。
* `python -m py_compile src/py_sc/nonlinear_roots.py chapters/ch08_nonlinear_roots/scripts/nonlinear_root_methods.py tests/test_nonlinear_roots.py`：通过。
* `nbclient` 执行 `chapters/ch08_nonlinear_roots/notebooks/04_secant_and_parabolic_methods.ipynb`：通过。
* Notebook 结构检查：第8章前四个 Notebook 均无缺失 cell id，无提交输出。
* `git diff --check`：通过。
* `PYTHONPATH=src python -c "from py_sc import bairstow_quadratic_factor, newton_polynomial_roots, synthetic_division"`：通过。
* `python chapters/ch08_nonlinear_roots/scripts/nonlinear_root_methods.py`：通过。
* `python -m pytest tests/test_nonlinear_roots.py`：20 passed。
* `python -m py_compile src/py_sc/nonlinear_roots.py chapters/ch08_nonlinear_roots/scripts/nonlinear_root_methods.py tests/test_nonlinear_roots.py`：通过。
* `nbclient` 执行 `chapters/ch08_nonlinear_roots/notebooks/05_polynomial_roots_extensions.ipynb`：通过。
* Notebook 结构检查：第8章五个 Notebook 均无缺失 cell id，无提交输出。
* `git diff --check`：通过。
* 第8章章节级 `python chapters/ch08_nonlinear_roots/scripts/nonlinear_root_methods.py`：通过。
* 第8章章节级 `python -m pytest tests/test_nonlinear_roots.py`：20 passed。
* 第8章章节级 `python -m py_compile src/py_sc/nonlinear_roots.py chapters/ch08_nonlinear_roots/scripts/nonlinear_root_methods.py tests/test_nonlinear_roots.py`：通过。
* 第8章章节级 `python -m pytest`：77 passed；其中包含外部第6章工作树中的 `tests/test_direct_linear.py`，仅作为环境状态验证，不纳入本任务提交。
* 第8章五个 Notebook 全量执行并清空输出：通过。
* Notebook 结构检查：第8章五个 Notebook 均无缺失 cell id、无输出、无执行 metadata。
* `git diff --check`：通过。
* `git status --short` 和 `git diff --stat` 已记录；显示外部第6章工作树修改仍未提交，本任务提交继续过滤。

### 失败或未执行的检查

* 全仓库测试尚未运行，按第8章章节自检和最终检查阶段运行。

### 已知问题

* 仓库当前只有第 2—5 章；用户要求直接按顺序建设第 7—12 章。本任务不创建第 6 章，只在必要处说明第 6 章直接法连接为前置空缺。
* 发现外部第6章任务产生的未提交文件和修改：`.agent/execplans/chapter-06-direct-methods.md`、`src/py_sc/direct_linear.py`、`tests/test_direct_linear.py`，以及 `src/py_sc/__init__.py` 中 direct-linear 导出、`.agent/RUN_LOG.md` 中 CH06 日志。第7章 checkpoint 必须排除这些外部内容。
* `.agent/run_logged.sh` 原先使用秒级时间戳，平行命令日志可能同名覆盖；已改为在日志文件名中加入进程号。

### 下一项具体动作

1. 暂存第8章最终状态、章节级自检日志和 Notebook metadata 清理，排除第6章外部未提交文件、`docs/README.md` 和 direct-linear hunks。
2. 创建 `Add chapter 08 nonlinear root-finding methods`。
3. 记录 commit hash。
4. 开始第9章“非线性方程组解法”。

### 恢复时应首先执行的命令

```bash
git status --short
git log -10 --oneline
sed -n '1,220p' .agent/execplans/chapters-07-12.md
tail -80 .agent/RUN_LOG.md
```

## 文件记录

### 已新增文件

* `.agent/PLANS.md`
* `.agent/execplans/chapters-07-12.md`
* `.agent/RUN_LOG.md`
* `.agent/run_logged.sh`
* `.agent/logs/command-2026-06-19T04-37-27-08-00.log`
* `.agent/logs/command-2026-06-19T04-37-32-08-00.log`
* `.agent/logs/command-2026-06-19T04-37-41-08-00.log`
* `.agent/logs/command-2026-06-19T04-38-32-08-00-14773.log`
* `.agent/logs/command-2026-06-19T04-38-32-08-00-14781.log`
* `.agent/logs/command-2026-06-19T04-38-32-08-00-14789.log`
* `.agent/logs/command-2026-06-19T04-38-32-08-00-14797.log`
* `.agent/logs/command-2026-06-19T04-38-34-08-00-14762.log`
* `.agent/logs/command-2026-06-19T05-17-13-08-00-33801.log`
* `.agent/logs/command-2026-06-19T05-17-13-08-00-33803.log`
* `.agent/logs/command-2026-06-19T05-17-13-08-00-33808.log`
* `.agent/logs/command-2026-06-19T05-17-22-08-00-34359.log`
* `.agent/logs/command-2026-06-19T05-17-42-08-00-34820.log`
* `.agent/logs/command-2026-06-19T05-17-52-08-00-34868.log`
* `.agent/logs/command-2026-06-19T05-17-52-08-00-34869.log`
* `.agent/logs/command-2026-06-19T05-17-52-08-00-34875.log`
* `.agent/logs/command-2026-06-19T05-18-16-08-00-36526.log`
* `.agent/logs/command-2026-06-19T05-18-16-08-00-36527.log`
* `.agent/logs/command-2026-06-19T05-18-21-08-00-36905.log`
* `.agent/logs/command-2026-06-19T05-23-42-08-00-41197.log`
* `.agent/logs/command-2026-06-19T05-23-42-08-00-41198.log`
* `.agent/logs/command-2026-06-19T05-23-42-08-00-41201.log`
* `.agent/logs/command-2026-06-19T05-23-42-08-00-41211.log`
* `.agent/logs/command-2026-06-19T05-23-48-08-00-41676.log`
* `.agent/logs/command-2026-06-19T05-23-56-08-00-41985.log`
* `.agent/logs/command-2026-06-19T05-23-56-08-00-41986.log`
* `.agent/logs/command-2026-06-19T05-28-12-08-00-45679.log`
* `.agent/logs/command-2026-06-19T05-28-12-08-00-45680.log`
* `.agent/logs/command-2026-06-19T05-28-12-08-00-45681.log`
* `.agent/logs/command-2026-06-19T05-28-12-08-00-45692.log`
* `.agent/logs/command-2026-06-19T05-28-17-08-00-46155.log`
* `.agent/logs/command-2026-06-19T05-28-26-08-00-46463.log`
* `.agent/logs/command-2026-06-19T05-28-26-08-00-46465.log`
* `.agent/logs/command-2026-06-19T05-33-56-08-00-50044.log`
* `.agent/logs/command-2026-06-19T05-33-56-08-00-50054.log`
* `.agent/logs/command-2026-06-19T05-33-56-08-00-50063.log`
* `.agent/logs/command-2026-06-19T05-33-56-08-00-50083.log`
* `.agent/logs/command-2026-06-19T05-34-03-08-00-50678.log`
* `.agent/logs/command-2026-06-19T05-34-14-08-00-50826.log`
* `.agent/logs/command-2026-06-19T05-34-14-08-00-50828.log`
* `.agent/logs/command-2026-06-19T05-36-48-08-00-53440.log`
* `.agent/logs/command-2026-06-19T05-36-48-08-00-53458.log`
* `.agent/logs/command-2026-06-19T05-36-48-08-00-53461.log`
* `.agent/logs/command-2026-06-19T05-36-48-08-00-53473.log`
* `.agent/logs/command-2026-06-19T05-36-57-08-00-54136.log`
* `.agent/logs/command-2026-06-19T05-37-43-08-00-54291.log`
* `.agent/logs/command-2026-06-19T05-37-44-08-00-54309.log`
* `.agent/logs/command-2026-06-19T05-38-18-08-00-55426.log`
* `.agent/logs/command-2026-06-19T05-38-18-08-00-55427.log`
* `.agent/logs/command-2026-06-19T05-39-01-08-00-57299.log`
* `.agent/logs/command-2026-06-19T05-39-01-08-00-57301.log`
* `src/py_sc/iterative_linear.py`
* `tests/test_iterative_linear.py`
* `chapters/ch07_iterative_linear_systems/README.md`
* `chapters/ch07_iterative_linear_systems/notebooks/01_stationary_iterations.ipynb`
* `chapters/ch07_iterative_linear_systems/notebooks/02_sor_and_block_iterations.ipynb`
* `chapters/ch07_iterative_linear_systems/notebooks/03_cg_and_pcg.ipynb`
* `chapters/ch07_iterative_linear_systems/notebooks/04_poisson_sparse_iterations.ipynb`
* `src/py_sc/nonlinear_roots.py`
* `tests/test_nonlinear_roots.py`
* `chapters/ch08_nonlinear_roots/README.md`
* `chapters/ch08_nonlinear_roots/notebooks/01_bracketing_methods.ipynb`
* `chapters/ch08_nonlinear_roots/notebooks/02_fixed_point_acceleration.ipynb`
* `chapters/ch08_nonlinear_roots/notebooks/03_newton_methods.ipynb`
* `chapters/ch08_nonlinear_roots/notebooks/04_secant_and_parabolic_methods.ipynb`
* `chapters/ch08_nonlinear_roots/notebooks/05_polynomial_roots_extensions.ipynb`
* `chapters/ch08_nonlinear_roots/scripts/nonlinear_root_methods.py`

## 第8章记录

### 已完成

* 8.1 区间扫描和二分法。
* 8.2 不动点、Aitken、Steffensen。
* 8.3 Newton、阻尼 Newton、重根修正。
* 8.4 弦截法与 Müller 抛物线法。
* 8.5/8.6 多项式根拓展。

### 待完成

* `chapters/ch07_iterative_linear_systems/scripts/iterative_linear_methods.py`

### 已修改文件

* `AGENTS.md`
* `.agent/execplans/chapters-07-12.md`
* `.agent/RUN_LOG.md`
* `.agent/run_logged.sh`
* `README.md`
* `src/py_sc/__init__.py`

### 不应触碰的既有修改

* `.agent/execplans/chapter-06-direct-methods.md`
* `src/py_sc/direct_linear.py`
* `tests/test_direct_linear.py`
* `.agent/RUN_LOG.md` 中 CH06 日志块
* `src/py_sc/__init__.py` 中 direct-linear 导入和 `__all__` 条目
* `docs/README.md` 中第6章外部路线图调整

## 决策日志

* 决定：创建分支 `codex/chapters-07-12`。原因：任务开始时工作树干净，用户要求用 Git checkpoint 作为恢复断点。影响：全部第 7—12 章工作在该本地分支上进行。
* 决定：不创建第 6 章。原因：用户明确要求按顺序完成第 7—12 章，仓库当前缺第 6 章但本任务范围不包含第 6 章。影响：第 7、11、12 章中涉及第六章直接法连接时，只作为前置章节空缺提示或轻量复用说明。
* 决定：新章节不再单独建立 `references.md`。原因：用户要求从现在开始章节末尾只保留一个“小结”，资料来源使用 Notebook 内联引用、链接、脚注或统一参考文件。影响：第 7—12 章目录只设置 README、notebooks、scripts，必要时使用 notes，不设置章节级 `references.md`。
* 决定：第7章 7.1 使用公共模块 `src/py_sc/iterative_linear.py` 而不是章节私有 scripts 作为正式实现。原因：前几章已采用 `src/py_sc` 作为可复用教学实现位置，章节 scripts 只作为快速运行入口。影响：`src/py_sc/__init__.py` 导出 iterative-linear 函数，Notebook 先展示教学实现再调用正式实现。
* 决定：块迭代 API 使用 `block_sizes` 而不是任意索引列表。原因：第七章教学重点是按连续变量组分块，连续块 API 更简单、错误面更小。影响：`block_jacobi_iteration` 和 `block_gauss_seidel_iteration` 支持连续块，任意子域排序留作后续拓展。
* 决定：Poisson 小规模验证提供稠密矩阵函数，同时提供矩阵-向量乘法函数。原因：测试和教学需要可与 `np.linalg.solve` 对照，但用户要求不要为大网格构造稠密矩阵。影响：`poisson_2d_dirichlet_matrix` 文档明确仅用于小规模教学验证，Notebook 中强调大网格应使用稀疏结构或 matvec。
