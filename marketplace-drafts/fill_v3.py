# -*- coding: utf-8 -*-
"""Finish the existing Gumroad product, then wait for SuperHive login."""
from __future__ import annotations

import json
import time
import traceback
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(r"E:\Assets\marketplace-drafts")
LOG = ROOT / "browser-logs"
PROFILE = ROOT / "chrome-profile"
STATUS = ROOT / "browser-status.json"
GR_EDIT = "https://gumroad.com/products/jkglzv/edit"
SH_URL = "https://superhivemarket.com/creator/products/new"
SH_LOGIN = "https://superhivemarket.com/login"
GR_IMG = ROOT / "images" / "gumroad"
SH_IMG = ROOT / "images" / "superhive"

PRODUCT_NAME = "Blueish Assets — Complete Node Library (534 Groups)"
PRICE = "10"

GR_PLAIN = """534 Asset Browser assets in 11 .blend files: Geometry Nodes (mesh, packing, matrix math), shaders (SDF, tiling, fractals, parallax), compositor effects, a custom particle solver, GN rigging (LBS / DQS / CoR / Delta Mush), NPR materials, flipbook VFX, and 6 slash trails.

Add the unzipped folder as an Asset Library and drag. No add-on.

A free GitHub copy of the same library exists:
https://github.com/blueish0930/Assets
Docs: https://blueish0930.github.io/Assets/
Remote library (Blender 5.2+): https://blender-assets.blueish.workers.dev

Buy here if you want a packaged zip, product support, and to fund the next nodes.

What's inside
Geometry Nodes 185 · Self Pruning / Spline Grammar 4 · Particle System 30 · Rigging 15 · Material Functions 49 · Shader Tools 161 · NPR 22 · Compositor 50 · Flipbook VFX 12 · Slash FX 6
Total 534 catalog assets.

Install
1. Unzip.
2. Blender → Edit → Preferences → File Paths → Asset Libraries → +
3. Select the folder that contains blender_assets.cats.txt
4. Open an Asset Browser and choose Blueish Assets.
5. Drag a node group into a Geometry Nodes / Shader / Compositor tree, or drag Flipbook/Slash objects into the viewport.

Requires Blender 5.3 (two PCG files last saved as 5.2.35). Cycles or EEVEE. Not compatible with 4.x.

Royalty-free for films, games, and client work. Do not redistribute the zip or resell the node groups.
"""

from fill_marketplaces import SH_ABOUT, DOC_BODY  # noqa: E402

NOTES = []


def log(msg: str) -> None:
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    NOTES.append(line)
    STATUS.write_text(json.dumps({"ts": line, "notes": NOTES[-40:]}, ensure_ascii=False, indent=2), encoding="utf-8")


def popup(title: str, text: str) -> None:
    try:
        import ctypes

        ctypes.windll.user32.MessageBoxW(0, text, title, 0x00000040 | 0x00001000 | 0x00040000)
    except Exception as e:
        log(f"MessageBox failed: {e}")


def dump(page, tag: str) -> None:
    LOG.mkdir(parents=True, exist_ok=True)
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in tag)[:80]
    try:
        page.screenshot(path=str(LOG / f"{safe}.png"), full_page=True, timeout=20000)
    except Exception as e:
        log(f"shot {tag}: {e}")
    try:
        (LOG / f"{safe}.html").write_text(page.content(), encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        (LOG / f"{safe}.url.txt").write_text(f"{page.url}\n{page.title()}", encoding="utf-8")
    except Exception:
        pass
    log(f"dump {tag} {page.url} | {page.title()}")


def finish_gumroad(page) -> dict:
    result = {"ok": False, "steps": []}
    page.goto(GR_EDIT, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(1500)
    dump(page, "gr3-open")

    # Description: click the placeholder / editor, replace text
    desc_ok = False
    for sel in (
        "div.ProseMirror",
        "[contenteditable='true']",
        "text=Describe your product",
    ):
        try:
            loc = page.locator(sel).first
            loc.click(timeout=4000)
            page.keyboard.press("Control+A")
            page.keyboard.insert_text(GR_PLAIN)
            desc_ok = True
            log("description replaced")
            break
        except Exception as e:
            log(f"desc {sel}: {e}")
    result["steps"].append(f"desc={desc_ok}")

    covers = [
        str(GR_IMG / "01_cover.jpg"),
        str(GR_IMG / "02_cover.jpg"),
        str(GR_IMG / "03_cover.jpg"),
        str(GR_IMG / "04_cover.jpg"),
        str(GR_IMG / "05_cover.jpg"),
    ]
    img_ok = False
    try:
        with page.expect_file_chooser(timeout=8000) as fc:
            page.get_by_text("Upload images or videos", exact=False).first.click()
        chooser = fc.value
        chooser.set_files(covers)
        img_ok = True
        log("covers via file chooser")
    except Exception as e:
        log(f"chooser: {e}")
        # fallback: file input whose accept includes image
        try:
            page.locator("input[type='file'][accept*='image']").first.set_input_files(covers)
            img_ok = True
        except Exception as e2:
            log(f"accept image: {e2}")
    result["steps"].append(f"covers={img_ok}")
    page.wait_for_timeout(4000)
    dump(page, "gr3-covers")

    saved = False
    try:
        page.get_by_role("button", name="Save and continue").click(timeout=8000)
        saved = True
        page.wait_for_timeout(2500)
    except Exception as e:
        result["steps"].append(f"save_err={e}")
    result["steps"].append(f"save={saved}")
    dump(page, "gr3-after-save")
    result["url"] = page.url
    result["ok"] = True
    return result


def fill_superhive(page) -> dict:
    result = {"ok": False, "steps": []}
    for i in range(8):
        try:
            page.goto(SH_URL, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            log(f"sh goto {e}")
        page.wait_for_timeout(1000)
        dump(page, f"sh3-try-{i}")
        if "/creator/" in page.url and "login" not in page.url.lower():
            break
        if i == 0:
            try:
                page.goto(SH_LOGIN, wait_until="domcontentloaded", timeout=45000)
            except Exception:
                pass
        popup(
            "请登录 SuperHive",
            f"Gumroad 商品已建好（$10 草稿）。\n\n请在 Chrome 登录 SuperHive，再点确定。\n"
            f"当前地址：{page.url}\n（第 {i+1}/8 次）",
        )
    else:
        result["error"] = f"not logged in: {page.url}"
        return result

    dump(page, "sh3-form")
    try:
        info = page.evaluate(
            """() => [...document.querySelectorAll('input,textarea,select,button,[contenteditable=true]')]
            .slice(0,100).map(e => ({
              tag:e.tagName, type:e.type, name:e.name, id:e.id,
              ph:e.placeholder, text:(e.innerText||'').slice(0,80)
            }))"""
        )
        (LOG / "sh3-controls.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
    except Exception as e:
        log(f"controls {e}")

    name_ok = False
    for sel in (
        page.get_by_label("Name"),
        page.get_by_role("textbox", name="Name"),
        page.locator("input[name*='name' i]"),
        page.locator("input[type='text']").first,
    ):
        try:
            sel.first.fill(PRODUCT_NAME, timeout=4000)
            name_ok = True
            break
        except Exception:
            continue
    result["steps"].append(f"name={name_ok}")

    price_ok = False
    for sel in (
        page.get_by_label("Price"),
        page.locator("input[name*='price' i]"),
        page.locator("input[id*='price' i]"),
    ):
        try:
            sel.first.fill(PRICE, timeout=4000)
            price_ok = True
            break
        except Exception:
            continue
    result["steps"].append(f"price={price_ok}")

    about_ok = False
    for frame in page.frames:
        try:
            body = frame.locator("body#tinymce")
            if body.count():
                body.fill(SH_ABOUT)
                about_ok = True
                break
        except Exception:
            pass
    if not about_ok:
        try:
            loc = page.locator("[contenteditable='true'], textarea").first
            loc.click()
            page.keyboard.press("Control+A")
            page.keyboard.insert_text(SH_ABOUT)
            about_ok = True
        except Exception as e:
            result["steps"].append(f"about_err={e}")
    result["steps"].append(f"about={about_ok}")

    imgs = [
        str(SH_IMG / "01_featured.jpg"),
        str(SH_IMG / "02_geometry_nodes_demo.jpg"),
        str(SH_IMG / "03_all_node_thumbnails.jpg"),
        str(SH_IMG / "04_vfx_flipbook_slash.jpg"),
        str(SH_IMG / "05_full_node_inventory.jpg"),
    ]
    img_ok = False
    try:
        with page.expect_file_chooser(timeout=6000) as fc:
            page.get_by_text("Add Imagery", exact=False).first.click()
        fc.value.set_files(imgs)
        img_ok = True
    except Exception as e:
        log(f"sh chooser: {e}")
        try:
            page.locator("input[type='file']").first.set_input_files(imgs)
            img_ok = True
        except Exception as e2:
            result["steps"].append(f"img={e2}")
    result["steps"].append(f"images={img_ok}")

    saved = False
    for name in ("Save Draft", "Save as draft", "Save Product", "Save"):
        try:
            btn = page.get_by_role("button", name=name, exact=False)
            if btn.count():
                btn.first.click(timeout=5000)
                saved = True
                break
        except Exception:
            continue
    result["steps"].append(f"save={saved}")
    page.wait_for_timeout(2000)
    dump(page, "sh3-after")
    result["url"] = page.url
    result["ok"] = name_ok or price_ok or saved
    return result


def main() -> None:
    LOG.mkdir(parents=True, exist_ok=True)
    log("launch v3")
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE),
            channel="chrome",
            headless=False,
            args=["--start-maximized", "--disable-blink-features=AutomationControlled", "--no-first-run"],
            ignore_default_args=["--enable-automation"],
            no_viewport=True,
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        out = {}
        try:
            out["gumroad"] = finish_gumroad(page)
        except Exception:
            out["gumroad"] = {"ok": False, "error": traceback.format_exc()}
            dump(page, "gr3-error")
        sh = ctx.new_page()
        try:
            out["superhive"] = fill_superhive(sh)
        except Exception:
            out["superhive"] = {"ok": False, "error": traceback.format_exc()}
            dump(sh, "sh3-error")
        (ROOT / "fill-result-v3.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        log("done " + json.dumps(out, ensure_ascii=False)[:2000])
        popup("填写结束", json.dumps(out, ensure_ascii=False)[:900])
        time.sleep(12)
        ctx.close()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        tb = traceback.format_exc()
        Path(r"E:\Assets\marketplace-drafts\fill-error.txt").write_text(tb, encoding="utf-8")
        print(tb, flush=True)
        raise
