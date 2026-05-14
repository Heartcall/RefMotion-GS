# RefMotion-GS MVP Implementation Log

## 2026-05-14

### Initialization

Evidence:

- Read all binding Phase 2 files under `outputs/phase2/`.
- `blender` is not available on `PATH` in this environment.
- Python has `numpy`, `pytest`, `matplotlib`, `PIL`, and `torch` importable.
- The current directory is not a git repository.

Inference:

- The MVP should start with the allowed analytic synthetic renderer fallback instead of blocking on Blender/Cycles.
- Because this workspace is not a git repository, milestone progress will be tracked through files and test output rather than commits.

Next actions:

1. Create package and test skeleton.
2. Write failing tests for camera and reflection geometry.
3. Implement only enough code to pass those tests.
4. Generate the first analytic synthetic scene.

### Milestone Status

- Milestone 1: completed with analytic fallback, not Blender/Cycles.
- Milestone 2: completed for camera rays, projection/unprojection, reflection directions, Pluecker representation, reflected-ray distance, and candidate matching.
- Milestone 3: completed for Formulation A diagnostic on the analytic scene.
- Milestone 4: completed as a constrained global normal-offset coordinate search.
- Milestone 5: completed with a minimal sphere-parameterized UV atlas plus the earlier pixel-space proxy.
- Milestone 6: preliminary decision recorded in `MVP_RESULTS.md`.

### Implemented Files

- `src/cameras.py`: calibrated pinhole camera conventions.
- `src/synthetic_scene.py`: analytic glossy/diffuse sphere fallback with reflected-color observations.
- `src/reflection_geometry.py`: reflection, Pluecker lines, angular error, and rotation helpers.
- `src/feature_matching.py`: reflected-ray top-k candidate matching.
- `src/losses.py`: Formulation A feature-space reflection-cycle diagnostic.
- `src/normal_optimization.py`: normal-only coordinate-search refinement.
- `src/uv_baking.py`: pixel-space routing and baking proxy.
- `src/uv_baking.py`: sphere UV atlas baking, visibility counts, and image-space reprojection for metrics.
- `src/metrics.py`: normal error, albedo RMSE, and specular leakage score.
- `scripts/run_mvp_diagnostics.py`: reproducible metric and plot generation.
- `tests/`: 16 unit/diagnostic tests.

### Verification

Commands:

```bash
pytest refmotion_gs_mvp/tests -q
python -m py_compile refmotion_gs_mvp/src/*.py refmotion_gs_mvp/scripts/run_mvp_diagnostics.py
python refmotion_gs_mvp/scripts/run_mvp_diagnostics.py --out-dir refmotion_gs_mvp/outputs/run_latest
```

Observed results:

- `pytest`: 14 passed in 9.00s.
- Latest `pytest`: 16 passed in 9.46s after adding sphere UV atlas tests.
- `py_compile`: exit code 0.
- Diagnostics decision checks:
  - `loss_correlated_near_gt`: true.
  - `normal_error_improves_10_percent`: true.
  - `routing_beats_all_pixels`: true.
  - `routing_beats_noisy_mask`: true.
  - `routing_beats_oracle_mask`: false.

### Key Metrics

- Loss landscape:
  - 0 deg: 0.0005611105653096932.
  - 1 deg: 0.0005811010930655471.
  - 3 deg: 0.0006926487699608295.
  - 5 deg: 0.0009197920034853393.
  - 10 deg: 0.0019402526425899235.
  - smooth random: 0.008498769904632624.
- Normal optimization:
  - reflective error: 5.7091979244066104 deg to 0.3569152456956942 deg.
  - improvement: 93.74841702071855 percent.
  - non-reflective error: 6.050038057050539 deg to 0.37822275380886655 deg.
- Specular leakage score:
  - sphere UV all pixels: 0.8937587779761458.
  - sphere UV oracle mask exclusion: 0.18894842742715495.
  - sphere UV noisy mask only: 0.48688553583972904.
  - sphere UV reflection-confidence routing: 0.20555594061539617.
  - sphere UV normal refinement plus routing: 0.19090032877604535.
- Pixel-space specular leakage score:
  - all pixels: 0.9845810540201183.
  - oracle mask exclusion: 0.1889352304278196.
  - noisy mask only: 0.48058422963629.
  - reflection-confidence routing: 0.20411952363401434.
  - normal refinement plus routing: 0.18994099794232064.
- Sphere UV albedo RMSE:
  - all pixels: 0.14287779314593882.
  - oracle mask exclusion: 0.08882049812030215.
  - noisy mask only: 0.10497112705538789.
  - reflection-confidence routing: 0.03822351541988649.
  - normal refinement plus routing: 0.03967209496171139.
- Pixel-space albedo RMSE:
  - all pixels: 0.15493268014400016.
  - oracle mask exclusion: 0.08883342661823146.
  - noisy mask only: 0.09827136194153686.
  - reflection-confidence routing: 0.03474389022354434.
  - normal refinement plus routing: 0.03739227320947693.

### Self-Review Notes

- This is still not a production UV unwrap, but the current baking metric now uses an explicit sphere-parameterized UV atlas for the analytic sphere.
- The normal optimizer currently uses a global rotation offset, which is a favorable low-dimensional diagnostic. A tangent-space normal-map optimizer is still needed.
- The synthetic renderer uses fixed analytic reflected-color lobes rather than Blender/Cycles path tracing.
- The method nearly matches but does not beat oracle reflective-mask exclusion on leakage; the evidence beyond simple exclusion is currently strongest under noisy masks and in albedo RMSE.
- No learned reflection field, inter-reflection residual, full PBR, relighting, or material editing code was introduced.
