# MVP Implementation Plan

## Goal

Two-week MVP to test one hypothesis:

"Reflection-induced motion provides a useful normal/texture-disambiguation signal for reflective object mesh and UV texture recovery."

Do not implement full RefTex-GS. Do not implement learned near-field reflection fields, inter-reflection residuals, full PBR optimization, material editing, or relighting.

Required minimal pipeline: synthetic Blender/Cycles dataset, ground-truth mesh/normals/albedo/roughness/reflective-region mask, 2DGS or PGSR initialization, mesh extraction, fixed UV unwrap, baseline UV texture baking, one proposed reflection-consistency loss, and evaluation of normal error plus specular leakage.

## Repository Structure

```text
reftex_gs_mvp/
  data/
    synthetic/
      scene_*/images/
      scene_*/cameras.json
      scene_*/mesh_gt.obj
      scene_*/normal_gt.exr
      scene_*/albedo_gt.png
      scene_*/roughness_gt.png
      scene_*/reflective_mask.png
  scripts/
    render_blender_dataset.py
    run_pgsr_init.py
    extract_mesh.py
    unwrap_uv.py
    bake_baseline_texture.py
    compute_reflection_features.py
    train_reflection_loss.py
    evaluate.py
  src/
    cameras.py
    mesh.py
    uv_baking.py
    reflection_geometry.py
    feature_matching.py
    losses.py
    metrics.py
    diagnostics.py
  tests/
    test_reflection_geometry.py
    test_uv_baking.py
    test_feature_correspondence.py
    test_metrics.py
  outputs/
    runs/
```

## Stage 1: Synthetic Blender/Cycles Dataset

Files:

- `scripts/render_blender_dataset.py`
- `src/cameras.py`

Generate 3 to 5 scenes:

- glossy sphere with checker reflected object,
- chrome teapot-like object,
- glossy curved plate with nearby colored blocks,
- mixed diffuse/specular object.

Outputs:

- RGB images,
- camera intrinsics/extrinsics,
- ground-truth mesh,
- ground-truth normal maps,
- albedo map or per-surface albedo,
- roughness map,
- reflective mask.

Sanity checks:

- projected mesh silhouette matches rendered mask,
- normals are in camera and world conventions correctly,
- reflected nearby object visibly moves across views.

Unit tests:

- camera projection/unprojection round trip,
- coordinate convention test with a known plane.

## Stage 2: Initialization

Files:

- `scripts/run_pgsr_init.py`
- `scripts/extract_mesh.py`
- `src/mesh.py`

Use 2DGS or PGSR as initialization. If integration is too slow, start from the ground-truth mesh with controlled perturbations to isolate the loss behavior, then swap in PGSR.

Inputs:

- RGB images,
- masks,
- cameras.

Outputs:

- coarse mesh,
- per-view rendered depth/normal,
- baseline projected surface samples.

Sanity checks:

- mesh is close enough for reflected-ray neighborhoods to overlap,
- reflective regions have higher photometric residual than diffuse regions.

Decision gate:

- if PGSR integration consumes more than 3 days, use perturbed ground-truth mesh for MVP and report that the loss is being tested independently of reconstruction initialization.

## Stage 3: Fixed UV Unwrap and Baseline Baking

Files:

- `scripts/unwrap_uv.py`
- `scripts/bake_baseline_texture.py`
- `src/uv_baking.py`

Implement:

```python
def bake_texture(mesh, cameras, images, masks, reflective_mask=None, mode="all_pixels"):
    ...
```

Baselines:

1. Bake all visible observations.
2. Bake only non-reflective observations using ground-truth mask.
3. Bake using noisy predicted reflective mask.

Outputs:

- UV albedo texture,
- visibility count map,
- specular leakage map.

Metrics:

- albedo RMSE against ground truth,
- specular leakage score: correlation between baked albedo residual and reflected-object colors,
- UV seam inconsistency.

## Stage 4: Reflection Feature Correspondence

Files:

- `src/reflection_geometry.py`
- `src/feature_matching.py`
- `scripts/compute_reflection_features.py`

Minimal functions:

```python
def reflect(view_dir, normal):
    ...

def plucker_line(point, direction):
    ...

def reflected_ray_distance(line_a, line_b, beta):
    ...

def candidate_pixels(view_i_sample, view_j_surface_samples, radius, k):
    ...

def soft_reflection_feature(sample_i, candidates_j, tau):
    ...
```

Use frozen features:

- start with RGB patches and Sobel/LoG features,
- then test DINOv2 or another frozen feature extractor only if needed.

Sanity checks:

- on ground-truth normals, reflected feature matches are better than on perturbed normals,
- the loss increases monotonically for 1, 3, 5, 10 degree normal perturbations near ground truth.

Unit tests:

- reflection direction for a known plane,
- Pluecker distance symmetry,
- candidate selection returns expected pixels in a toy mirror scene.

## Stage 5: Proposed Loss

Files:

- `src/losses.py`
- `scripts/train_reflection_loss.py`

Implement Formulation A only:

```text
L = L_nonref_texture + lambda_cycle L_feature_reflection_cycle
    + lambda_normal L_normal_smooth + lambda_mesh L_laplacian.
```

Variables:

- normal map or vertex normal offsets first,
- mesh vertices second if the normal-only test succeeds.

Stop-gradient:

- freeze image features,
- freeze correspondence weights in first experiments,
- freeze reflective mask.

No learned F_nf.

Expected outputs:

- refined normals,
- updated mesh if enabled,
- baked texture after reflective routing.

## Stage 6: Evaluation

Files:

- `src/metrics.py`
- `src/diagnostics.py`
- `scripts/evaluate.py`

Metrics:

- reflective-region normal angular error,
- non-reflective normal angular error,
- albedo RMSE,
- specular leakage score,
- held-out reflective-region rendering error,
- Chamfer distance if mesh vertices are optimized.

Required plots:

- normal error vs. training iteration,
- leakage score for all-pixel bake, mask-only bake, proposed,
- loss curve under controlled normal perturbations,
- visual UV textures with reflected-color contamination highlighted.

## Two-Week Schedule

Days 1-2: Blender dataset and camera/normal convention tests.

Days 3-4: baseline mesh path. Use PGSR if easy; otherwise use perturbed GT mesh.

Days 5-6: UV unwrap and baseline baking metrics.

Days 7-8: reflection geometry, candidate matching, and feature extraction.

Days 9-10: implement reflection-cycle loss and normal-only optimization.

Days 11-12: mesh-vertex optimization if normal-only succeeds; otherwise diagnose.

Day 13: ablations and plots.

Day 14: go/no-go report.

## Continue / Abandon Criteria

Continue if all are true:

- on synthetic scenes, reflection-cycle loss is lower near ground-truth normals than perturbed normals,
- reflective-region normal error improves by at least 10 percent over PGSR/2DGS initialization,
- specular leakage in UV albedo decreases versus all-pixel baking and mask-only baking,
- held-out reflective-region error does not worsen substantially.

Abandon or pivot if any are true:

- loss has no monotonic relation to normal perturbation,
- feature correspondences are too ambiguous even on synthetic data,
- improvements require ground-truth masks and fail under mild mask noise,
- texture leakage can be solved equally well by simply excluding reflective pixels,
- optimization improves rendering but not normals or UV texture.
