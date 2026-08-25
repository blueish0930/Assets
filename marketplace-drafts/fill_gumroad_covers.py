# -*- coding: utf-8 -*-
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
GR_EDIT = "https://gumroad.com/products/jkglzv/edit"
COVERS = [
    str(ROOT / "images" / "gumroad" / f"{i:02d}_cover.jpg")
    for i in range(1, 6)
]
NAME = "Blueish Assets — Complete Node Library (534 Groups)"


def log(m):
    print(f"{datetime.now().isoformat(timespec='seconds')} {m}", flush=True)


def dump(page, tag):
    LOG.mkdir(exist_ok=True)
    page.screenshot(path=str(LOG / f"{tag}.png"), full_page=True, timeout=20000)
    (LOG / f"{tag}.url.txt").write_text(f"{page.url}\n{page.title()}", encoding="utf-8")
    log(f"dump {tag} {page.url}")


def main():
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
        page.goto(GR_EDIT, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(1500)
        dump(page, "gr4-open")

        # fix name
        try:
            page.get_by_label("Name").fill(NAME)
            log("name fixed")
        except Exception as e:
            log(f"name {e}")

        info = page.evaluate(
            """() => [...document.querySelectorAll('input[type=file]')].map((e,i) => ({
                i, accept: e.accept, name: e.name, id: e.id,
                cls: e.className, multiple: e.multiple,
                hidden: e.hidden || e.style.display === 'none',
                w: e.getBoundingClientRect().width
            }))"""
        )
        log("file inputs " + json.dumps(info))
        (LOG / "gr4-file-inputs.json").write_text(json.dumps(info, indent=2), encoding="utf-8")

        uploaded = False
        # Prefer the Cover dropzone: scroll it into view, then set files on nearby input
        try:
            page.get_by_text("Cover", exact=True).first.scroll_into_view_if_needed()
            page.wait_for_timeout(400)
        except Exception as e:
            log(f"scroll cover {e}")

        # Try every file input that accepts images or is empty-accept
        for i, item in enumerate(info):
            acc = (item.get("accept") or "").lower()
            if acc and ("image" not in acc and "video" not in acc and acc != "*"):
                log(f"skip input {i} accept={acc}")
                continue
            try:
                loc = page.locator("input[type='file']").nth(i)
                loc.set_input_files(COVERS, timeout=15000)
                log(f"uploaded via input {i} accept={acc!r}")
                uploaded = True
                break
            except Exception as e:
                log(f"input {i} failed: {e}")

        if not uploaded:
            try:
                with page.expect_file_chooser(timeout=10000) as fc:
                    page.locator("text=Upload images or videos").last.click()
                fc.value.set_files(COVERS)
                uploaded = True
                log("uploaded via last upload button")
            except Exception as e:
                log(f"last chooser {e}")

        page.wait_for_timeout(5000)
        dump(page, "gr4-covers")

        try:
            # stay unpublished: do NOT click Publish
            if page.get_by_role("button", name="Save and continue").count():
                page.get_by_role("button", name="Save and continue").click()
            elif page.get_by_role("button", name="Save changes").count():
                page.get_by_role("button", name="Save changes").click()
            log("saved")
        except Exception as e:
            log(f"save {e}")
        page.wait_for_timeout(2500)
        # go back to product tab if we landed on content
        if "/content" in page.url:
            try:
                page.get_by_role("link", name="Product").click()
                page.wait_for_timeout(1500)
            except Exception:
                page.goto(GR_EDIT, wait_until="domcontentloaded")
                page.wait_for_timeout(1500)
        dump(page, "gr4-final")
        (ROOT / "fill-result-v4.json").write_text(
            json.dumps({"uploaded": uploaded, "url": page.url, "inputs": info}, indent=2),
            encoding="utf-8",
        )
        time.sleep(8)
        ctx.close()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        tb = traceback.format_exc()
        print(tb, flush=True)
        Path(r"E:\Assets\marketplace-drafts\fill-error.txt").write_text(tb, encoding="utf-8")
        raise
