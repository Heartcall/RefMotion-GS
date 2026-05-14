# Core Contribution Reduction

## Component Classification

| Component | Classification | Reason |
|---|---|---|
| Live mesh | ESSENTIAL TO IMPLEMENTATION | Needed for stable normals, evaluation, and UV baking. Not novel by itself because nvdiffrec, SuGaR, GeoSplatting, MILo, and GS-2M already use mesh outputs or mesh guidance. |
| Surface-bound 2D Gaussians | ESSENTIAL TO IMPLEMENTATION | A practical way to render and optimize surface samples. Not novel because 2DGS, PGSR, SuGaR variants, and TextureSplat already use surface-like primitives. |
| UV PBR atlas | OPTIONAL FOR FINAL SYSTEM | Important for the long-term asset story, but a risky first-paper burden. UV/PBR maps overlap with nvdiffrec, TexGaussian, TextureSplat, and possibly GS-2M. |
| Reflective-region reasoning | ESSENTIAL TO NOVELTY | The key decision is whether a pixel supervises surface texture or reflected radiance. This should be the core claim. |
| Far-field environment lighting | ESSENTIAL TO IMPLEMENTATION | Needed as a minimal specular renderer, but not novel. Use a fixed or low-capacity environment for MVP. |
| Near-field reflection field | REMOVE FROM FIRST PAPER | Heavy overlap with SpecTRe-GS and Ref-DGS. It also introduces cheating risk. Do not include unless the reduced signal fails without it. |
| Inter-reflection residual | REMOVE FROM FIRST PAPER | High complexity and strong overlap with Reflective GS, IRGS, SpecTRe-GS. It dilutes the story. |
| Reflection-consistency loss | ESSENTIAL TO NOVELTY | This is the only plausible core contribution if formulated rigorously and evaluated separately. |
| UV baking loss | ABLATION ONLY | Useful to measure specular leakage, but do not make it a main method until the normal/texture signal is proven. |
| Relighting/editing | REMOVE FROM FIRST PAPER | Evaluation and implementation burden. Current novelty is not relighting. Overclaiming editability will invite reviewer attack. |

## Minimal Paper Version

### One Core Technical Idea

[HYPOTHESIS]: Reflected image content follows a different multi-view motion model from surface texture. If a reflective-region observation is inconsistent with UV-stationary texture but consistent with a normal-induced reflected ray, it should supervise the surface normal and reflection residual, not the diffuse texture.

### Minimum Representation

Use:

1. A mesh initialized from 2DGS or PGSR.
2. Fixed UV unwrap.
3. A diffuse UV texture map.
4. A roughness or binary reflective mask, initially known in synthetic data and optionally predicted later.
5. A low-capacity far-field environment map or fixed synthetic environment.

Do not use:

- learned near-field reflection field in the first implementation,
- inter-reflection residual,
- metallic/specular PBR map optimization,
- material editing,
- relighting claims beyond a small sanity check.

### Minimum Loss

The minimum loss is not a full renderer. It is:

1. UV texture stationarity loss on non-reflective pixels.
2. Feature-space reflection-cycle consistency on reflective pixels.
3. Normal smoothness and mesh regularization.
4. Specular-leakage penalty on baked texture.

The proposed loss should be tested with ground-truth synthetic normals before optimizing geometry. First prove that the loss has a minimum near correct normals.

### Minimum Experiment

Synthetic Blender/Cycles scenes with:

- one glossy or mirror-like object,
- known mesh,
- known normals,
- known albedo and roughness,
- reflective mask,
- nearby colored reflector objects producing visible reflected motion,
- 20 to 80 calibrated views.

Compare:

- PGSR/2DGS mesh and texture baking,
- baseline UV texture baking with reflective pixels included,
- baseline baking with reflective mask excluded,
- proposed reflection-motion normal supervision plus gated texture baking.

Metrics:

- normal angular error in reflective regions,
- specular leakage into diffuse UV texture,
- mesh Chamfer or point-to-surface error,
- held-out view error restricted to reflective masks.

### Components Deferred to Future Work

Defer:

- near-field reflection field,
- inter-reflection residual,
- full PBR atlas,
- material editing,
- relighting,
- real in-the-wild scenes without ground truth,
- learned reflective-region prediction.

These are valuable only after the reflection-motion signal is proven.

## Reduced Claim

Do not claim:

"We reconstruct reflective objects with mesh, UV PBR materials, near-field reflection, inter-reflection, relighting, and editing."

Claim:

"For reflective object mesh and texture recovery, we show that reflection-induced multi-view motion can supervise normals and reduce specular leakage in UV texture baking, compared with photometric and mask-only baselines."

This claim is narrower, falsifiable, and easier to defend.
