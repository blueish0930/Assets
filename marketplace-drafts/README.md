# Blueish Assets — marketplace drafts（先不要发布）

SuperHive / Gumroad 的商品草稿都在这个文件夹。
**没有登录你的店铺，也没有提交审核、没有上架。**

你给的两个链接是后台页（需要登录）：
- SuperHive 销售：https://superhivemarket.com/creator/sales
- Gumroad 结算：https://gumroad.com/payouts

请把文案复制进后台的 **Save Draft**，不要点 Submit / Publish。

## 中文操作顺序

1. 先看 `PACKING_CHECKLIST.md`：Slash 的 `Blade_FX.001`～`.005` 必须改成英文专名，分类 `平铺` / `三渲二` 改成英文，否则 SuperHive 会拒。
2. SuperHive 表单：`SUPERHIVE_FORM.md` + 站内文档 `DOCUMENTATION_ON_PAGE.md`
3. 上传 `images/superhive/` 里 5 张 **2:1 JPG**（不要用 1920×1080）
4. Gumroad 表单：`GUMROAD_FORM.md` + `images/gumroad/`（16:9 封面 + 1200 方图）
5. 两边都先存草稿。GitHub 免费版会在文案里写明，购买 = 支持作者 + 打包与售后。

## What was scanned

| | |
|---|---|
| Library name | **Blueish Assets** (`_asset-library-meta.json`) |
| Path | `E:\Assets\blender\assets` |
| Catalog assets | **534** (519 node groups + 15 objects) |
| Blend files | **11** (~441 MB listing, files dated 2026-07-05 → 2026-07-19) |
| Blender versions in files | 5.2.35 / 5.3.4 / 5.3.8 |
| Free GitHub | https://github.com/blueish0930/Assets |
| Docs site | https://blueish0930.github.io/Assets/ |
| Remote library (5.2+) | https://blender-assets.blueish.workers.dev |

## Files in this folder

| File | Use |
|---|---|
| `SUPERHIVE_FORM.md` | SuperHive product form, field by field, English (required) |
| `GUMROAD_FORM.md` | Gumroad product form |
| `DOCUMENTATION_ON_PAGE.md` | On-site documentation to paste (SuperHive rejects GitHub-only docs) |
| `INVENTORY.md` | Full node list generated from the official listing JSON |
| `PACKING_CHECKLIST.md` | Fixes required **before** you hit Submit for Review |
| `images/superhive/` | 5 images, **2:1**, ≥2560×1280, JPG — SuperHive gallery |
| `images/gumroad/` | 5× 16:9 covers + 1200×1200 thumbnail |
| `build_listing_images.py` | Regenerates images from real thumbs/screenshots |

## Images (real sources only — no AI art)

| # | SuperHive file | Source |
|---|---|---|
| 1 Featured | `01_featured.jpg` | Your real desktop screenshot of the Asset Browser (Generation catalog) |
| 2 | `02_geometry_nodes_demo.jpg` | Real screenshot: 3D Recursive Subdivision node in use |
| 3 | `03_all_node_thumbnails.jpg` | Every real Asset Browser thumbnail from the 11 .blend files |
| 4 | `04_vfx_flipbook_slash.jpg` | Real Flipbook + Slash product PNGs already in the library |
| 5 | `05_full_node_inventory.jpg` | Full node names from `_v1/assets-00000.json` |

All SuperHive images are **2:1**. Featured is JPG. Do **not** upload 1920×1080 (wrong ratio — #1 rejection reason).

## Why these are drafts, not live products

1. SuperHive and Gumroad creator dashboards need **your login**. The URLs you sent (`/creator/sales`, `/payouts`) are account pages, not public product editors. I did not log in and did not submit anything.
2. SuperHive will **reject** the Slash objects named `Blade_FX.001` … `Blade_FX.005` (default Blender naming).
3. Catalog paths `Material/平铺` and `三渲二` should be English before review.
4. SuperHive requires a publish date **at least 2 weeks** in the future.

Fix the checklist, then paste the form. Do not toggle **Submit for Review** until the pack is clean.
