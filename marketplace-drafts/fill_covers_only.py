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
        files = page.locator("input[type='file']")
        n = files.count()
        log(f"file inputs {n}")
        files.nth(0).set_input_files(COVERS)
        log("covers set on input 0")
        page.wait_for_timeout(2000)
        if n >= 3:
            files.nth(2).set_input_files(THUMB)
            log("thumb set on input 2")
        page.wait_for_timeout(6000)
        dump(page, "gr5-after-upload")
        # Save without leaving if possible
        btn = page.get_by_role("button", name="Save and continue")
        if btn.count():
            btn.click()
            page.wait_for_timeout(2500)
        dump(page, "gr5-saved")
        ctx.close()


if __name__ == "__main__":
    main()
