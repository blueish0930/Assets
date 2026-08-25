# Gumroad product form — DRAFT, do not publish

Dashboard: https://gumroad.com/payouts is the **payouts** page, not the product editor.

Create a product: Gumroad → **New product** → **Digital product**.
Save as draft. Do not flip the product to **published**.

Gumroad does not review listings the way SuperHive does, but keep the same English naming and packed zip.

---

## Product type

Digital product / digital download

## Name

```
Blueish Assets — Complete Blender Node Library (534 Groups)
```

## URL slug (suggestion)

```
blueish-assets
```

→ `https://gumroad.com/l/blueish-assets` (or your username path)

## Cover images (up to 8)

Gumroad: PNG/JPEG/GIF/MOV, recommended **≥ 1280×720 (16:9)**. Multiple covers should share the same height.

Upload in this order from `images/gumroad/`:

| # | File | Size | Source |
|---|---|---|---|
| 1 | `01_cover.jpg` | 2560×1440 | Real Asset Browser screenshot |
| 2 | `02_cover.jpg` | 2560×1440 | 3D Recursive Subdivision demo |
| 3 | `03_cover.jpg` | 2560×1440 | All real node thumbnails |
| 4 | `04_cover.jpg` | 2560×1440 | Flipbook + Slash renders |
| 5 | `05_cover.jpg` | 2560×1440 | Full node inventory |

## Thumbnail (Discover / library / profile)

```
images/gumroad/thumbnail.jpg
```

1200×1200 crop of the real Asset Browser Generation grid. Gumroad minimum is 600×600.

## Pricing

The zip is ~441 MB. **Gumroad free products are capped at 250 MB**, so this cannot be $0.

Recommended:

| Setting | Value |
|---|---|
| Type | Pay what you want |
| Minimum | **$5** |
| Suggested | **$19** |
| Currency | USD |

If you prefer a fixed price: **$19**.

SuperHive draft is $29. Gumroad can sit a bit lower (no SuperHive cut, no review delay). Do not go below $1.

## Description (Gumroad markdown — paste)

```markdown
# Blueish Assets

**534** Asset Browser assets in **11** `.blend` files: Geometry Nodes (mesh algorithms, packing, matrix math), shaders (SDF, tiling, fractals, parallax), compositor effects, a custom particle solver, GN rigging (LBS / DQS / CoR / Delta Mush), NPR materials, flipbook VFX, and 6 slash trails.

Add the unzipped folder as an Asset Library and drag. No add-on.

## Free on GitHub — paid here is support

The same library is public:

- https://github.com/blueish0930/Assets
- Docs: https://blueish0930.github.io/Assets/
- Remote library (Blender 5.2+): `https://blender-assets.blueish.workers.dev`

Clone it if you just want to try nodes. Buy this product if you want a packaged zip, product support, and to fund the next nodes.

## What's inside

| Module | File | Count |
|---|---|---:|
| Geometry Nodes | geometry_nodes_category_layout.blend | 185 |
| Self Pruning / Spline Grammar | Self_Pruning.blend, Spline_Grammar_v3.blend | 4 |
| Particle System | Particle_System_V3_EN.blend | 30 |
| Rigging | GN_Rigging_V3.blend | 15 |
| Material Functions | Material_Functions.blend | 49 |
| Shader Tools | Shader_Tools.blend | 161 |
| NPR | NPR_Shaders.blend | 22 |
| Compositor | Compositor.blend | 50 |
| Flipbook VFX | Flipbook.blend | 12 |
| Slash FX | Slash_Master.blend | 6 |
| **Total** | **11 files** | **534** |

### Geometry Nodes
Laplacian & mesh processing, heat geodesics, graph coloring / MIS / MST, Voronoi fracture, marching cubes, QEM simplification, circle/sphere packing, phyllotaxis, 3×3 matrix toolkit, PCA, RBF, linear solvers, catenary, Coons patch, IK, parallel transport.

### Shaders
51 SDF shapes, 46 tiling tools/patterns, 15 fractals, simplex noise, 5 parallax methods (POM, interior mapping), complex-number math, NPR toon/cel/hatch/hair/skin.

### Particles & rigging
Curl / vortex / spring / curve forces, children, trails, collisions. Skeleton from armature, bone capture/deform, DQS, Center of Rotation, Delta Mush.

### Compositor & VFX
ASCII, pixel sorting, rainy window, broken glass, palettes (viridis, inferno, …). Flipbooks: explosion, fire, smoke, water, ice, blood, dust, bubbles. Six stylized slash objects.

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

Gumroad message / SuperHive support / [X](https://x.com/blueish0930) / [Bilibili](https://space.bilibili.com/3546391456516604)

Full name list is in the product file `INVENTORY` (or the docs site).
```

## Call to action / summary (if the form has a short field)

```
534 Asset Browser node groups for Blender 5.3 — geometry, shaders, particles, rigging, NPR, compositor, VFX. Free on GitHub; buying here supports the project.
```

## Content / files to attach

Same zip as SuperHive: `Blueish_Assets_v1.0.zip`

Optional extra: a small `README.txt` and `INVENTORY.txt` inside the zip (English install + node list). Do not attach the 146 desktop screenshots.

Gumroad paid-product file cap is 20 GB. This pack is fine.

## Settings

| Field | Value |
|---|---|
| Discover | Off until you are ready (draft) |
| Community / comments | On |
| Limit quantity | No |
| Require shipping | No |
| Custom button | `Support & download` or `Buy the library` |
| Tags | blender, geometry nodes, shaders, npr, vfx, asset browser, procedural |
| Category | Design / 3D (closest Gumroad category) |

## Variants

Not required. If you mirror SuperHive:

- Personal — $19
- Studio — $49

PWYW with a $5 floor is simpler and matches “if you like it, support me”.

## Do not publish yet

Leave the product **unpublished / draft**. Gumroad goes live as soon as you publish — there is no review queue.

Fix Slash names (`Blade_FX.001` …) before you attach the zip, even on Gumroad, so both stores ship the same pack.
