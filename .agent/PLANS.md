# Agent Plans

本目录保存长时间任务的持久计划、运行日志和命令输出。任何跨多个章节、多个阶段或可能中断的任务，都必须有一个活动 ExecPlan。

## 恢复流程

新会话开始后，在修改文件之前依次执行：

1. 阅读 `AGENTS.md`；
2. 阅读本文件；
3. 阅读活动 ExecPlan，例如 `.agent/execplans/chapters-07-12.md`；
4. 阅读 `.agent/RUN_LOG.md` 的最后部分；
5. 执行 `git status --short`；
6. 执行 `git log -10 --oneline`；
7. 核对 ExecPlan 中的最后安全 commit 和当前工作树；
8. 对 ExecPlan 中列出的未验证文件执行最小验证；
9. 从“下一项具体动作”继续。

不要仅根据聊天记忆或文件是否存在判断任务完成。若 ExecPlan、Git 历史和工作树冲突，以实际文件和 Git 状态为代码事实，重新运行最小验证，修正 ExecPlan，并在 `.agent/RUN_LOG.md` 中记录。

## 原子工作单元

原子工作单元通常是：

* 一个核心 Notebook 及其关联 scripts、公共模块和 tests；
* 一个完整小节；
* 一个章节入口和导航；
* 一轮章节自检与修复。

每个原子工作单元结束后必须更新 ExecPlan、追加 RUN_LOG、运行最小检查，并在安全时创建 checkpoint commit。

## 命令日志

较长命令的完整输出保存到 `.agent/logs/`。`.agent/RUN_LOG.md` 只记录命令、退出码、摘要和日志路径，不保存大段输出。
