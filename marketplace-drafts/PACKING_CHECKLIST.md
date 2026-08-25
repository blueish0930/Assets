# Pack before SuperHive review

SuperHive rejects on process, not on node quality. Fix these first.

## Will reject

1. **Default object names in `VFX/Slash/Slash_Master.blend`**
   - Current: `Blade_FX`, `Blade_FX.001`, `Blade_FX.002`, `Blade_FX.003`, `Blade_FX.004`, `Blade_FX.005`
   - SuperHive rule: `Cube.001` / `*.001` style names are not allowed.
   - Rename in English, for example:
     - `Slash_Fire`
     - `Slash_Blue`
     - `Slash_Green`
     - `Slash_Purple`
     - `Slash_Gold`
     - `Slash_Cyan`
   - Match the six real preview PNGs in `VFX/Slash/Thumbnails/`.
   - Re-mark as assets and regenerate thumbnails / listing.

2. **Catalog language**
   - `Material/平铺`, `Material/平铺/Tools`, `Material/平铺/平铺纹理`, `三渲二`
   - Product parts must be English.
   - Suggested:
     - `Material/Tiling`
     - `Material/Tiling/Tools`
     - `Material/Tiling/Patterns`
     - `Stylized NPR`

3. **Images**
   - Exactly **2:1**. Use the JPGs in `images/superhive/`.
   - Featured **JPG, &lt; 5 MB**.
   - Minimum **5** images, all ≥ 1200 px wide.
   - Do **not** use 1920×1080.
   - Do **not** put the Blender logo or the word “Blender” as a graphic overlay. UI screenshots of the product in use are fine; do not add extra Blender branding.

4. **Documentation**
   - Paste `DOCUMENTATION_ON_PAGE.md` into the SuperHive **Documentation** field.
   - A GitHub / docs.site link alone is **not** enough. Reviewers reject “docs are external”.

5. **Packed files**
   - `Compositor/Tex/` contains `Glitch.mp4`, `Puddle.mp4`, `RainDrop.png`.
   - Either pack them into `Compositor.blend` or keep that `Tex/` folder next to the blend with relative paths, then zip the whole tree.
   - Do not upload loose textures as separate product files.

6. **Zip / 7z only**
   - Single archive ≤ 5 GB (this pack is ~0.5 GB, fine).
   - Suggested name: `Blueish_Assets_v1.0.zip`

## Should fix (quality, not automatic reject)

| Issue | Where |
|---|---|
| 54 node groups have **no Asset Browser thumbnail** | See `INVENTORY.md` lines marked *(no thumbnail)* — many new GN mesh/math nodes, Self Pruning, Spline Grammar, some particle nodes |
| Typos in asset names | `Plexus Connnection`, `Spherical Sprial`, `Line Attaction Force`, `Barycentric Coodinate`, `Iterative Closet Point`, `Gaussain Blur`, `Mandelbort_V2`, `Regular_Octogon_SDF`, `Generate Paricles`, `Smooth Tesellation` |
| Folder typo | `RIgging_System` |
| GitHub is public | Listing already discloses this. Do not hide it. |

## Suggested zip layout

```
Blueish_Assets_v1.0/
  README.txt                 (install steps, English)
  blender_assets.cats.txt    (English catalog paths)
  Compositor/
  GN/
  Particle_System/
  Rigging_System/
  Shader/
  Stylized/
  VFX/
```

Keep `*_thumbnails/` folders. Blender Asset Browser needs them.

You can include `_v1/` + `_asset-library-meta.json` so Blender 5.2+ treats it as a proper library listing.

Do **not** ship `docs/Desktop/` screenshots or this `marketplace-drafts/` folder inside the customer zip.

## SuperHive submit flow

1. Creator Dashboard → Products → New Product.
2. Fill Primary Information from `SUPERHIVE_FORM.md`.
3. Add Imagery → upload the 5 SuperHive JPGs (featured first).
4. Categories / tags / version / license / zip.
5. Paste on-site documentation + FAQs.
6. Set publish date **≥ 14 days** from today.
7. **Save Draft**. Do not toggle Submit for Review until the Slash names and English catalogs are fixed.
8. Review takes 3–5 days after you submit.
