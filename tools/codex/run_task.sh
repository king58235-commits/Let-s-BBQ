#!/usr/bin/env bash
# 以非互動模式把一個任務交給 Codex CLI（主要用來生圖）。
#
# 用法：  tools/codex/run_task.sh <任務名> [參考圖檔名 ...]
#   任務檔：tools/codex/tasks/<任務名>.txt          （寫法見 TASK_TEMPLATE.md）
#   參考圖：放在 assets/raw/，這裡只寫檔名
#   紀錄：  tools/codex/out/<任務名>.{jsonl,err,_last.txt}   （事件與用量、錯誤、Codex 的最後訊息）
#
# 平行執行（同時 3 個）：  cat tools/codex/jobs.txt | xargs -P 3 -L 1 tools/codex/run_task.sh
#   jobs.txt 每行：  任務名 參考圖1 參考圖2 ...
#
# 環境變數：
#   CODEX_BIN     Codex CLI 的路徑。Windows 的 npm 版在 %APPDATA%\npm\codex.cmd；
#                 Microsoft Store 版 App 的執行檔在受保護資料夾，無法從外部呼叫。
#   CODEX_EFFORT  推理強度，預設 medium（生圖幾乎不需要推理）。
#   CODEX_SANDBOX 沙盒模式，預設 workspace-write；做程式碼審查時用 read-only（只讀、不能改檔）。
#   CODEX_EXTRA   額外參數（例如 "-m 模型名"）。
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && { pwd -W 2>/dev/null || pwd; })"   # Git Bash 用 D:/... 格式，傳給 Windows 版 codex 比 /d/... 穩
TASKS="$ROOT/tools/codex/tasks"
OUT="$ROOT/tools/codex/out"
RAW="$ROOT/assets/raw"

name="${1:?用法：run_task.sh <任務名> [參考圖檔名 ...]}"; shift
task="$TASKS/$name.txt"
[ -f "$task" ] || { echo "找不到任務檔：$task" >&2; exit 2; }

if [ -z "${CODEX_BIN:-}" ]; then
  if command -v codex >/dev/null 2>&1; then CODEX_BIN="codex"
  elif [ -n "${APPDATA:-}" ] && [ -f "$APPDATA/npm/codex.cmd" ]; then CODEX_BIN="$APPDATA/npm/codex.cmd"
  else echo "找不到 codex。請安裝 npm 版 CLI（npm i -g @openai/codex）或設定 CODEX_BIN" >&2; exit 3; fi
fi

mkdir -p "$OUT"
args=()
for f in "$@"; do
  [ -f "$RAW/$f" ] || { echo "找不到參考圖：$RAW/$f" >&2; exit 4; }
  args+=(-i "$RAW/$f")
done

"$CODEX_BIN" exec -C "$ROOT" -s "${CODEX_SANDBOX:-workspace-write}" --skip-git-repo-check \
  -c "model_reasoning_effort=\"${CODEX_EFFORT:-medium}\"" ${CODEX_EXTRA:-} \
  "${args[@]}" -o "$OUT/${name}_last.txt" --json - \
  < "$task" > "$OUT/$name.jsonl" 2> "$OUT/$name.err"
code=$?
echo "$name exit=$code"
exit $code
