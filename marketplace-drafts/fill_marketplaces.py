# -*- coding: utf-8 -*-
"""Open Chrome, wait for shop login, fill SuperHive + Gumroad drafts at $10. Do not publish."""
from __future__ import annotations

import json
import time
import traceback
from datetime import datetime
from pathlib import Path

from playwright.sync_api import TimeoutError as PwTimeout
from playwright.sync_api import sync_playwright

ROOT = Path(r"E:\Assets\marketplace-drafts")
LOG = ROOT / "browser-logs"
PROFILE = ROOT / "chrome-profile"
STATUS = ROOT / "browser-status.json"
SH_IMG = ROOT / "images" / "superhive"
GR_IMG = ROOT / "images" / "gumroad"
DOC = (ROOT / "DOCUMENTATION_ON_PAGE.md").read_text(encoding="utf-8")
# SuperHive docs field should not start with a markdown H1 heading token if the editor is rich text.
DOC_BODY = DOC.split("\n", 2)[-1].strip() if DOC.startswith("# ") else DOC

PRODUCT_NAME = "Blueish Assets — Complete Node Library (534 Groups)"
PRICE = "10"
SH_URL = "https://superhivemarket.com/creator/products/new"
GR_URL = "https://gumroad.com/products/new"

SH_ABOUT = """
<p><strong>534 reusable Blender assets</strong> in <strong>11 Asset Browser files</strong>: geometry-processing node groups, shader/material functions, compositor effects, a custom particle solver, geometry-nodes rigging, NPR materials, flipbook VFX, and stylized slash FX.</p>
<p>Drop the folder into Preferences → File Paths → Asset Libraries, open the Asset Browser, and drag a group onto a tree or object. No add-on install.</p>
<p>This is a toolbox, not a single generator. Geometry Nodes cover Laplacian-style deformation, heat geodesics, graph coloring, Voronoi fracture, packing, matrix math, and curve tools. Shading covers SDFs, tiling, fractals, parallax, and NPR. Simulation includes a force-based particle system plus LBS / DQS / CoR / Delta Mush skinning.</p>
<h3>Why buy this on SuperHive?</h3>
<p>A free GitHub copy of the same library exists:</p>
<ul>
<li>Files: <a href="https://github.com/blueish0930/Assets">https://github.com/blueish0930/Assets</a></li>
<li>Docs: <a href="https://blueish0930.github.io/Assets/">https://blueish0930.github.io/Assets/</a></li>
<li>Remote library (Blender 5.2+): <code>https://blender-assets.blueish.workers.dev</code></li>
</ul>
<p>If you only need to try nodes, use GitHub. A SuperHive purchase is for a packaged Asset Browser folder, product-page support, and to fund further nodes.</p>
<h3>What's included (scanned from the .blend files)</h3>
<ul>
<li>Geometry Nodes — 185 groups (mesh algorithms, packing, matrix math, curves)</li>
<li>Self Pruning + Spline Grammar — 4 groups</li>
<li>Particle System — 30 groups (solver, forces, trails, collisions)</li>
<li>Rigging — 15 groups (capture, deform, DQS, CoR, Delta Mush)</li>
<li>Material Functions — 49 (complex math, parallax, triplanar, normal blend)</li>
<li>Shader Tools — 161 (SDF, tiling, fractals, palettes)</li>
<li>Stylized NPR — 22 (cel, toon, hatch, hair, skin, …)</li>
<li>Compositor — 50 (ASCII, pixel sorting, rainy window, palettes, …)</li>
<li>Flipbook VFX — 12 (explosion, fire, smoke, water, ice, blood, dust, bubbles)</li>
<li>Slash FX — 6 stylized blade trails</li>
</ul>
<p><strong>Total: 534 catalog assets (519 node groups + 15 objects).</strong></p>
<h3>Requirements</h3>
<ul>
<li>Blender 5.3 recommended (two PCG files last saved as 5.2.35)</li>
<li>Cycles or EEVEE</li>
<li>Not compatible with Blender 4.x</li>
</ul>
<h3>Install</h3>
<ol>
<li>Unzip the product archive.</li>
<li>Edit → Preferences → File Paths → Asset Libraries → +</li>
<li>Select the folder that contains <code>blender_assets.cats.txt</code>.</li>
<li>Open an Asset Browser and choose Blueish Assets.</li>
<li>Drag a node group into a Geometry Nodes / Shader / Compositor tree, or drag Flipbook/Slash objects into the viewport.</li>
</ol>
<p>License: Royalty Free for films, games, and client work. Do not redistribute the zip or resell the node groups.</p>
""".strip()

GR_DESC = """# Blueish Assets

**534** Asset Browser assets in **11** `.blend` files: Geometry Nodes (mesh algorithms, packing, matrix math), shaders (SDF, tiling, fractals, parallax), compositor effects, a custom particle solver, GN rigging (LBS / DQS / CoR / Delta Mush), NPR materials, flipbook VFX, and 6 slash trails.

Add the unzipped folder as an Asset Library and drag. No add-on.

## Free on GitHub — paid here is support

The same library is public:

- https://github.com/blueish0930/Assets
- Docs: https://blueish0930.github.io/Assets/
- Remote library (Blender 5.2+): `https://blender-assets.blueish.workers.dev`

Clone it if you just want to try nodes. Buy this product if you want a packaged zip, product support, and to fund the next nodes.

## What's inside

- Geometry Nodes — 185
- Self Pruning / Spline Grammar — 4
- Particle System — 30
- Rigging — 15
- Material Functions — 49
- Shader Tools — 161
- NPR — 22
- Compositor — 50
- Flipbook VFX — 12
- Slash FX — 6
- **Total 534**

## Install

1. Unzip.
2. Blender → Edit → Preferences → File Paths → Asset Libraries → `+`.
3. Select the folder that contains `blender_assets.cats.txt`.
4. Open an Asset Browser and choose **Blueish Assets**.
5. Drag a node group into a Geometry Nodes / Shader / Compositor tree, or drag Flipbook/Slash objects into the viewport.

## Requirements

- Blender **5.3** (two PCG files last saved as 5.2.35)
- Cycles or EEVEE
- Not compatible with Blender 4.x

## License

Royalty-free for your films, games, and client work. Do not redistribute the zip or resell the node groups.

## Support

Gumroad message / SuperHive support / https://x.com/blueish0930 / https://space.bilibili.com/3546391456516604
"""

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


def dump_page(page, tag: str) -> None:
    LOG.mkdir(parents=True, exist_ok=True)
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in tag)[:80]
    try:
        page.screenshot(path=str(LOG / f"{safe}.png"), full_page=True, timeout=15000)
    except Exception as e:
        log(f"screenshot {tag}: {e}")
    try:
        (LOG / f"{safe}.html").write_text(page.content(), encoding="utf-8", errors="replace")
    except Exception as e:
        log(f"html {tag}: {e}")
    try:
        (LOG / f"{safe}.url.txt").write_text(f"{page.url}\n{page.title()}", encoding="utf-8")
    except Exception:
        pass


def looks_like_login(url: str, title: str = "") -> bool:
    u = (url or "").lower()
    t = (title or "").lower()
    keys = [
        "sign_in",
        "signin",
        "/login",
        "log-in",
        "blender-id",
        "blenderid",
        "oauth",
        "accounts.google",
        "users/sign",
        "session/new",
        "auth.",
    ]
    if any(k in u for k in keys):
        return True
    if "log in" in t or "sign in" in t or "login" in t:
        if "product" not in u:
            return True
    return False


def first_match(page, selectors, timeout=2500):
    for sel in selectors:
        try:
            loc = page.locator(sel).first
            if loc.count() == 0:
                continue
            loc.wait_for(state="visible", timeout=timeout)
            return loc
        except Exception:
            continue
    return None


def fill_first(page, selectors, value, timeout=2500) -> bool:
    loc = first_match(page, selectors, timeout=timeout)
    if not loc:
        return False
    try:
        loc.click(timeout=3000)
        loc.fill(value, timeout=5000)
        return True
    except Exception:
        try:
            loc.click(timeout=2000)
            page.keyboard.press("Control+A")
            page.keyboard.type(value, delay=10)
            return True
        except Exception as e:
            log(f"fill failed {selectors[0]}: {e}")
            return False


def click_text(page, texts, timeout=3000) -> bool:
    for t in texts:
        for role in ("button", "link", "tab"):
            try:
                loc = page.get_by_role(role, name=t, exact=False)
                if loc.count():
                    loc.first.click(timeout=timeout)
                    return True
            except Exception:
                pass
        try:
            loc = page.get_by_text(t, exact=False)
            if loc.count():
                loc.first.click(timeout=timeout)
                return True
        except Exception:
            pass
    return False


def fill_rich(page, html_or_text: str) -> bool:
    # contenteditable / ProseMirror / Trix / Quill
    for sel in [
        '[contenteditable="true"]',
        ".ProseMirror",
        ".ql-editor",
        ".trix-content",
        ".tox-edit-area",
        "div[role='textbox']",
    ]:
        try:
            loc = page.locator(sel).first
            if loc.count() == 0:
                continue
            loc.click(timeout=3000)
            page.keyboard.press("Control+A")
            page.keyboard.insert_text(html_or_text)
            return True
        except Exception:
            continue
    # TinyMCE iframe
    for frame in page.frames:
        try:
            body = frame.locator("body#tinymce, body[contenteditable='true']").first
            if body.count():
                body.click(timeout=2000)
                frame.page.keyboard.press("Control+A")
                body.fill(html_or_text)
                return True
        except Exception:
            continue
    # plain textarea named description
    return fill_first(
        page,
        [
            "textarea[name*='description' i]",
            "textarea[id*='description' i]",
            "textarea[name*='body' i]",
            "textarea",
        ],
        html_or_text,
    )


def set_files(page, selectors, files) -> bool:
    for sel in selectors:
        try:
            loc = page.locator(sel)
            n = loc.count()
            if n == 0:
                continue
            loc.first.set_input_files(files, timeout=20000)
            log(f"uploaded {len(files)} files via {sel}")
            return True
        except Exception as e:
            log(f"set_files {sel}: {e}")
    # hidden file inputs
    try:
        inputs = page.locator("input[type='file']")
        if inputs.count():
            inputs.first.set_input_files(files, timeout=20000)
            log(f"uploaded {len(files)} files via first file input")
            return True
    except Exception as e:
        log(f"file input: {e}")
    return False


def fill_superhive(page) -> dict:
    result = {"ok": False, "steps": []}
    page.bring_to_front()
    if "products/new" not in page.url:
        page.goto(SH_URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(1500)
    dump_page(page, "superhive-before")
    result["url"] = page.url

    if looks_like_login(page.url, page.title()):
        result["steps"].append("still_login")
        return result

    name_ok = fill_first(
        page,
        [
            "input[name*='name' i]",
            "input[id*='name' i]",
            "input[name*='title' i]",
            "input[id*='title' i]",
            "input[placeholder*='name' i]",
            "input[placeholder*='title' i]",
        ],
        PRODUCT_NAME,
    )
    result["steps"].append(f"name={name_ok}")

    # sometimes name is the only visible field until you continue
    click_text(page, ["Continue", "Next", "Add Imagery", "Save", "Create product"])

    price_ok = fill_first(
        page,
        [
            "input[name*='price' i]",
            "input[id*='price' i]",
            "input[placeholder*='price' i]",
            "input[inputmode='decimal']",
            "input[type='number']",
        ],
        PRICE,
    )
    result["steps"].append(f"price={price_ok}")

    about_ok = fill_rich(page, SH_ABOUT)
    result["steps"].append(f"about={about_ok}")

    # images
    sh_files = [
        str(SH_IMG / "01_featured.jpg"),
        str(SH_IMG / "02_geometry_nodes_demo.jpg"),
        str(SH_IMG / "03_all_node_thumbnails.jpg"),
        str(SH_IMG / "04_vfx_flipbook_slash.jpg"),
        str(SH_IMG / "05_full_node_inventory.jpg"),
    ]
    click_text(page, ["Add Imagery", "Add images", "Upload images", "Featured Image", "Gallery"])
    page.wait_for_timeout(800)
    img_ok = set_files(
        page,
        [
            "input[type='file'][accept*='image']",
            "input[type='file'][name*='image' i]",
            "input[type='file'][id*='image' i]",
            "input[type='file']",
        ],
        sh_files,
    )
    result["steps"].append(f"images={img_ok}")

    # documentation
    click_text(page, ["Documentation", "FAQs", "Docs"])
    page.wait_for_timeout(500)
    # try a second contenteditable (docs field)
    docs_ok = False
    try:
        editors = page.locator("[contenteditable='true'], textarea[name*='documentation' i], textarea[id*='documentation' i]")
        if editors.count() >= 2:
            editors.nth(1).click()
            page.keyboard.press("Control+A")
            page.keyboard.insert_text(DOC_BODY)
            docs_ok = True
        elif editors.count() == 1 and not about_ok:
            editors.first.click()
            page.keyboard.insert_text("\n\n" + DOC_BODY)
            docs_ok = True
        else:
            docs_ok = fill_first(
                page,
                [
                    "textarea[name*='documentation' i]",
                    "textarea[id*='documentation' i]",
                    "textarea[name*='doc' i]",
                ],
                DOC_BODY,
            )
    except Exception as e:
        result["steps"].append(f"docs_err={e}")
    result["steps"].append(f"docs={docs_ok}")

    # blender version / license guesses
    click_text(page, ["5.3", "Blender 5.3"])
    click_text(page, ["Royalty Free", "Royalty-Free"])
    click_text(page, ["Cycles", "EEVEE", "Eevee"])

    # SAVE DRAFT — never submit for review
    saved = click_text(
        page,
        ["Save Draft", "Save as draft", "Save Product", "Save", "Create Draft"],
    )
    result["steps"].append(f"save_draft={saved}")
    page.wait_for_timeout(2500)
    dump_page(page, "superhive-after")
    result["url_after"] = page.url
    result["ok"] = name_ok or price_ok or about_ok or saved
    return result


def fill_gumroad(page) -> dict:
    result = {"ok": False, "steps": []}
    page.bring_to_front()
    if "products/new" not in page.url and "/products/" not in page.url:
        page.goto(GR_URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(1500)
    dump_page(page, "gumroad-before")
    result["url"] = page.url
    if looks_like_login(page.url, page.title()):
        result["steps"].append("still_login")
        return result

    # type picker
    click_text(page, ["Digital product", "Digital download", "Digital"])
    page.wait_for_timeout(600)

    name_ok = fill_first(
        page,
        [
            "input[name='name']",
            "input[name*='name' i]",
            "input[placeholder*='name' i]",
            "input[placeholder*='Name']",
            "input[aria-label*='name' i]",
        ],
        PRODUCT_NAME,
    )
    result["steps"].append(f"name={name_ok}")

    click_text(page, ["Continue", "Next", "Create", "Add product"])
    page.wait_for_timeout(1000)

    price_ok = fill_first(
        page,
        [
            "input[name*='price' i]",
            "input[placeholder*='0' i]",
            "input[inputmode='decimal']",
            "input[type='text'][name*='amount' i]",
        ],
        PRICE,
    )
    if not price_ok:
        # Gumroad sometimes uses a Price button then an input
        click_text(page, ["Price", "$0", "$"])
        page.wait_for_timeout(400)
        price_ok = fill_first(page, ["input[type='text']", "input[inputmode='decimal']"], PRICE)
    result["steps"].append(f"price={price_ok}")

    click_text(page, ["Description", "Content"])
    desc_ok = fill_rich(page, GR_DESC)
    result["steps"].append(f"desc={desc_ok}")

    gr_files = [
        str(GR_IMG / "01_cover.jpg"),
        str(GR_IMG / "02_cover.jpg"),
        str(GR_IMG / "03_cover.jpg"),
        str(GR_IMG / "04_cover.jpg"),
        str(GR_IMG / "05_cover.jpg"),
    ]
    click_text(page, ["Upload images or videos", "Cover", "Add cover", "Upload images"])
    page.wait_for_timeout(500)
    img_ok = set_files(page, ["input[type='file']"], gr_files)
    result["steps"].append(f"covers={img_ok}")
    # thumbnail
    try:
        thumbs = page.locator("input[type='file']")
        if thumbs.count() >= 2:
            thumbs.nth(1).set_input_files(str(GR_IMG / "thumbnail.jpg"))
            result["steps"].append("thumbnail=True")
    except Exception as e:
        result["steps"].append(f"thumbnail={e}")

    # Do not publish: uncheck publish if present
    for label in ["Published", "Publish", "On profile", "Listed"]:
        try:
            box = page.get_by_label(label)
            if box.count():
                if box.first.is_checked():
                    box.first.uncheck()
                    result["steps"].append(f"unchecked_{label}")
        except Exception:
            pass

    saved = click_text(page, ["Save", "Save changes", "Update", "Create product", "Continue"])
    result["steps"].append(f"save={saved}")
    page.wait_for_timeout(2500)
    dump_page(page, "gumroad-after")
    result["url_after"] = page.url
    result["ok"] = name_ok or price_ok or desc_ok or saved
    return result


def wait_until_logged_in(page, kind: str, retries: int = 6) -> bool:
    target = SH_URL if kind == "superhive" else GR_URL
    for i in range(retries):
        try:
            page.goto(target, wait_until="domcontentloaded", timeout=45000)
        except Exception as e:
            log(f"{kind} goto retry: {e}")
        page.wait_for_timeout(800)
        url, title = page.url, page.title()
        log(f"{kind} url={url} title={title}")
        dump_page(page, f"{kind}-login-check-{i}")
        if kind == "superhive":
            if "/creator/" in url and not looks_like_login(url, title):
                return True
        if kind == "gumroad":
            if "gumroad.com" in url and not looks_like_login(url, title):
                return True
        if i < retries - 1:
            popup(
                "还需要登录",
                f"{kind} 还没进新建商品页。\n当前地址：{url}\n\n请在 Chrome 里登录，登录成功后点确定。",
            )
    url, title = page.url, page.title()
    if kind == "superhive":
        return "/creator/" in url and not looks_like_login(url, title)
    return "gumroad.com" in url and not looks_like_login(url, title)


def main() -> None:
    LOG.mkdir(parents=True, exist_ok=True)
    PROFILE.mkdir(parents=True, exist_ok=True)
    log("launching Chrome")
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE),
            channel="chrome",
            headless=False,
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check",
            ],
            ignore_default_args=["--enable-automation"],
            no_viewport=True,
        )
        # close leftover about:blank extras later
        sh = ctx.pages[0] if ctx.pages else ctx.new_page()
        gr = ctx.new_page()
        try:
            sh.goto(SH_URL, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            log(f"superhive goto: {e}")
        try:
            gr.goto(GR_URL, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            log(f"gumroad goto: {e}")
        dump_page(sh, "superhive-open")
        dump_page(gr, "gumroad-open")
        log(f"opened SH={sh.url} GR={gr.url}")

        popup(
            "请登录 SuperHive 和 Gumroad",
            "已经打开 Chrome。\n\n"
            "1. 在 SuperHive 标签页登录你的创作者账号\n"
            "2. 在 Gumroad 标签页登录你的账号\n"
            "3. 两个都进入新建商品页之后，回到这个对话框点「确定」\n\n"
            "我会填写商品信息，售价 $10，只保存草稿，不会点发布/Submit for Review。",
        )

        sh_ok = wait_until_logged_in(sh, "superhive")
        gr_ok = wait_until_logged_in(gr, "gumroad")
        log(f"login superhive={sh_ok} gumroad={gr_ok}")

        out = {"superhive": None, "gumroad": None}
        if sh_ok:
            try:
                out["superhive"] = fill_superhive(sh)
            except Exception:
                out["superhive"] = {"ok": False, "error": traceback.format_exc()}
                dump_page(sh, "superhive-error")
        else:
            out["superhive"] = {"ok": False, "error": "not logged in"}

        if gr_ok:
            try:
                out["gumroad"] = fill_gumroad(gr)
            except Exception:
                out["gumroad"] = {"ok": False, "error": traceback.format_exc()}
                dump_page(gr, "gumroad-error")
        else:
            out["gumroad"] = {"ok": False, "error": "not logged in"}

        (ROOT / "fill-result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        log("done " + json.dumps(out, ensure_ascii=False)[:1500])
        popup(
            "填写结束",
            "已经尝试填完两个后台。\n\n"
            f"SuperHive: {out['superhive']}\n\n"
            f"Gumroad: {out['gumroad']}\n\n"
            "Chrome 先留着，请你看一眼草稿。没有点发布。",
        )
        # keep browser open a bit so the user can inspect
        time.sleep(8)
        ctx.close()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        tb = traceback.format_exc()
        Path(r"E:\Assets\marketplace-drafts\fill-error.txt").write_text(tb, encoding="utf-8")
        print(tb, flush=True)
        raise
