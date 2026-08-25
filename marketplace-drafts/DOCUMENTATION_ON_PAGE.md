# Documentation (paste into SuperHive Documentation field)

Blueish Assets is an Asset Browser library. It is not an add-on. After you add the unzipped folder as a library, every node group and VFX object below is drag-and-drop.

Online socket-level reference (optional extra, the lists here are complete): https://blueish0930.github.io/Assets/

Free source repository: https://github.com/blueish0930/Assets

---

## 1. Install

1. Unzip the product archive. You should see `blender_assets.cats.txt` next to folders named `GN`, `Shader`, `Compositor`, `Particle_System`, `RIgging_System`, `Stylized`, `VFX`.
2. In Blender: **Edit → Preferences → File Paths → Asset Libraries**.
3. Click **+** → **Add Asset Library** and choose that unzipped folder.
4. Name it `Blueish Assets` (or leave the default).
5. Open an **Asset Browser** editor. In the library dropdown (top-left of that editor), pick **Blueish Assets**.
6. Catalogs appear in the left sidebar: Geometry Node, Material, Compositor, Particle System, Rigging System, Stylized NPR, Effect.

### Remote library (optional, Blender 5.2+)

If you prefer on-demand download instead of the zip:

1. Preferences → File Paths → Asset Libraries → **Add Remote Asset Library**
2. URL: `https://blender-assets.blueish.workers.dev`

The remote listing is the same 534 assets / 11 files.

---

## 2. How to use

### Node groups (almost everything)

1. Open a **Geometry Nodes**, **Shader**, or **Compositor** editor.
2. In the Asset Browser, select the matching catalog.
3. Drag the asset onto the node tree (or into the empty editor).
4. Connect Geometry / Shader / Color sockets as you would with any group.

Geometry node groups expect a Geometry Nodes modifier. Shader groups belong in a material. Compositor groups belong in the Compositor.

### Flipbook and Slash objects

These live under **Effect / Flipbook** and **Effect / Slash**. Drag from the Asset Browser into the **3D Viewport**. They are objects with the effect already set up, not node groups (except the Flipbook / Frame Blend / Motion Vector groups).

### Append instead of Asset Browser

File → Append → pick the `.blend` → NodeTree (or Object) → the group name. Works, but the Asset Browser is the intended path.

---

## 3. Requirements

- Blender **5.3** (files saved as 5.3.4 / 5.3.8). `Self_Pruning.blend` and `Spline_Grammar_v3.blend` last saved as **5.2.35**.
- Windows / macOS / Linux.
- Cycles or EEVEE.
- Some mesh/math groups (heat geodesic, linear solvers, fracture, marching cubes) are heavier. Use them on a duplicate, not on a 2-million-face production mesh first.

---

## 4. File map

| Path | Contents | Count |
|---|---|---:|
| `GN/geometry_nodes_category_layout.blend` | Mesh / curve / math / generation / utility groups | 185 |
| `GN/Self_Pruning.blend` | Self Pruning | 1 |
| `GN/Spline_Grammar_v3.blend` | Spline Grammar + module info | 3 |
| `Particle_System/Particle_System_V3_EN.blend` | Solver, forces, trails, masks | 30 |
| `RIgging_System/GN_Rigging_V3.blend` | Capture, deform, DQS, CoR, Delta Mush | 15 |
| `Shader/Material_Functions.blend` | Complex math, coordinates, parallax, utilities | 49 |
| `Shader/Shader_Tools.blend` | SDF, tiling, fractal, image, texture, palettes | 161 |
| `Stylized/NPR_Shaders.blend` | Toon / cel / hatch / material presets | 22 |
| `Compositor/Compositor.blend` | Effects, palettes, utilities | 50 |
| `VFX/Flipbook/Flipbook.blend` | Flipbook objects + player groups | 12 |
| `VFX/Slash/Slash_Master.blend` | Six slash objects | 6 |

Total: **534** catalog assets (519 node groups + 15 objects).

---

## 5. Complete node list

Names below are the Asset Browser names from the scanned library.

### Geometry Node / Mesh (68)

2D Medial Axis, 2D Remesh, 2D Straight Skeleton, Auto UV Seam, Bend, Circular Parameterization, Collision Detection, Cube Deform, Curvature, Detriangulate, Discrete Panelization, Edge Collapse, Edge Flip, Edge Loop ID, Edge Loop Selection, Edge Ring ID, Edge Split, Edges of Face, Edges to Road, Elastic Sphere, Face Extrusion, Face Loop Selection, Face Stripes Group, Faces of Edge, Faces of Vertex, Graph Color, Graph MIS, Heat Geodesic, Insert Face, Laplacian, Loop Subdivision, Marching Cube, Marching Square, Marching Triangle, Measure Centroid, Measure Volume, Mesh Ambient Occlusion, Mesh Folding, Mesh Puzzle, Mesh SDF, Mesh Thickness, Minimum Spanning Tree, Outline, Path Deform, Poly Cut, Principal Curvature, QEM Mesh Simplification, Reaction Diffusion, Recalculate Face Normals, Remesh, Sharpen Mesh, Shrink Wrap Packaging, Skin Modifier, Smooth Tesellation, Solidify, Spherical Parameterization, Split Points, Stretch, Surface Deform, Taper, Tessellation, Twist, Vertices of Face, Volume Path, Voronoi Fracture, Wire Deform, Wireframe, World Tangent

### Geometry Node / Generation (34)

10-Tetrahetra, 3D Recursive Subdivision, 5-Tetrahetra, Capsule, Cardioid, Circle Packing, Circular Packing, Coordinate System, Custom Voronoi Texture, Dragon Fractal, Heart, Helicoidal Surface, Hexagon, Homogeneous Disk, Homogeneous Sphere, Image to ASCII, Koch Line, Koch Snowflake, Line Drawing, Maze Generation, N Joint, Nearest Point Connection, Ordered Dithering, Phyllotaxis Disk, Phyllotaxis Sphere, Plexus Connnection, Random Points, Recursive Cube Packing, Recursive Subdivision, Scatter, Sketch, Spherical Sprial, Spirograph, Triangle

### Geometry Node / Math (43)

3 Planes Intersection Point, 3D Incircle, 3x3 1-Norm, 3x3 Adjugate Matrix, 3x3 Diag, 3x3 Diagonalize Symmetric, 3x3 Frobenius Norm, 3x3 Infinity-Norm, 3x3 Matrix Trace, 3x3 Max-Norm, 3x3 Polar Decomposition, 3x3 Pseudo-Inverse, 3x3 Spectral-Norm, Barycentric Coodinate, CircumSphere, Closest Point Pair, Cotangent Laplacian, Cross to Matrix, Dense Linear Solver, Dihedral, Divergence, Extract Transform, Fourier Transform, Gradient, InSphere, Iterative Closet Point, Matrices Multiply, Matrix Add, Matrix Scale, Matrix to Vectors, Mobius Transform, Normal Distribution, Outerproduct, PCA, Project to Tangent Plane, Quaternion to Matrix, RBF Interpolate, Sample Bary-Coord, Slerp, Sparse Linear Solver, Sphere Intersections, Store Bary-Coord, Vectors to Matrix

### Geometry Node / Curve (23)

2D Curve Point Info, Bevel 2D Curve, Boolean Curve, Catenary, Consistent Curve Orientation, Coons Patch, Curve Constrained Sphere Packing, Curve Instance Packing, Curve Intersections, Curve Loop Edge, Curve Rolling, Dash Line, Edge Bundling, Even Curve Segments, Fill 3D Curve, Hair Mesh to Curve, Inverse Kinematics, Loft Curve, Phyllotaxis Profile Surface, Ribbon Render, Sweep, Twist Curve, Weave Curve

### Geometry Node / Utility (17)

Attribute Delete, Camera Culling, Cluster Points, Debug, Delete By Age, Find All Cells, Fourier Transform Drawing, Match Size, Minimum Bounding Sphere, Order in Field, Oriented Bounding Box, Parallel Transport, Space Colonization, Toon Node, Visualize Epicycles, Visualize UVMap, Voronoi Relaxation

### Advanced / PCG (4)

Self Pruning, Spline Grammar, Combine Module Infos, Module Info Piece

### Particle System (30)

**Forces:** Bitangent Noise, Cone Direction, Curl Noise Force, Curve Force, Drag, Gravity Force, Limit Force, Line Attaction Force, Mesh Velocity, Object Force, Orbit Force, Point Attraction Force, Signed Distance Noise, Spring Force, Vortex Force

**Info:** Curve Info, Particle Attribute, Particle Info

**Masks:** Cube Mask, Custom Mask, Sphere Mask

**System:** Curve Trail, Generate Paricles, Initialize Particles, Particle Children, Particle Collision, Particle Solver, Particle Trail, Render Particles, Surface Collision

How to use: start from **Particle Solver** / **Initialize Particles** / **Generate Paricles**, then stack Force groups and a **Render Particles** (or trail) output.

### Rigging System (15)

Bone Capture, Bone Deform, Compress Bone Weights, Compute CoR, DQS Compensation, Delta Mush, Detect Error, Joint Mask, Recompute Transform, Rig Forward Kinematic, Skeleton Sim, Skeleton from Armature, Skeleton from Edges, Visualize Bone Weight, Visualize Rig

Typical path: **Skeleton from Armature** → **Bone Capture** → **Bone Deform**, then optional **DQS Compensation**, **Compute CoR**, or **Delta Mush**.

### Material Functions (49)

**cMath:** cCosh, cCosine, cDivide, cExponent, cLn(x), cLog(x), cMultiply, cPower, cSine, cSinh, cSquare Root, cTangent

**Coordinates:** Cartesian to Spherical, Coordinate Detect, Flipbook, Matcap v1, Matcap v2, Scatter Coordinate, Spherical to Cartesian, Swirl Coordinate, Triplaner, Triplaner Pro

**Functions:** Billboard, Blend Normal (Angle / Euler / RNM / UDN / White-Out), Bump to Normal, Camera Facing Vector, Camera Location, Casted Plane Transparent, Create Third Orthographic Vector, Derive Normal Z, Inverse Transform Matrix, Object Transform, Quadratic Equation, Tangent to World, Virtual Cube / Cylinder / Plane / Sphere, World to Tangent, is Casted to Plane

**Parallax:** Interior Mapping, Parallax Mapping, Parallax Occlusion Mapping, Relief Parallax Mapping, Steep Parallax Mapping

### Shader Tools (161)

**Fractal (15):** Barnsley_Tree, Butterfly_fractal, Cubic_Julia, Julia_Set, Julia_Sine, Lambda_Fractal, Mandelbort_V2, Mandelbrot, Marek_Dragon, Newton_Fractal, Phoenix_Julia, Sinh_Fractal, Spiral_Septagon_Fractal, iabs_Fractal, iabs_Fractal_V2

**Image (10):** 3x3 Convolution, Box Blur, Circular Blur, Droste_Zoom, Gaussain Blur, Image_Rotation, LED_Screen, Radial Blur, Scatter_Image, Seamless_Image

**Shape / SDF (51):** Arc_SDF, Bezier_SDF, Bezier(Low)_SDF, Blobby_Cross_SDF, Box_SDF, Circle, Circle_Wave_SDF, Cool_S_SDF, Cross_SDF, Curved_Polygon, Cut_Disk_SDF, Egg_SDF, Ellipse_SDF, Equilateral_Triangle_SDF, Fonts_SDF, Heart_SDF, Hexagram_SDF, HorseShoe_SDF, Isosceles_Trapezoid_SDF, Isosceles_Triangle_SDF, Lemon_Piece, Moon_SDF, N_Polygon_SDF, Parabola_SDF, Parabola_Segment_SDF, Parallelogram_SDF, Pie_SDF, Polygon_SDF, Quadratic_Circle_SDF, Regular_Hexagon_SDF, Regular_Octogon_SDF, Regular_Pentagon_SDF, Regular_Star_SDF, Rhombus, Rhombus_SDF, Ring, Ring_SDF, Rounded_Box_SDF, Rounded_Cross_SDF, Rounded_X_SDF, SDF_Viewer, Segment_SDF, Smile, Square, Stair_SDF, Star_SDF, Triangle_SDF, Tunnel_SDF, Uneven_Capsule_SDF, Vesica_SDF, Yin&Yang

**Texture (12):** 3D Simplex Noise, 4D Simplex Noise, AO-Edge, Caustics, Color_Variation, Macro_Variation, Radial-Noise, Radial-Segments, Radial-Voronoi, Scratch, Tileable_Water_Caustic, Water_Stain

**Utility (27):** Boolean(Custom), Index_Switch, Integer(Custom), Palette1–Palette19, Render_Mask, Scene_Time(Custom), Switch_Multi_Images, Switch_Multi_UVs, Time_Falloff

**Tiling tools (5):** Circular_Tiling, Hexagon_Tile, Simple_Tile, Tile_Generator(3x3), Tile_Generator(5x5)

**Tiling patterns (41):** (2D)Recursive_Subdivision, (3D)Recursive_Subdivision, Candy_Tile, Checker_Pro+, Circle_And_Square_Tile, Cube_Pattern_Tile, Diamond_Corner_Tile, Diamond_Tile, Fiber_Tile, FlagStone_Tile, Floor_Brick_Tile, Floor_Brick_Tile_V2, Herringbone_Pattern, Hexagon, Metal_Floor_Tile1, Metal_Floor_Tile2, Ornament_Tile, Ornament_Tile2–7, Paisley_Tile, Pattern_Tile1, Paving_Block_Tiles, Random_Tile_Pattern, Ring_Tiling, Roof_Tile, Scale_Tile, Scale_Tile_V2, Six_Hex_Tile, Square_Tile, Square_Triangle_Tile, Tangled_Square_Tile, Tile1, Tile2, Triangle, Truchet_Tile, Weave, Wicker

### Stylized NPR (22)

Bark, Cel Shader, Cross Hatch, Crystal, Glass, Hair, Hair Anisotropy, Half Tone, Line Style, Metal, Painting, Raymarching, Scratch, Shading Models, Silk, Skin, Toon Node, Toon Ocean, Toon Shader, Voronoi Star, Water, Wood

### Compositor (50)

**Effect (22):** ASCII, Broken Glass, CRT, Comic, Cross Hatching, Dither Dot, Fire Outline, Frozen Glass, Glitch, HackWave, Noise, Ordered Dithering, Outline Edge, Pixel Sorting, Puddle, Rainy Window, Ripple, Scene Transition, Shifting Color, Stylized Dither, Underwater, Warning Glitch

**Palette (23):** Autumn, Blues, Cividis, Cool, Coolwarm, GnBu, Hot, Inferno, Jet, Magma, Ocean, PiYG, Plasma, Purple Sunset, Rainbow, RdYlBu, Spectral, Sunset, Toon Ocean, Twilight, Twilight_shifted, Viridis, YlGnBu

**Utilities (5):** Debug Float, Flipbook, RGB To CMYK, Texture Sample, Vignette

Enable Use Nodes in the Compositor, then drag a group onto the tree and plug Image/Scene through it.

### Effect / Flipbook (12)

Objects: Blood, Bubble, Dust, Explosion, Fire, Ice, Smoke, Water, Sprite Render Setup

Node groups: Flipbook, Frame Blend Flipbook, Motion Vector Flipbook

### Effect / Slash (6)

Blade_FX plus five variants. Rename the `.001`–`.005` copies to unique English names before SuperHive review (see packing checklist).

---

## 6. Troubleshooting

**Library is empty**
The folder you added must be the one that contains `blender_assets.cats.txt`, not a parent `Assets` repo root.

**Pink / missing textures on compositor glitch / puddle / rain**
Keep `Compositor/Tex/` next to `Compositor.blend` (`Glitch.mp4`, `Puddle.mp4`, `RainDrop.png`), or File → External Data → Pack Resources.

**Node group has no preview icon**
54 groups currently have no thumbnail (mostly newer mesh/math, Self Pruning, Spline Grammar, a few particle nodes). Search the Asset Browser by name. They still work.

**Blender 4.x**
Not supported. Groups use 5.x sockets (including bundles on some matrix nodes).

**Performance**
Heat Geodesic, linear solvers, marching cubes, Voronoi fracture, and the particle solver are the heavy ones. Disable the modifier in the viewport while editing, or lower iterations/resolution first.

---

## 7. License (when bought on SuperHive / Gumroad)

Royalty Free for the purchased copy: use in commercial and personal projects. Do not re-upload the library, do not resell the node groups as a competing asset pack, and do not share the zip.

The GitHub repository may use a different (public) license — that applies only to files you clone from GitHub, not to this paid zip.
