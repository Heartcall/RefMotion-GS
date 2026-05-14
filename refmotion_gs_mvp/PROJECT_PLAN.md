# RefMotion-GS MVP Project Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use planning, executing-plans, test-driven-development, systematic-debugging, code-review, and verification-before-completion workflows while implementing this plan task-by-task.

**Goal:** Test whether reflection-induced multi-view motion is a useful supervision signal for reflective-region normals and UV texture recovery.

**Architecture:** The MVP uses a synthetic, calibrated testbed with known geometry and controlled normal perturbations. It implements Formulation A from `outputs/phase2/theory_rewrite.md`: feature-space reflection-cycle consistency with geometric reflected-ray matching, no learned near-field reflection field, and no full RefTex-GS system.

**Tech Stack:** Python, NumPy, PyTest, Matplotlib/Pillow for diagnostics. Blender/Cycles is preferred for rendering but the current environment has no `blender` executable on `PATH`, so Milestone 1 starts with the allowed analytic synthetic renderer fallback.

---

## 1. Restated Reduced Hypothesis

Reflection-induced multi-view motion provides a useful supervision signal for reflective-region normals and reduces specular leakage during UV texture recovery.

The defensible core is not mesh-bound Gaussians, UV atlases, PBR maps, relighting, or near-field reflection rendering. The core test is whether reflected-ray geometry creates measurable evidence beyond photometric texture stationarity and mask-only exclusion.

## 2. What Will Be Implemented

1. A deterministic synthetic scene generator with calibrated views, a glossy curved object, colored reflected objects, ground-truth surface normals, ground-truth albedo, roughness or reflective mask, and camera intrinsics/extrinsics.
2. Camera geometry: ray generation, projection, unprojection, surface-ray intersection for the analytic scene, and convention tests.
3. Reflection geometry: outgoing view directions, reflection directions, Pluecker line representation, reflected-ray distance, and cross-view candidate matching.
4. Formulation A diagnostic loss: feature-space reflection-cycle consistency using frozen image/RGB-derived features and reflected-ray candidate weights.
5. Controlled normal perturbation tests: ground truth, 1 degree, 3 degree, 5 degree, 10 degree, and smooth random perturbation.
6. Normal-only optimization over normal offsets or tangent-space normal parameters, without optimizing mesh vertices first.
7. UV-like texture baking and leakage metrics: all-pixel baking, oracle reflective-mask exclusion, noisy mask-only baking, reflection-cycle confidence routing, and normal-refinement plus routing.
8. Reproducible metrics and plots under `refmotion_gs_mvp/outputs/`.

## 3. What Will Explicitly Not Be Implemented

1. Full RefTex-GS.
2. Learned near-field reflection fields.
3. Inter-reflection residuals.
4. Full PBR optimization.
5. Material editing or relighting claims.
6. Mesh-bound Gaussians as a novelty claim.
7. UV texture maps or PBR maps as the main novelty claim.
8. Any claim of broad real-world robustness without direct evaluation.

## 4. Milestones

### Milestone 1: Synthetic Data Testbed

Create one simple scene first. Prefer Blender/Cycles when available; otherwise use the analytic renderer fallback.

Required outputs:

- RGB images.
- Camera intrinsics and extrinsics.
- Ground-truth mesh or analytic surface definition.
- Ground-truth normals.
- Ground-truth albedo.
- Roughness or reflective mask.

Completion gate:

- A generated dataset exists under `refmotion_gs_mvp/outputs/synthetic/`.
- Camera convention tests pass.
- Reflected colored objects visibly vary across calibrated views in the rendered observations.

### Milestone 2: Geometry and Reflection Module

Implement:

- Camera rays.
- Projection and unprojection.
- Surface samples.
- Outgoing view direction.
- Reflection direction.
- Pluecker line representation.
- Reflected-ray distance.
- Candidate matching across views.

Completion gate:

- Unit tests pass for projection round trip, reflection on a known plane, Pluecker distance symmetry, and toy candidate matching.

### Milestone 3: Loss-Landscape Diagnostic

Implement Formulation A from `theory_rewrite.md`.

Test:

- Ground-truth normals.
- 1 degree perturbation.
- 3 degree perturbation.
- 5 degree perturbation.
- 10 degree perturbation.
- Smooth random perturbation.

Required result:

- Reflection-cycle loss is lower near ground-truth normals and generally increases as perturbation grows.

Decision gate:

- If this fails on clean synthetic data, stop implementation of training and diagnose the geometry, feature, and correspondence path first.

### Milestone 4: Normal-Only Optimization

Optimize only normal offsets or a tangent-space normal map. Do not optimize mesh vertices first.

Required result:

- Reflective-region normal angular error improves by at least 10 percent over the perturbed initialization.

### Milestone 5: UV Texture Baking and Leakage Metric

Implement:

- All-pixel baking.
- Oracle reflective-mask exclusion.
- Noisy mask-only baking.
- Proposed reflection-cycle confidence routing.
- Proposed normal refinement plus routing.

Metrics:

- Reflective-region normal angular error.
- Non-reflective normal angular error.
- Albedo RMSE.
- Specular leakage score.
- UV seam inconsistency if applicable.

### Milestone 6: MVP Go/No-Go

Update `MVP_RESULTS.md` with evidence, inference, and decision.

Required answers:

1. Is reflection-cycle loss correlated with normal correctness?
2. Does normal-only optimization improve reflective-region normals?
3. Does texture routing reduce specular leakage versus all-pixel baking?
4. Does it improve beyond mask-only baking?
5. Does it still work under noisy reflective masks?
6. What are the main failure cases?
7. Should the project continue, pivot, or stop?

## 5. Tests

Use test-first development for core behavior.

Planned tests:

- `tests/test_cameras.py`: camera projection, unprojection, and ray direction round trip.
- `tests/test_reflection_geometry.py`: reflection direction, Pluecker line construction, line distance symmetry, and distance monotonicity under normal perturbation in a controlled toy setup.
- `tests/test_synthetic_scene.py`: generated scene shapes, masks, normals, and color observations are deterministic and finite.
- `tests/test_feature_matching.py`: candidate matching selects same reflected-direction samples in a toy multi-view setup.
- `tests/test_losses.py`: diagnostic loss is lower for ground-truth normals than a controlled perturbation in a minimal synthetic fixture.
- `tests/test_metrics.py`: angular normal error, albedo RMSE, and leakage score are numerically stable.

## 6. Metrics

Primary metrics:

- Reflection-cycle loss under controlled normal perturbations.
- Reflective-region normal angular error.
- Non-reflective normal angular error.
- Albedo RMSE against ground truth.
- Specular leakage score based on contamination by reflected-object colors.

Secondary diagnostics:

- Candidate match entropy.
- Reflected-ray distance histograms.
- Loss curves during normal-only optimization.
- Texture residual visualizations.

## 7. Go/No-Go Criteria

Continue only if all are true:

1. Reflection-cycle loss is correlated with normal correctness.
2. Reflective-region normal error improves by at least 10 percent.
3. Specular leakage decreases compared with all-pixel baking and noisy-mask baking.
4. The method provides information beyond simply excluding reflective pixels.

Pivot if any are true:

1. Mask-only baking matches the method.
2. Feature correspondences are too ambiguous.
3. Normal error does not improve.
4. Improvements require ground-truth masks only.

Stop if either is true:

1. Reflection-cycle loss has no meaningful relationship with normal correctness on clean synthetic data.
2. The core hypothesis is falsified before adding any higher-capacity model.

## 8. Reviewer Risks and MVP Responses

**Component stacking:** The MVP implements only reflection-motion supervision, normal diagnostics, and texture routing. It avoids presenting mesh, UV, PBR, or Gaussian representation as novelty.

**Overlap with SpecTRe-GS and Ref-DGS:** The MVP does not implement near-field reflection rendering or local reflection Gaussians. It evaluates normal correctness and UV leakage, not only appearance fit.

**Overlap with MaterialRefGS:** The MVP isolates reflected-ray geometry and compares against mask-only and texture-only routing; later work should add a photometric-variation baseline if the core signal passes.

**Texture mapping overlap with TextureSplat:** UV or texture baking is an evaluation surface, not the claimed novelty.

**Learned reflection fields can absorb errors:** No learned reflection field is allowed in the MVP.

**Underdefined reflection loss:** Implementation follows Formulation A with explicit reflected-ray Pluecker distances, candidate sets, and frozen features.

**Real-data ground truth weakness:** The first evidence is synthetic and ground-truth controlled.

**Ill-posed UV/PBR evaluation:** Metrics focus on diffuse albedo leakage and normals, not full material recovery.

**Overclaimed relighting/editing:** No relighting or editing claim will be made.

**Signal may be unnecessary:** The MVP directly tests all-pixel, oracle mask-only, noisy mask-only, reflection-cycle routing, and normal-refinement plus routing.

