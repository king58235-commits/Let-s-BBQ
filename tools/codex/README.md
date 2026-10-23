# tools/codex — Claude ↔ Codex 生圖協作工具

這是 2026-10-23 做《中秋海邊烤肉攤》時整理出的做法（細節與數據見 [`docs/TECH_REPORT.md`](../../docs/TECH_REPORT.md) §4、§5、§8）。

| 檔案 | 用途 |
|---|---|
| `run_task.sh` | 以非互動模式交付一個任務；支援參考圖、平行（`xargs -P`）、記錄事件與用量 |
| `TASK_TEMPLATE.md` | 任務檔範本與退件段落、審查清單 |
| `tasks/` | 任務檔放這裡（`<任務名>.txt`） |
| `out/` | 執行紀錄（`.jsonl` 含 token 用量、`_last.txt` 是 Codex 的回報；已加入 `.gitignore`） |

## 最短流程
```bash
# 1. 寫任務檔（照 TASK_TEMPLATE.md）
# 2. 交付（要附參考圖就寫檔名；圖放在 assets/raw/）
tools/codex/run_task.sh ing_pork ing_pork.png
# 3. 客觀檢查，再目視；通過後後製
python tools/check_raw.py ing_pork
python tools/process_assets.py
```

## 看用量
```python
import json
for line in open("tools/codex/out/ing_pork.jsonl", encoding="utf-8"):
    e = json.loads(line)
    if e.get("type") == "turn.completed": print(e["usage"])   # input / cached_input / output / reasoning_output tokens
```
注意：這**看不到圖像生成本身的額度**（只有文字 token）。要得到「每張圖多少額度」，記下額度百分比，連續跑同樣的 N 張再比對。
