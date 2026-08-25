# -*- coding: utf-8 -*-
"""Build SuperHive 2:1 and Gumroad 16:9 listing images from REAL library thumbs/screenshots."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(r"E:\Assets")
ASSETS = ROOT / "blender" / "assets"
DOCS_DESK = ROOT / "docs" / "Desktop"
OUT_SH = ROOT / "marketplace-drafts" / "images" / "superhive"
OUT_GR = ROOT / "marketplace-drafts" / "images" / "gumroad"
CATS_FILE = ASSETS / "blender_assets.cats.txt"
INDEX = ASSETS / "_v1" / "assets-00000.json"

# SuperHive: 2:1, min 1200x600, featured JPG <5MB
SH_W, SH_H = 2560, 1280
# Gumroad cover: 16:9, min 1280x720
GR_W, GR_H = 2560, 1440
# Gumroad thumbnail: min 600x600
TH_S = 1200

BG = (18, 20, 26)
BG2 = (28, 31, 40)
INK = (230, 234, 241)
MUTED = (140, 148, 164)
ACCENT = (255, 138, 43)
LINE = (48, 52, 64)

SHOT_FEATURED = DOCS_DESK / "Desktop Screenshot 2026.07.09 - 23.11.45.20.png"
# 12.01.02 has a Douyin live overlay — do not use for storefront.
SHOT_DEMO = DOCS_DESK / "Desktop Screenshot 2026.07.09 - 23.16.48.65.png"

EN_CAT = {
    "Material/平铺": "Material/Tiling",
    "Material/平铺/Tools": "Material/Tiling/Tools",
    "Material/平铺/平铺纹理": "Material/Tiling/Patterns",
    "三渲二": "Stylized NPR",
}


def font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    if mono:
        cands = [r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\cour.ttf"]
    elif bold:
        cands = [
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\msyhbd.ttc",
        ]
    else:
        cands = [
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\msyh.ttc",
        ]
    for p in cands:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()


def load_cats() -> dict[str, str]:
    out = {}
    for line in CATS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("VERSION"):
            continue
        uuid, path, _simple = line.split(":", 2)
        out[uuid] = EN_CAT.get(path, path)
    return out


def load_assets():
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    cats = load_cats()
    rows = []
    for a in data["assets"]:
        cid = (a.get("meta") or {}).get("catalog_id", "")
        cat = cats.get(cid, "Uncategorized")
        thumb = (a.get("thumbnail") or {}).get("url")
        rows.append(
            {
                "name": a["name"],
                "id_type": a.get("id_type", ""),
                "file": (a.get("files") or ["?"])[0],
                "cat": cat,
                "thumb": (ASSETS / thumb) if thumb else None,
                "desc": (a.get("meta") or {}).get("description") or "",
            }
        )
    rows.sort(key=lambda r: (r["cat"].lower(), r["name"].lower()))
    return rows, data


def open_rgb(path: Path) -> Image.Image:
    im = Image.open(path)
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", im.size, BG)
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def crop_ratio(im: Image.Image, ratio: float, top: int = 32) -> Image.Image:
    """Crop a 2:1 or 16:9 window from a desktop screenshot, skipping the title bar."""
    w, h = im.size
    target_h = int(w / ratio)
    if target_h > h - top:
        target_h = h
        top = 0
    # Prefer keeping the upper UI (Asset Browser). Clamp to exclude typical taskbar.
    max_y = h - 48
    y0 = top
    y1 = y0 + target_h
    if y1 > max_y:
        y1 = max_y
        y0 = max(0, y1 - target_h)
    crop = im.crop((0, y0, w, y0 + target_h))
    return crop.resize((int(target_h * ratio), target_h), Image.Resampling.LANCZOS)


def fit_canvas(im: Image.Image, size: tuple[int, int], fill=BG) -> Image.Image:
    canvas = Image.new("RGB", size, fill)
    tw, th = size
    scale = min(tw / im.width, th / im.height)
    nw, nh = max(1, int(im.width * scale)), max(1, int(im.height * scale))
    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.paste(resized, ((tw - nw) // 2, (th - nh) // 2))
    return canvas


def save_jpg(im: Image.Image, path: Path, quality: int = 90) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rgb = im.convert("RGB")
    rgb.save(path, "JPEG", quality=quality, optimize=True, subsampling=1)
    kb = path.stat().st_size / 1024
    print(f"  wrote {path.name:40s} {rgb.size[0]}x{rgb.size[1]}  {kb:.0f} KB")


def header_bar(draw: ImageDraw.ImageDraw, w: int, h: int, title: str, subtitle: str) -> None:
    draw.rectangle((0, 0, w, h), fill=BG2)
    draw.rectangle((0, h - 3, w, h), fill=ACCENT)
    draw.text((36, 18), title, font=font(36, bold=True), fill=INK)
    bbox = draw.textbbox((36, 18), title, font=font(36, bold=True))
    draw.text((bbox[2] + 22, 30), subtitle, font=font(20), fill=MUTED)


def img_featured():
    src = open_rgb(SHOT_FEATURED)
    sh = fit_canvas(crop_ratio(src, 2.0, top=36), (SH_W, SH_H))
    gr = fit_canvas(crop_ratio(src, 16 / 9, top=36), (GR_W, GR_H))
    # Square thumb: Asset Browser catalog only (no empty node editor).
    pane = src.crop((8, 70, 1012, 758))
    thumb = Image.new("RGB", (TH_S, TH_S), (38, 38, 38))
    scale = TH_S / pane.width
    nw, nh = TH_S, int(pane.height * scale)
    resized = pane.resize((nw, nh), Image.Resampling.LANCZOS)
    thumb.paste(resized, (0, (TH_S - nh) // 2))
    save_jpg(sh, OUT_SH / "01_featured.jpg", 88)
    save_jpg(gr, OUT_GR / "01_cover.jpg", 88)
    save_jpg(thumb, OUT_GR / "thumbnail.jpg", 88)


def img_catalog_demo():
    src = open_rgb(SHOT_DEMO)
    sh = fit_canvas(crop_ratio(src, 2.0, top=36), (SH_W, SH_H))
    gr = fit_canvas(crop_ratio(src, 16 / 9, top=36), (GR_W, GR_H))
    save_jpg(sh, OUT_SH / "02_geometry_nodes_demo.jpg")
    save_jpg(gr, OUT_GR / "02_cover.jpg")


def img_all_thumbs(rows):
    """Visual inventory: every real Asset Browser thumbnail in the library."""
    W, H = 3840, 1920
    header = 88
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)
    thumbs = [r for r in rows if r["thumb"] and r["thumb"].exists()]
    n = len(thumbs)
    header_bar(
        draw,
        W,
        header,
        "Complete node preview sheet",
        f"{n} real Asset Browser thumbnails  ·  {len(rows)} catalog assets  ·  11 .blend files  ·  no generated art",
    )

    pad = 10
    area_w, area_h = W - pad * 2, H - header - pad
    # Largest cell that still fits every real thumbnail.
    cell = 128
    while cell > 24:
        cols = max(1, area_w // cell)
        rows_n = (n + cols - 1) // cols
        if rows_n * cell <= area_h:
            break
        cell -= 1
    cols = max(1, area_w // cell)
    rows_n = (n + cols - 1) // cols
    grid_w = cols * cell
    grid_h = rows_n * cell
    x0 = (W - grid_w) // 2
    y0 = header + (area_h - grid_h) // 2

    inner = max(8, cell - 6)
    for i, r in enumerate(thumbs):
        c, rr = i % cols, i // cols
        x = x0 + c * cell + (cell - inner) // 2
        y = y0 + rr * cell + (cell - inner) // 2
        box = Image.new("RGB", (inner, inner), (24, 26, 32))
        try:
            thumb = open_rgb(r["thumb"])
            thumb.thumbnail((inner, inner), Image.Resampling.LANCZOS)
            ox = (inner - thumb.width) // 2
            oy = (inner - thumb.height) // 2
            box.paste(thumb, (ox, oy))
        except Exception:
            pass
        canvas.paste(box, (x, y))

    sh = fit_canvas(canvas, (SH_W, SH_H))
    gr = fit_canvas(canvas, (GR_W, GR_H))
    save_jpg(canvas, OUT_SH / "03_all_node_thumbnails.jpg", 86)
    # SuperHive also accepts 3840x1920 (2:1). Keep the hi-res as the upload file.
    save_jpg(sh, OUT_SH / "03_all_node_thumbnails_2560.jpg", 86)
    save_jpg(gr, OUT_GR / "03_cover.jpg", 86)


def img_vfx():
    W, H = 3840, 1920
    canvas = Image.new("RGB", (W, H), (8, 8, 10))
    draw = ImageDraw.Draw(canvas)
    header_bar(
        draw,
        W,
        88,
        "Flipbook VFX + Slash FX  —  real product renders",
        "Blood · Bubble · Dust · Explosion · Fire · Ice · Smoke · Water · 6 slash variants",
    )

    flip_dir = ASSETS / "VFX" / "Flipbook" / "Thumbnails"
    slash_dir = ASSETS / "VFX" / "Slash" / "Thumbnails"
    flip_names = ["Explosion.png", "Fire.png", "Smoke.png", "Water.png", "Ice.png", "Blood.png", "Dust.png", "Bubble.png"]
    slash_names = ["01.png", "02.png", "03.png", "04.png", "05.png", "06.png", "07.png"]

    tiles: list[tuple[str, Path]] = []
    for n in flip_names:
        p = flip_dir / n
        if p.exists():
            tiles.append((n.replace(".png", ""), p))
    for n in slash_names:
        p = slash_dir / n
        if p.exists():
            tiles.append((f"Slash {n[1]}", p))

    # 5 x 3 fills a 2:1 frame (8 flipbooks + 7 slash previews).
    cols, rows_n = 5, 3
    pad, header = 28, 88
    gap = 16
    area_w = W - pad * 2
    area_h = H - header - pad - 8
    tw = (area_w - gap * (cols - 1)) // cols
    th = (area_h - gap * (rows_n - 1)) // rows_n
    side = min(tw, th)
    grid_w = cols * side + (cols - 1) * gap
    grid_h = rows_n * side + (rows_n - 1) * gap
    x0 = (W - grid_w) // 2
    y0 = header + (H - header - grid_h) // 2

    for i, (label, path) in enumerate(tiles[: cols * rows_n]):
        c, r = i % cols, i // cols
        x = x0 + c * (side + gap)
        y = y0 + r * (side + gap)
        im = open_rgb(path).resize((side, side), Image.Resampling.LANCZOS)
        canvas.paste(im, (x, y))
        # caption strip
        draw.rectangle((x, y + side - 36, x + side, y + side), fill=(0, 0, 0, ))
        draw.text((x + 10, y + side - 30), label, font=font(18, bold=True), fill=INK)

    save_jpg(canvas, OUT_SH / "04_vfx_flipbook_slash.jpg", 88)
    save_jpg(fit_canvas(canvas, (GR_W, GR_H), (8, 8, 10)), OUT_GR / "04_cover.jpg", 88)


def img_inventory(rows):
    W, H = 3840, 1920
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)
    by_cat: dict[str, list[str]] = defaultdict(list)
    for r in rows:
        by_cat[r["cat"]].append(r["name"])

    header_bar(
        draw,
        W,
        78,
        "Full node inventory  —  534 assets from the scanned .blend files",
        "Names taken from blender/assets/_v1/assets-00000.json  ·  grouped by Asset Browser catalog",
    )

    # Flatten to labeled blocks
    blocks = []
    for cat in sorted(by_cat):
        names = sorted(by_cat[cat], key=str.lower)
        blocks.append((cat, names))

    cols = 6
    col_w = (W - 40) // cols
    x_margin, y_margin = 20, 92
    col_x = [x_margin + i * col_w for i in range(cols)]
    col_y = [y_margin] * cols
    col_i = 0
    f_cat = font(13, bold=True)
    f_item = font(12)
    line_h = 16
    cat_h = 20
    footer_limit = H - 32

    def next_col_if_needed(need: int):
        nonlocal col_i
        if col_y[col_i] + need > footer_limit:
            col_i += 1
            if col_i >= cols:
                return False
        return True

    overflow = []
    for cat, names in blocks:
        need = cat_h + line_h * len(names) + 8
        # If the whole block won't fit, split by remaining space
        while names:
            if col_i >= cols:
                overflow.extend(names)
                names = []
                break
            remaining = footer_limit - col_y[col_i]
            if remaining < cat_h + line_h * 3:
                col_i += 1
                continue
            can = max(1, (remaining - cat_h - 8) // line_h)
            chunk, names = names[:can], names[can:]
            x = col_x[min(col_i, cols - 1)]
            y = col_y[min(col_i, cols - 1)]
            draw.text((x, y), f"{cat}  ({len(by_cat[cat])})", font=f_cat, fill=ACCENT)
            y += cat_h
            for nm in chunk:
                draw.text((x + 8, y), nm, font=f_item, fill=INK)
                y += line_h
            y += 10
            col_y[min(col_i, cols - 1)] = y

    draw.text(
        (24, H - 28),
        "Blueish Assets  ·  scanned from E:\\Assets\\blender\\assets  ·  519 node groups + 15 objects  ·  Blender 5.2 / 5.3",
        font=font(14),
        fill=MUTED,
    )
    if overflow:
        print("WARNING overflow names:", len(overflow), overflow[:8])

    save_jpg(canvas, OUT_SH / "05_full_node_inventory.jpg", 90)
    save_jpg(fit_canvas(canvas, (GR_W, GR_H)), OUT_GR / "05_cover.jpg", 90)


def write_inventory_markdown(rows, files_meta):
    by_cat = defaultdict(list)
    by_file = defaultdict(list)
    for r in rows:
        by_cat[r["cat"]].append(r)
        by_file[r["file"]].append(r)
    lines = [
        "# Blueish Assets — scanned inventory",
        "",
        "Source of truth: `E:\\Assets\\blender\\assets\\_v1\\assets-00000.json`",
        "",
        f"- **{len(rows)}** catalog assets",
        f"- **{len(files_meta)}** `.blend` files",
        f"- Node groups: **{sum(1 for r in rows if r['id_type']=='NODETREE')}**",
        f"- Objects: **{sum(1 for r in rows if r['id_type']=='OBJECT')}**",
        "",
        "## Files",
        "",
        "| Blend file | Bytes | Blender | Assets |",
        "|---|---:|---|---:|",
    ]
    size = {f["path"]: f for f in files_meta}
    for path, items in sorted(by_file.items()):
        meta = size.get(path, {})
        lines.append(
            f"| `{path}` | {meta.get('size_in_bytes','') :,} | {meta.get('blender_version','')} | {len(items)} |"
            if isinstance(meta.get("size_in_bytes"), int)
            else f"| `{path}` |  | {meta.get('blender_version','')} | {len(items)} |"
        )
    lines += ["", "## Catalogs", ""]
    for cat, items in sorted(by_cat.items()):
        lines += [f"### {cat} ({len(items)})", ""]
        for r in items:
            mark = "" if (r["thumb"] and r["thumb"].exists()) else " *(no thumbnail)*"
            extra = f" — {r['desc']}" if r["desc"] else ""
            lines.append(f"- **{r['name']}**{mark}{extra}")
        lines.append("")
    out = ROOT / "marketplace-drafts" / "INVENTORY.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", out)


def main():
    OUT_SH.mkdir(parents=True, exist_ok=True)
    OUT_GR.mkdir(parents=True, exist_ok=True)
    rows, data = load_assets()
    print(f"loaded {len(rows)} assets, {len(data['files'])} files")
    write_inventory_markdown(rows, data["files"])
    print("01 featured")
    img_featured()
    print("02 catalog demo")
    img_catalog_demo()
    print("03 all thumbs")
    img_all_thumbs(rows)
    print("04 vfx")
    img_vfx()
    print("05 inventory")
    img_inventory(rows)
    print("done")


if __name__ == "__main__":
    main()
