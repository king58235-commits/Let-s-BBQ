"""審查前的客觀檢查：對 assets/raw/ 指定的原圖檢查尺寸、純綠背景、主體是否貼邊。

用法： python tools/check_raw.py cust_rabbit ing_corn ...   （不帶副檔名）
"""
import sys
from pathlib import Path

from PIL import Image

RAW = Path(__file__).resolve().parent.parent / "assets" / "raw"


def is_bg(p):
    r, g, b = p[:3]
    return g - max(r, b) >= 150


def check_fullbleed(name, img):
    """背景、材質這類「鋪滿畫面」的圖：回報尺寸、平均亮度，以及是否誤含純綠。"""
    w, h = img.size
    px = img.load()
    n = green = 0
    lum = 0.0
    for y in range(0, h, 4):
        for x in range(0, w, 4):
            r, g, b = px[x, y]
            lum += 0.2126 * r + 0.7152 * g + 0.0722 * b
            green += is_bg((r, g, b))
            n += 1
    mean, gp = lum / n, green / n
    issues = []
    if gp > 0.02:
        issues.append(f"含 {gp:.0%} 純綠像素（鋪滿型的圖不該有綠幕）")
    return f"{name}: {'✅' if not issues else '⚠️'} 尺寸 {w}x{h}，平均亮度 {mean:.0f}/255" + ("；" + "；".join(issues) if issues else "")


def check(name):
    path = RAW / f"{name}.png"
    if not path.exists():
        return f"{name}: ❌ 檔案不存在"
    img = Image.open(path).convert("RGB")
    if name in ("bg_scene", "grate"):
        return check_fullbleed(name, img)
    w, h = img.size
    px = img.load()
    issues = []
    if (w, h) != (1024, 1024):
        issues.append(f"尺寸 {w}x{h}（要 1024x1024）")
    for cx, cy in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)):
        r, g, b = px[cx, cy]
        if not (r < 40 and g > 215 and b < 40):
            issues.append(f"角落不是純綠 {px[cx, cy]}")
            break
    xs, ys, n = [], [], 0
    step = 2
    for y in range(0, h, step):
        for x in range(0, w, step):
            if not is_bg(px[x, y]):
                xs.append(x); ys.append(y); n += 1
    if not n:
        return f"{name}: ❌ 沒有主體"
    left, right, top, bottom = min(xs), w - 1 - max(xs), min(ys), h - 1 - max(ys)
    m = min(left, right, top, bottom)
    cover = n * step * step / (w * h)
    bw = (max(xs) - min(xs)) / w
    bh = (max(ys) - min(ys)) / h
    if name.startswith("cust_"):
        # 半身像：身體在下緣、左右被裁切是正常的，只要求頭頂（含耳朵/角）不被切到
        if top < 30:
            issues.append(f"頭頂太貼上緣（{top}px，要 >= 30）")
        if min(left, right) < 12:
            issues.append(f"手臂/衣服被畫布左右邊緣切到（左{left} 右{right}px，要 >= 12）")
    elif m < 20:
        side = {"左": left, "右": right, "上": top, "下": bottom}
        hit = [k for k, v in side.items() if v < 20]
        issues.append("主體貼邊/被裁切：" + "、".join(hit))
    status = "✅" if not issues else "⚠️"
    return (f"{name}: {status} 邊距 左{left} 右{right} 上{top} 下{bottom}px，"
            f"主體寬{bw:.0%} 高{bh:.0%}，覆蓋{cover:.0%}" + ("；" + "；".join(issues) if issues else ""))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for n in sys.argv[1:]:
        print(check(n))
