# 美術素材規格（中秋海邊烤肉攤）

## 風格分工（已定案）
- **客人角色**：手遊幹員立繪風（細線稿＋賽璐珞上色＋機能風穿搭），範本 `assets/raw/cust_bear.png`。
- **食材**：Q 版手繪水彩風，範本 `assets/raw/ing_pork.png`。（曾試過把食材改平塗，使用者覺得不好看，已退回。）

通用規則：
- 背景一律用**純綠色 #00FF00**，之後由 `tools/process_assets.py` 去背成透明 PNG。主體本身不要用綠色。
- 輸出 PNG，正方形 **1024×1024**（原圖放 `assets/raw/`，遊戲用的縮小版放 `assets/`）。
- `assets/raw/` 內帶 `_v1_...`、`_painterly`、`_flat`、`_rejected` 後綴的是封存檔，僅供比較，處理腳本會自動略過。

## 客人風格（客人每一張圖的 prompt 都要帶這一段，並附 `cust_bear.png` 當風格參考圖）

```
Mobile-game operator-portrait style (general style only, do not copy any existing character):
sharp thin dark anime line art, cel shading with 2-3 tone steps and clean edges, selective fine
gradients and reflections on fabric and hair, refined detailed design.
Techwear / tactical streetwear outfit: straps, buckles, zippers, pockets, asymmetric cuts, layering;
base of black / dark gray / white / beige with exactly ONE vivid accent color.
Slender elegant proportions, calm confident or relaxed expression, natural slightly dynamic pose.
Waist-up, tight framing so the face is large and readable at small icon size
(head including ears/horns about 30-35% of image height), subject centered with a clean margin
(do not touch the canvas edges), about 85-90% of the canvas.
No text, no watermark, no cast shadow, no props, no other characters.
Background: solid flat pure green (#00FF00). No green on the subject.
```

### 獸化程度（每位角色指定一級）
| 等級 | 說明 |
|---|---|
| **Lv1 獸耳** | 完整人類臉孔，只有獸耳（和短尾巴） |
| **Lv2 半獸化** | 人類臉孔為主，加上明顯獸類特徵：獸瞳、尖牙、頰側／頸部絨毛、爪形指尖、較大的尾巴、手臂局部毛色 |
| **Lv3 高獸化** | 獸類的臉（有口鼻部），全身有毛皮，但站姿與身形是人的比例，穿衣服（kemono / 獸人） |

### 客人名單（8 位，男 5 / 女 3，全部高獸化）
使用者回饋：半獸人（人臉加獸耳）看起來比較有 AI 味，獸臉版比較有辨識度，所以所有角色都改成 **Lv3 獸臉**（含口鼻部、毛皮），並把男性比例拉高。
點綴色各不相同，玩家才能一眼分辨。**新角色一律附 `cust_wolf.png` 當畫風與大小範本**（頭含耳朵約占圖高 30%、雙肩寬約占圖寬 55~62%、左右各留 7% 空白）。
姿勢要自然有動感；**不要雙手在身前交握**（曾因此退件）。

| id | 性別 | 物種 | 點綴色 | 備註 |
|---|---|---|---|---|
| `bear` | 男 | 棕熊 | 芥末黃 | ✅ 手放頭後，新月別針 |
| `rabbit` | 女 | 白兔 | 薄荷綠 | ✅ 長兔耳一立一折 |
| `fox` | 女 | 赤狐 | 靛紫 | ✅ **刻意與狼區隔**：嬌小活潑、橘紅短髮、米白短版外套、V 字手勢加叉腰、大尾巴翹起（舊版與狼同為犬科又同樣雙手交疊，輪廓太像，已退換，舊版封存為 `cust_fox_v8_samepose.png`） |
| `panda` | 男 | 大貓熊 | 橘色 | ✅ 揮手加叉腰，壯碩 |
| `cat` | 男 | 黑豹貓 | 珊瑚紅 | ✅ 全新男性設計；插口袋、拉領口。整隻偏黑，疊在夜景上對比偏低（靠金色眼睛與紅色配件辨認） |
| `sheep` | 男 | 公羊 | 粉紅 | ✅ 全新男性設計；螺旋羊角、羊羔絨領外套 |
| `wolf` | 男 | 灰狼 | 冰藍 | ✅ **大小範本** |
| `tiger` | 女 | 老虎 | 酒紅＋金 | ✅ |

舊的人臉版封存在 `assets/raw/*_v6_humanface.png`。

**顯示大小**：每位的縮放係數在 `index.html` 的 `CUSTOMERS[].scale`（以狼為基準 1.0），用並排比較調到頭部看起來一樣大。換新圖後要重新並排校準。

## 第一批素材

### 食材（`assets/ing_<id>.png`）
畫「單一塊食材」，正面。**不要畫竹籤**（遊戲裡的籤由程式繪製）、不要畫整串、不要畫烤架。

**食材風格**（每張食材 prompt 帶這一段，並附 `ing_pork.png` 當風格參考圖）：
```
Cute chibi hand-drawn game illustration, Q-version, thick warm dark-brown outline,
soft gouache / watercolor shading with gentle highlights, warm saturated colors,
rounded simplified shapes (not photorealistic, not glossy), light from top-left.
Single subject centered, filling about 85% of the canvas, no text, no watermark, no cast shadow.
Background: solid flat pure green (#00FF00). No green on the subject. No bamboo skewer.
```

**色相要拉開**：使用者回饋原本 6 種食材都落在紅黃褐，烤熟後更難分辨。現在的組合是紅（豬肉）、綠（青蔥）、黃（玉米）、紫（茄子）、粉白（棉花糖）、橘（蝦）。新食材的 prompt 要求「主色飽和乾淨、盡量不要整個烤成咖啡色、烤痕只局部點到為止」，且蔥綠要偏黃偏深，避免與去背用的螢光綠撞色。遊戲裡氣泡也會在食材後面加一圈該食材的顏色。

| 檔名 | 內容 | 狀態 |
|---|---|---|
| `ing_pork.png` | 一塊圓潤的烤豬肉丁，粉紅偏褐，肥肉紋理與烤痕（**風格範本**） | ✅ |
| `ing_scallion.png` | 一束用麻繩綁起的烤青蔥段，鮮綠蔥葉加奶黃蔥白 | ✅ |
| `ing_corn.png` | 一段玉米（圓柱切段），金黃玉米粒 | ✅ |
| `ing_eggplant.png` | 烤茄子厚片，深紫外皮加奶白果肉切面與十字烤痕 | ✅ |
| `ing_marshmallow.png` | 一顆棉花糖，粉白色，頂面烤成焦糖色 | ✅ |
| `ing_shrimp.png` | 一隻去頭的蝦，橘紅色，彎曲，帶尾巴 | ✅ |
| ~~香腸、香菇~~ | 已撤下（色相太接近、不易分辨），原圖封存為 `assets/raw/*_retired.png` | 停用 |

### 客人（`assets/cust_<id>.png`）
名單見上方，8 位全部完成。處理腳本會依頭部位置自動對齊並完整保留身體（不裁掉手臂、袖子、尾巴）。

## 第二批素材（✅ 已完成）

| 檔名 | 內容 | 風格 | 處理後（assets/） |
|---|---|---|---|
| `bg_scene.png` | 夜晚海邊：中秋滿月、海平線與月光倒影、遠山剪影（無人物、低對比） | 柔和動漫繪景 | `bg_scene.jpg` 1080×636（置中覆蓋裁切，鋪客人區） |
| `icon_trash.png` | Q 版金屬垃圾桶（桶蓋歪斜、露出皺紙） | 手繪水彩（同食材） | `icon_trash.png` 256×256 去背 |
| `grate.png` | 烤架格子底圖：木炭＋6 根垂直鐵棒，底部透出餘燼光 | 手繪水彩（同食材） | `grate.jpg` 512×512，遊戲端再疊暗色漸層讓食物跳出來 |

## 流程（Claude 交付 → Codex 執行 → Claude 審查）

1. Claude 以 `codex exec`（推理強度 medium）交付任務，已通過的圖作為風格參考圖附上。
2. Claude 逐張審查：尺寸、純綠背景、風格一致性、是否符合規格。不過關就寫明退件原因並請 Codex 重做。
3. 全部通過後執行 `python tools/process_assets.py` 去背縮圖，並把檔案加進 `index.html` 的 `ART_FILES`。
4. 本機預覽請用 `.claude/launch.json` 的 `bbq-static`（本機小伺服器）；直接雙擊 `index.html` 也能玩，但瀏覽器預覽窗格讀不到相對路徑的圖。

## UI 風格（遊戲介面，非美術圖）

參考使用者公司專案的 UI 語彙，**稍微偏向、不照抄**（不使用其 Logo、字樣、角色，截圖也不放進專案）。元件都在 `index.html` 的 `UI` 與 `ui*` 函式，純平面、沒有立體感或發光。

| 元素 | 做法 |
|---|---|
| 配色 | 炭灰底（`#1b2021` / `#101314`）、洋紅 `#c900df`、紫 `#9c43d3`、青綠 `#19e3a0`、米色 `#e3dbcb`、紅色菱形提示 `#ff3b5c`；遊戲世界仍保留月光金與夜景 |
| 面板 | 深色底 + 上紫下青綠的漸層邊框（`uiPanel`） |
| 標題列 | 洋紅底，兩端深色棋盤格（`uiTitleBar`），壓在面板上緣 |
| 關閉 / 繼續 | 菱形 X，騎在對話框下緣（`uiDiamondX`） |
| 資訊標籤 | 米色底深色字，左上小綠缺角（`uiChip`、HUD 的時間與分數） |
| 按鈕 | 主要＝青綠實心；次要＝米色 + 綠缺角；上方有英文小標籤（`uiButton`） |
| 新提示 | 紅色菱形加驚嘆號（新解鎖食材，托盤上顯示 10 秒，`uiBadge`） |
| 底部 | 炭灰底加細網格 |
| 鍵盤提示 | 純平面淺色小標籤，只在用鍵盤時顯示 |

> **角色之間要拉開輪廓**：同科的角色（例如狐與狼）除了臉以外，姿勢、體型、髮型、衣服底色也要不同；每新增一位，先和現有角色並排看剪影是否容易混淆。
