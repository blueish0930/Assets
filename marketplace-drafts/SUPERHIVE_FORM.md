# SuperHive product form — DRAFT, do not submit yet

Paste these fields into **Creator Dashboard → Products → New Product**.
Product page language must be English.

Upload images from `images/superhive/` only (2:1 JPG).

---

## Primary Information

**Product name**

```
Blueish Assets — Complete Node Library (534 Groups)
```

**Short tagline** (if the form has a subtitle / one-liner)

```
Asset Browser library: Geometry Nodes, shaders, compositor, particles, GN rigging, NPR, flipbooks, and slash FX.
```

**About your product** (main description — paste into the rich-text editor)

Use headings, bullets, and bold. Do not rely on a screenshot of this file.

---

### About your product (paste)

**534 reusable Blender assets** in **11 Asset Browser files**: geometry-processing node groups, shader/material functions, compositor effects, a custom particle solver, geometry-nodes rigging, NPR materials, flipbook VFX, and stylized slash FX.

Drop the folder into Preferences → File Paths → Asset Libraries, open the Asset Browser, and drag a group onto a tree or object. No addon install.

This is a **toolbox**, not a single generator. The Geometry Nodes side covers Laplacian / ARAP-style deformation, heat geodesics, graph coloring, Voronoi fracture, packing, matrix math, and curve tools. The shading side covers SDFs, tiling, fractals, parallax, and NPR. The simulation side is a force-based particle system plus LBS / DQS / CoR / Delta Mush skinning nodes.

#### Why buy this on SuperHive?

A free GitHub copy of the same library exists:

- Code & files: https://github.com/blueish0930/Assets
- Node docs: https://blueish0930.github.io/Assets/
- Optional remote library (Blender 5.2+): `https://blender-assets.blueish.workers.dev`

If you only need to try nodes, use GitHub. A SuperHive purchase is for people who want:

1. A packaged Asset Browser folder plus **support** from the author
2. This product page as a stable install + inventory reference
3. To fund further nodes (self-pruning, spline grammar, solvers, VFX)

If the library helps you, buying here is the intended way to support it.

#### What's in the box (scanned from the .blend files)

| Module | File | Assets |
|---|---|---:|
| Geometry Nodes | `GN/geometry_nodes_category_layout.blend` | 185 |
| Self Pruning | `GN/Self_Pruning.blend` | 1 |
| Spline Grammar | `GN/Spline_Grammar_v3.blend` | 3 |
| Particle System | `Particle_System/Particle_System_V3_EN.blend` | 30 |
| Rigging System | `RIgging_System/GN_Rigging_V3.blend` | 15 |
| Material Functions | `Shader/Material_Functions.blend` | 49 |
| Shader Tools | `Shader/Shader_Tools.blend` | 161 |
| Stylized NPR | `Stylized/NPR_Shaders.blend` | 22 |
| Compositor | `Compositor/Compositor.blend` | 50 |
| Flipbook VFX | `VFX/Flipbook/Flipbook.blend` | 12 |
| Slash FX | `VFX/Slash/Slash_Master.blend` | 6 |
| **Total** | **11 files** | **534** |

Counts come from Blender's own asset listing (`_v1/assets-00000.json`): **519 node groups** and **15 objects**.

#### Geometry Nodes — 185 + PCG

Built as Asset Browser node groups (drag onto a Geometry Nodes tree).

**Mesh (68)** — Laplacian, QEM simplification, remesh, marching cubes/squares/triangles, heat geodesic, principal curvature, Voronoi fracture, mesh folding, detriangulate, edge collapse/flip/split, graph color / MIS / MST, UV seam, solidify, wireframe, skin, shrink-wrap packaging, reaction-diffusion, and more.

**Generation (34)** — circle / sphere packing, phyllotaxis, Koch, dragon fractal, maze, spirograph, tetrahedra, recursive subdivision, plexus, scatter, capsule, heart, helicoid.

**Math (43)** — 3×3 matrix toolkit (trace, norms, polar decomposition, pseudo-inverse, adjugate), PCA, RBF, dense/sparse linear solvers, gradient/divergence, Möbius, barycentric, ICP, FFT, cotangent Laplacian.

**Curve (23)** — catenary, Coons patch, loft, sweep, bevel, Boolean curve, IK, weave, even segments, curve intersections, hair-mesh-to-curve.

**Utility (17)** — camera culling, OBB, minimum bounding sphere, parallel transport, space colonization, debug, Voronoi relaxation.

**PCG** — Self Pruning; Spline Grammar + module-info helpers.

#### Shaders & material functions — 210

**Shader Tools (161)** — 51 SDF shapes, 15 fractals (Mandelbrot, Julia, Newton, …), 46 tiling generators/patterns, image filters, simplex noise, caustics, 19 palettes, boolean/index utilities.

**Material Functions (49)** — complex-number math (`cSine`, `cLn`, `cPower`, …), triplanar / matcap / spherical coordinates, five parallax methods (including POM and interior mapping), normal blending (RNM, UDN, White-Out, …), virtual cube/sphere/plane/cylinder intersections.

#### Stylized NPR — 22

Cel / toon shaders, hatch, halftone, anisotropic hair, skin, silk, metal, glass, water, wood, bark, crystal, painting, raymarching, line style, toon ocean.

#### Compositor — 50

**Effects (22)** — ASCII, pixel sorting, rainy window, frozen/broken glass, glitch, CRT, ordered dither, comic, cross-hatch, puddle, ripple, fire outline, scene transition, …

**Palettes (23)** — viridis, inferno, magma, plasma, twilight, toon ocean, cinematic ramps.

**Utilities** — vignette, flipbook, RGB→CMYK, texture sample, debug float.

#### Particle system — 30

Force-based GN solver: curl / bitangent / SDF noise, gravity, vortex, spring, orbit, curve and object forces, particle children, curve/particle trails, sphere/cube/custom masks, mesh velocity, collisions.

#### Rigging — 15

Skeleton from armature or edges, bone capture / deform, compress weights, Dual Quaternion (DQS) compensation, Center of Rotation, Delta Mush, joint mask, FK, skeleton sim, weight and rig visualizers.

#### VFX

- **Flipbook** objects: Blood, Bubble, Dust, Explosion, Fire, Ice, Smoke, Water, plus Flipbook / Frame Blend / Motion Vector node groups and a sprite render setup.
- **Slash FX**: 6 stylized blade-trail objects (rename `.001` suffixes before upload — see packing checklist).

#### Requirements

- Blender **5.3** recommended (most files saved as 5.3.8). `Self_Pruning.blend` and `Spline_Grammar_v3.blend` are 5.2.35.
- Cycles or EEVEE.
- GPU helps on the heavier mesh/math groups (geodesics, solvers, fracture).

#### Install (2 minutes)

1. Unzip `Blueish_Assets_v1.0`.
2. Blender → Edit → Preferences → File Paths → Asset Libraries → **+**.
3. Point it at the unzipped folder (the one that contains `blender_assets.cats.txt`).
4. Open an **Asset Browser** editor, set the library to **Blueish Assets**.
5. Drag a node group into a Geometry Nodes / Shader / Compositor tree, or drag Flipbook / Slash objects into the viewport.

Remote option (Blender 5.2+, same listing): Add Remote Asset Library → `https://blender-assets.blueish.workers.dev`

#### Support

- SuperHive product support on this page (I aim to reply within 72 hours).
- https://x.com/blueish0930
- https://space.bilibili.com/3546391456516604

The full per-node socket reference lives in **Documentation** below and on https://blueish0930.github.io/Assets/ — the on-site docs are enough to install and find every asset if the site is down.

---

## Featured Image & Gallery

Upload in this order. All files are **2:1 JPG**.

| Order | File | What it is | Notes |
|---|---|---|---|
| Featured | `images/superhive/01_featured.jpg` | Real Asset Browser, Generation catalog | JPG, 2560×1280, no extra branding overlay |
| 2 | `images/superhive/02_geometry_nodes_demo.jpg` | 3D Recursive Subdivision node in use | Real desktop screenshot |
| 3 | `images/superhive/03_all_node_thumbnails.jpg` | All real node thumbnails from the 11 blends | 3840×1920, still 2:1 |
| 4 | `images/superhive/04_vfx_flipbook_slash.jpg` | Real Flipbook + Slash product renders | From `VFX/*/Thumbnails` |
| 5 | `images/superhive/05_full_node_inventory.jpg` | Complete name list from the listing JSON | 3840×1920, 2:1 |

Do not add watermarks. Do not upload WebP. Do not upload 16:9.

## Demo Video, Categories & Tags

**Demo video:** none yet (optional). A 30–60s Asset Browser drag-and-drop clip would help; leave empty for this draft.

**Main category:** Modifier Setups

**Sub-categories (max 3):** Materials · FX · Scripts  
(If the form uses different labels: Surfacing / FX / Addons — pick the closest. One main + ≤3 subs.)

**Tags** (comma-separated, keep them accurate):

```
geometry-nodes, asset-browser, node-group, procedural, shader, compositor, npr, particle-system, rigging, vfx, flipbook, sdf, tiling, fractal, matrix
```

## Software Version, Files, Variations & License

**Blender version:** 5.3 (also tick 5.2 if the form allows multiple)

**Render engine:** Cycles, EEVEE

**Files:** `Blueish_Assets_v1.0.zip` (or `.7z`) — build only after the packing checklist is done.

**Variations / price (recommendation, change if you want):**

| Variation | Price USD | Who |
|---|---:|---|
| Personal | **29** | Individuals, hobby, students |
| Studio (optional) | **79** | Studios, multiple seats |

If you only want one price, use **$29** and no variations.

Because GitHub is free, do not set this at $80+ unless you add exclusive SuperHive-only content.

**License:** Royalty Free (standard SuperHive asset license).

This is an **asset product** (`.blend` node groups / objects), not a GPL addon. Do not mark it as an Extension.

## Documentation & FAQs

Paste the entire contents of `DOCUMENTATION_ON_PAGE.md` into the Documentation box.

**FAQs** (add as separate FAQ entries if the form supports them):

**Does this require an add-on?**
No. It is an Asset Browser library. Add the folder under Preferences → File Paths → Asset Libraries.

**Which Blender version?**
5.3 recommended. Two files (`Self_Pruning.blend`, `Spline_Grammar_v3.blend`) were last saved as 5.2.35. Older 4.x is not supported.

**Is this the same as the GitHub repo?**
Yes — the node library is also public at https://github.com/blueish0930/Assets. Buying on SuperHive supports development and includes product-page support. You are not paying for a secret exclusive pack unless a future update says otherwise.

**How do I use a node group?**
Open the Asset Browser, set the library to Blueish Assets, drag the group into a Geometry Nodes, Shader, or Compositor tree. Flipbook and Slash entries in Effect catalogs are objects — drag those into the 3D viewport.

**EEVEE or Cycles?**
Both. NPR and most shaders are EEVEE-friendly. Flipbooks are sprite cards. Heavy mesh/math groups are viewport-bound, not renderer-bound.

**Can I use this commercially?**
Yes under SuperHive Royalty Free: use in your jobs, games, films, and client work. Do not redistribute the raw `.blend` library or resell the node groups as your own product.

**Missing thumbnails?**
A subset of newer Geometry Nodes groups (solvers, geodesics, Self Pruning, Spline Grammar, some particle nodes) do not have preview images yet. They still appear by name in the catalog. Previews will be filled in an update.

**Support window?**
Reply target is 72 hours via SuperHive support. SuperHive’s product update window follows the site’s current 12-month policy.

## Collaborators & Dev-Fund

- Collaborators: none
- Blender Development Fund: optional; 5–10% is a nice default if you want it

## Publishing

- **Save Draft** only for now.
- When you actually submit: set the publish date **at least 14 days** ahead.
- Do **not** enable Submit for Review until Slash object names and English catalogs are fixed (`PACKING_CHECKLIST.md`).

## Gallery image alt text (if asked)

1. Asset Browser showing Blueish Generation node thumbnails and a remesh demo
2. Geometry Nodes demo: 3D Recursive Subdivision on a cube
3. Contact sheet of all real node-group thumbnails from the library
4. Flipbook explosion/fire/smoke/water and six slash FX renders
5. Complete 534-asset name inventory grouped by catalog
