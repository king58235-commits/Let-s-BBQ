"""把 assets/raw/ 裡通過審查的綠幕原圖去背並縮小，輸出到 assets/。

用法（在專案根目錄）：  python tools/process_assets.py
只處理檔名符合 ing_<名稱>.png / cust_<名稱>.png 的檔案，
帶有 _v1_rejected、_painterly 等後綴的封存檔會自動略過。

食材：去背後縮成 256x256。
客人：去背後「依頭部位置自動對齊」——頭頂（含耳朵/角）貼齊上緣、頭在圖的水平正中央、
      身體左右完整保留不裁切（寬度依身體而定，高度 582），讓遊戲裡每位客人的頭頂高度與氣泡位置一致。
"""
import re
import sys
import time
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "assets" / "raw"
OUT = ROOT / "assets"
NAME_RE = re.compile(r"^((ing|cust|icon)_[a-z]+|bg_scene|grate)\.png$")
ING_SIZE = 256            # 食材、icon 的輸出邊長
BG_OUT = (1080, 636)      # 背景：只用來鋪客人區（畫面 540x318 的 2 倍）
GRATE_SIZE = 512          # 烤架格子材質
CUST_WIN = (717, 869)      # 原圖(1024)上的裁切框 寬x高
CUST_OUT = (480, 582)      # 輸出尺寸（與裁切框同比例）
TOP_PAD = 14               # 頭頂上方多留的像素（原圖座標）


def key_green(img: Image.Image) -> Image.Image:
    """純綠 #00FF00 背景 → 透明，邊緣做半透明與去綠邊。"""
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            spill = g - max(r, b)          # 綠色超出紅藍的程度：背景約 255，主體接近 0
            # 薄荷綠這類「偏淡的綠」約為 55~65，必須完全不動；只處理接近純綠的背景與邊緣
            if spill >= 200:
                px[x, y] = (0, 0, 0, 0)
            elif spill > 80:
                t = (spill - 80) / 120.0
                alpha = int(a * (1 - t))
                g2 = max(r, b) + int(spill * 0.1)
                px[x, y] = (r, min(g, g2), b, alpha)
    return img


def head_box(img: Image.Image):
    """回傳 (頂端 y, 頭部水平中心 x)。頭部中心取最上方 40% 身高範圍內不透明像素的平均 x。"""
    a = img.getchannel("A")
    w, h = img.size
    ap = a.load()
    top = bottom = None
    for y in range(h):
        if any(ap[x, y] > 40 for x in range(0, w, 2)):
            if top is None:
                top = y
            bottom = y
    band_end = top + int((bottom - top) * 0.4)
    xs = [x for y in range(top, band_end, 2) for x in range(0, w, 2) if ap[x, y] > 40]
    return top, sum(xs) / len(xs)


def crop_customer(img: Image.Image) -> Image.Image:
    """以頭部為水平中心、左右對稱地保留整個身體（不裁掉手臂、袖子、尾巴）。
    高度固定（頭頂貼齊上緣，下緣自然截斷）；寬度依身體範圍而定，最窄不小於 CUST_WIN 寬。
    輸出圖的水平正中央就是頭，遊戲裡直接以頭為中心繪製。"""
    w, h = img.size
    top, cx = head_box(img)
    ap = img.getchannel("A").load()
    xs = [x for y in range(0, h, 2) for x in range(0, w, 2) if ap[x, y] > 40]
    reach = max(cx - min(xs), max(xs) - cx) + 6          # 身體離頭中心最遠的距離
    half = max(CUST_WIN[0] / 2, reach)
    ch = CUST_WIN[1]
    y0 = max(0, top - TOP_PAD)
    x0, x1 = int(round(cx - half)), int(round(cx + half))
    out = img.crop((x0, y0, x1, y0 + ch))                # 超出畫布的部分自動補透明
    scale = CUST_OUT[0] / CUST_WIN[0]
    return out.resize((round(out.width * scale), round(ch * scale)), Image.LANCZOS)


def cover_crop(img: Image.Image, size) -> Image.Image:
    """把圖等比放大到完整覆蓋 size，再以「垂直置中」裁掉多出來的部分（月亮與海平線在中間）。"""
    tw, th = size
    s = max(tw / img.width, th / img.height)
    nw, nh = round(img.width * s), round(img.height * s)
    img = img.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - tw) // 2, (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))


def main() -> int:
    files = sorted(p for p in RAW.glob("*.png") if NAME_RE.match(p.name))
    if not files:
        print("assets/raw/ 裡沒有符合命名規則的圖")
        return 1
    for src in files:
        stem = src.stem
        if stem in ("bg_scene", "grate"):                # 不去背的整張圖：存成 JPEG（檔案小）
            img = Image.open(src).convert("RGB")
            if stem == "bg_scene":
                img = cover_crop(img, BG_OUT)
            else:
                img = img.resize((GRATE_SIZE, GRATE_SIZE), Image.LANCZOS)
            dst = OUT / f"{stem}.jpg"
            img.save(dst, quality=88, optimize=True)
        else:
            kind = stem.split("_", 1)[0]
            img = key_green(Image.open(src))
            if kind == "cust":
                img = crop_customer(img)
            else:                                        # ing / icon
                img = img.resize((ING_SIZE, ING_SIZE), Image.LANCZOS)
            dst = OUT / src.name
            img.save(dst, optimize=True)
        print(f"{src.name} -> assets/{dst.name} {img.size[0]}x{img.size[1]}")
    bump_asset_version()
    return 0


def bump_asset_version() -> None:
    """把 index.html 裡的 ASSET_VER 改成現在時間，讓瀏覽器重新下載剛更新的圖（否則會用快取的舊圖）。"""
    html = ROOT / "index.html"
    text = html.read_text(encoding="utf-8")
    ver = time.strftime("%Y%m%d%H%M%S")
    new, n = re.subn(r"const ASSET_VER = '[^']*';", f"const ASSET_VER = '{ver}';", text)
    if n == 1:
        html.write_text(new, encoding="utf-8")
        print(f"ASSET_VER -> {ver}")
    else:
        print("找不到 ASSET_VER，沒有更新版本號")


if __name__ == "__main__":
    sys.exit(main())
