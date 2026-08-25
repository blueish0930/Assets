# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(r"E:\Assets\marketplace-drafts")
LOG = ROOT / "browser-logs"
PROFILE = ROOT / "chrome-profile"
GR_EDIT = "https://gumroad.com/products/jkglzv/edit"
COVERS = [str(ROOT / "images" / "gumroad" / f"{i:02d}_cover.jpg") for i in range(1, 6)]
THUMB = str(ROOT / "images" / "gumroad" / "thumbnail.jpg")
GR_PLAIN = Path(r"E:\Assets\marketplace-drafts\fill_v3.py").read_text(encoding="utf-8")
# extract GR_PLAIN from fill_v3
import re
m = re.search(r'GR_PLAIN = """(.*?)"""', GR_PLAIN, re.S)
TEXT = m.group(1).strip() if m else "Blueish Assets — 534 node groups. $10."


def log(m):
    print(f"{datetime.now().isoformat(timespec='seconds')} {m}", flush=True)


def dump(page, tag):
    LOG.mkdir(exist_ok=True)
    page.screenshot(path=str(LOG / f"{tag}.png"), full_page=True, timeout=20000)
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

        # restore description as text
        ed = page.locator("[contenteditable='true'], .ProseMirror").first
        ed.click()
        page.keyboard.press("Control+A")
        page.keyboard.insert_text(TEXT)
        log("description restored")
        page.wait_for_timeout(500)

        # Cover: open picker then Computer files
        page.locator("text=Cover").first.scroll_into_view_if_needed()
        page.wait_for_timeout(400)
        dumped = False
        try:
            # If submenu already open
            if page.get_by_text("Computer files").count():
                with page.expect_file_chooser(timeout=8000) as fc:
                    page.get_by_text("Computer files").first.click()
                fc.value.set_files(COVERS)
                log("covers via existing Computer files")
                dumped = True
        except Exception as e:
            log(f"existing submenu {e}")
        if not dumped:
            try:
                page.get_by_text("Upload images or videos").first.click()
                page.wait_for_timeout(600)
                with page.expect_file_chooser(timeout=8000) as fc:
                    page.get_by_text("Computer files").first.click()
                fc.value.set_files(COVERS)
                log("covers via Cover > Computer files")
                dumped = True
            except Exception as e:
                log(f"cover flow {e}")
        page.wait_for_timeout(5000)
        dump(page, "gr6-covers")

        # Thumbnail
        try:
            page.get_by_text("Thumbnail").first.scroll_into_view_if_needed()
            page.wait_for_timeout(300)
            with page.expect_file_chooser(timeout=8000) as fc:
                page.locator("text=Thumbnail").locator("xpath=ancestor::div[1]").get_by_text("Upload").first.click()
            fc.value.set_files(THUMB)
            log("thumb uploaded")
        except Exception as e:
            log(f"thumb {e}")
            try:
                with page.expect_file_chooser(timeout=8000) as fc:
                    page.get_by_role("button", name="Upload").last.click()
                fc.value.set_files(THUMB)
                log("thumb via last Upload")
            except Exception as e2:
                log(f"thumb2 {e2}")
        page.wait_for_timeout(4000)
        dump(page, "gr6-thumb")

        if page.get_by_role("button", name="Save and continue").count():
            page.get_by_role("button", name="Save and continue").click()
            page.wait_for_timeout(2500)
        dump(page, "gr6-final")
        ctx.close()


if __name__ == "__main__":
    main()
