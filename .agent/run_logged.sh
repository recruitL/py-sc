#!/usr/bin/env bash
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$ROOT/.agent/logs"
RUN_LOG="$ROOT/.agent/RUN_LOG.md"
mkdir -p "$LOG_DIR"

timestamp="$(date -Iseconds)"
safe_timestamp="${timestamp//[:+]/-}"
log_file="$LOG_DIR/command-${safe_timestamp}-$$.log"

{
  echo "timestamp: $timestamp"
  echo "cwd: $(pwd)"
  echo "command: $*"
  echo "---- output ----"
} >"$log_file"

"$@" >>"$log_file" 2>&1
exit_code=$?

{
  echo
  echo "[$timestamp] [COMMAND] [EXIT $exit_code]"
  echo "命令：\`$*\`"
  echo "退出码：$exit_code"
  echo "日志：\`$log_file\`"
  if [ "$exit_code" -eq 0 ]; then
    echo "摘要：命令执行成功。"
  else
    echo "摘要：命令执行失败，需查看日志并修复。"
  fi
} >>"$RUN_LOG"

exit "$exit_code"
