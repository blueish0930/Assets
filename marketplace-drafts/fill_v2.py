# -*- coding: utf-8 -*-
"""Fill Gumroad + SuperHive product drafts at $10 using the real form layout."""
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

PRODUCT_NAME = "Blueish Assets — Complete Node Library (534 Groups)"
PRICE = "10"
SH_URL = "https://superhivemarket.com/creator/products/new"
SH_LOGIN = "https://superhivemarket.com/login"
GR_URL = "https://gumroad.com/products/new"

from fill_marketplaces import DOC_BODY, GR_DESC, SH_ABOUT, SH_IMG, GR_IMG  # noqa: E402

NOTES = []


def log(msg: str) -> None:
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    NOTES.append(line)
    STATUS.write_text(
        json.dumps({"ts": line, "notes": NOTES[-50:]}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


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
    except Exception as e:
        log(f"html {tag}: {e}")
    try:
        (LOG / f"{safe}.url.txt").write_text(f"{page.url}\n{page.title()}", encoding="utf-8")
    except Exception:
        pass
    log(f"dump {tag} url={page.url} title={page.title()}")


def fill_labeled(page, label: str, value: str) -> bool:
    for getter in (
        lambda: page.get_by_label(label, exact=True),
        lambda: page.get_by_role("textbox", name=label, exact=False),
        lambda: page.locator(f"label:has-text('{label}')").locator("xpath=following::input[1]"),
    ):
        try:
            loc = getter().first
            loc.wait_for(state="visible", timeout=4000)
            loc.click()
            loc.fill("")
            loc.fill(value)
            log(f"filled label={label!r}")
            return True
        except Exception as e:
            log(f"label {label!r} try failed: {e}")
    return False


def fill_gumroad(page) -> dict:
    result = {"ok": False, "steps": []}
    page.bring_to_front()
    page.goto(GR_URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(1200)
    dump(page, "gr2-start")
    if "login" in page.url.lower():
        result["error"] = "gumroad login"
        return result

    try:
        page.get_by_text("Digital product", exact=False).first.click(timeout=4000)
        result["steps"].append("type=digital")
    except Exception as e:
        result["steps"].append(f"type={e}")

    name_ok = fill_labeled(page, "Name", PRODUCT_NAME)
    result["steps"].append(f"name={name_ok}")
    price_ok = fill_labeled(page, "Price", PRICE)
    result["steps"].append(f"price={price_ok}")
    dump(page, "gr2-named")

    try:
        page.get_by_role("button", name="Next: Customize").click(timeout=8000)
        result["steps"].append("clicked_next")
    except Exception as e:
        result["steps"].append(f"next={e}")
        return result

    page.wait_for_timeout(2500)
    try:
        page.wait_for_load_state("networkidle", timeout=20000)
    except Exception:
        pass
    dump(page, "gr2-customize")
    result["customize_url"] = page.url

    # Description: ProseMirror / textarea / contenteditable
    desc_ok = False
    for sel in (
        ".ProseMirror",
        "[contenteditable='true']",
        "div[role='textbox']",
        "textarea",
    ):
        try:
            loc = page.locator(sel).first
            if loc.count() == 0:
                continue
            loc.click(timeout=4000)
            page.keyboard.press("Control+A")
            page.keyboard.insert_text(GR_DESC)
            desc_ok = True
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
        files = page.locator("input[type='file']")
        n = files.count()
        log(f"gumroad file inputs: {n}")
        if n:
            files.first.set_input_files(covers, timeout=30000)
            img_ok = True
    except Exception as e:
        result["steps"].append(f"covers_err={e}")
    result["steps"].append(f"covers={img_ok}")

    # thumbnail if a second file input exists
    try:
        files = page.locator("input[type='file']")
        if files.count() >= 2:
            files.nth(1).set_input_files(str(GR_IMG / "thumbnail.jpg"))
            result["steps"].append("thumb=True")
    except Exception as e:
        result["steps"].append(f"thumb={e}")

    # Do not publish
    for name in ("Published", "Unpublished", "On profile"):
        try:
            loc = page.get_by_label(name)
            if loc.count() and name == "Published" and loc.first.is_checked():
                loc.first.uncheck()
                result["steps"].append("unpublished")
        except Exception:
            pass

    saved = False
    for name in ("Save changes", "Save", "Update"):
        try:
            btn = page.get_by_role("button", name=name, exact=True)
            if btn.count():
                btn.first.click(timeout=5000)
                saved = True
                result["steps"].append(f"save={name}")
                break
        except Exception:
            continue
    if not saved:
        result["steps"].append("save=False")

    page.wait_for_timeout(2000)
    dump(page, "gr2-after")
    result["url"] = page.url
    result["ok"] = name_ok and price_ok
    return result


def fill_superhive(page) -> dict:
    result = {"ok": False, "steps": []}
    page.bring_to_front()
    page.goto(SH_URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(1500)
    dump(page, "sh2-start")
    url = page.url.lower()
    if "login" in url or "/creator/" not in url:
        page.goto(SH_LOGIN, wait_until="domcontentloaded", timeout=60000)
        dump(page, "sh2-login")
        popup(
            "请登录 SuperHive",
            "Gumroad 已登录。\n\n请在这个 Chrome 窗口登录 SuperHive（邮箱/密码或 passkey）。\n"
            "登录成功后点确定，我会打开新建商品页并填写 $10 草稿。",
        )
        page.goto(SH_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(1500)
        dump(page, "sh2-after-login")
        if "login" in page.url.lower() or "/creator/" not in page.url:
            result["error"] = f"still not on creator form: {page.url}"
            return result

    # Dump form controls for debugging
    try:
        info = page.evaluate(
            """() => [...document.querySelectorAll('input,textarea,select,button,[contenteditable=true]')]
            .slice(0,80).map(e => ({
              tag: e.tagName, type: e.type, name: e.name, id: e.id,
              placeholder: e.placeholder, text: (e.innerText||'').slice(0,60)
            }))"""
        )
        (LOG / "sh2-controls.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
        log(f"superhive controls {len(info)}")
    except Exception as e:
        log(f"controls {e}")

    name_ok = fill_labeled(page, "Name", PRODUCT_NAME) or fill_labeled(page, "Title", PRODUCT_NAME)
    if not name_ok:
        try:
            page.locator("input[type='text']").first.fill(PRODUCT_NAME)
            name_ok = True
        except Exception as e:
            result["steps"].append(f"name_fallback={e}")
    result["steps"].append(f"name={name_ok}")

    price_ok = fill_labeled(page, "Price", PRICE)
    if not price_ok:
        try:
            page.locator("input[name*='price' i], input[id*='price' i]").first.fill(PRICE)
            price_ok = True
        except Exception as e:
            result["steps"].append(f"price_fallback={e}")
    result["steps"].append(f"price={price_ok}")

    about_ok = False
    for sel in ("[contenteditable='true']", "textarea", ".ProseMirror", "body#tinymce"):
        try:
            loc = page.locator(sel).first
            if loc.count() == 0:
                continue
            loc.click(timeout=3000)
            page.keyboard.press("Control+A")
            page.keyboard.insert_text(SH_ABOUT)
            about_ok = True
            break
        except Exception:
            continue
    for frame in page.frames:
        try:
            body = frame.locator("body#tinymce")
            if body.count():
                body.fill(SH_ABOUT)
                about_ok = True
                break
        except Exception:
            pass
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
        fi = page.locator("input[type='file']")
        if fi.count():
            fi.first.set_input_files(imgs, timeout=30000)
            img_ok = True
    except Exception as e:
        result["steps"].append(f"img_err={e}")
    result["steps"].append(f"images={img_ok}")

    saved = False
    for name in ("Save Draft", "Save as draft", "Save Product", "Save"):
        try:
            btn = page.get_by_role("button", name=name, exact=False)
            if btn.count():
                btn.first.click(timeout=5000)
                saved = True
                result["steps"].append(f"save={name}")
                break
        except Exception:
            continue
    result["steps"].append(f"save={saved}")
    page.wait_for_timeout(2000)
    dump(page, "sh2-after")
    result["url"] = page.url
    result["ok"] = bool(name_ok or price_ok or saved)
    return result


def main() -> None:
    LOG.mkdir(parents=True, exist_ok=True)
    log("launch v2")
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
            out["gumroad"] = fill_gumroad(page)
        except Exception:
            out["gumroad"] = {"ok": False, "error": traceback.format_exc()}
            dump(page, "gr2-error")
        sh_page = ctx.new_page()
        try:
            out["superhive"] = fill_superhive(sh_page)
        except Exception:
            out["superhive"] = {"ok": False, "error": traceback.format_exc()}
            dump(sh_page, "sh2-error")

        (ROOT / "fill-result-v2.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        log("done " + json.dumps(out, ensure_ascii=False)[:2000])
        popup(
            "填写结束",
            "Gumroad / SuperHive 草稿填写已尝试完成。\n请看 Chrome 里的页面确认。\n没有点发布。\n\n"
            + json.dumps(out, ensure_ascii=False)[:800],
        )
        time.sleep(15)
        ctx.close()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        tb = traceback.format_exc()
        Path(r"E:\Assets\marketplace-drafts\fill-error.txt").write_text(tb, encoding="utf-8")
        print(tb, flush=True)
        raise
