# RefMotion-GS MVP Results

## Current Decision State

Status: **PRELIMINARY CONTINUE WITH CAUTION**

The reduced hypothesis is not falsified on the first clean analytic synthetic scene. The current evidence supports continuing the MVP, but not yet making a paper-level claim. The strongest unresolved issue is that the proposed routing nearly matches but does not beat oracle reflective-mask exclusion on the specular leakage metric.

## Evidence Ledger

### Environment

- Blender/Cycles executable: unavailable on `PATH`.
- Analytic synthetic renderer fallback: selected for Milestone 1.
- Python dependencies for first MVP stage: available for NumPy, PyTest, Matplotlib, Pillow, and Torch.

### Verification Commands

```bash
pytest refmotion_gs_mvp/tests -q
python -m py_compile refmotion_gs_mvp/src/*.py refmotion_gs_mvp/scripts/run_mvp_diagnostics.py
python refmotion_gs_mvp/scripts/run_mvp_diagnostics.py --out-dir refmotion_gs_mvp/outputs/run_latest
```

Observed:

- 16 tests passed.
- Python compilation passed.
- Metrics, plots, pixel-space bakes, and sphere-UV textures were written to `refmotion_gs_mvp/outputs/run_latest/`.

### Loss-Landscape Diagnostic

Evidence:

| Perturbation | Reflection-cycle loss |
|---|---:|
| 0 deg | 0.0005611105653096932 |
| 1 deg | 0.0005811010930655471 |
| 3 deg | 0.0006926487699608295 |
| 5 deg | 0.0009197920034853393 |
| 10 deg | 0.0019402526425899235 |
| smooth random | 0.008498769904632624 |

Inference:

- The diagnostic loss is correlated with normal correctness on this clean analytic scene.
- This supports continuing to a more realistic synthetic renderer or a less constrained normal map.

### Normal-Only Optimization

Evidence:

- Reflective-region normal error improved from 5.7091979244066104 deg to 0.3569152456956942 deg.
- Improvement: 93.74841702071855 percent.
- Non-reflective normal error changed from 6.050038057050539 deg to 0.37822275380886655 deg.
- Optimization loss decreased from 0.0014502013166587903 to 0.0005588875658240342.

Inference:

- The normal-only diagnostic passes the 10 percent improvement threshold.
- The current optimizer is intentionally limited to global normal rotations, so this is a low-dimensional proof of signal, not evidence that dense normal-map optimization is solved.

### Texture Routing and Leakage

Evidence:

Sphere-UV atlas evidence:

| Method | Specular leakage score | Albedo RMSE |
|---|---:|---:|
| all pixels | 0.8937587779761458 | 0.14287779314593882 |
| oracle mask exclusion | 0.18894842742715495 | 0.08882049812030215 |
| noisy mask only | 0.48688553583972904 | 0.10497112705538789 |
| reflection-confidence routing | 0.20555594061539617 | 0.03822351541988649 |
| normal refinement plus routing | 0.19090032877604535 | 0.03967209496171139 |

Pixel-space proxy evidence:

| Method | Specular leakage score | Albedo RMSE |
|---|---:|---:|
| all pixels | 0.9845810540201183 | 0.15493268014400016 |
| oracle mask exclusion | 0.1889352304278196 | 0.08883342661823146 |
| noisy mask only | 0.48058422963629 | 0.09827136194153686 |
| reflection-confidence routing | 0.20411952363401434 | 0.03474389022354434 |
| normal refinement plus routing | 0.18994099794232064 | 0.03739227320947693 |

Inference:

- Routing reduces leakage compared with all-pixel baking and noisy-mask-only baking.
- Routing almost matches oracle mask exclusion on leakage but does not beat it in either pixel-space or sphere-UV evaluation.
- Routing improves albedo RMSE versus all baselines in the sphere-UV evaluation, but this is still an analytic sphere atlas rather than a production unwrap.

## Required MVP Questions

1. Is reflection-cycle loss correlated with normal correctness?
   - Answer: yes on the analytic scene. Loss increases monotonically from 0 to 10 degrees and is highest under smooth random perturbation.

2. Does normal-only optimization improve reflective-region normals?
   - Answer: yes in the constrained global-offset diagnostic. Reflective normal error improved by 93.74841702071855 percent.

3. Does texture routing reduce specular leakage versus all-pixel baking?
   - Answer: yes. In sphere-UV evaluation, leakage decreased from 0.8937587779761458 to 0.19090032877604535 for normal refinement plus routing.

4. Does it improve beyond mask-only baking?
   - Answer: mixed. It improves beyond noisy-mask-only baking but does not beat oracle mask exclusion on leakage.

5. Does it still work under noisy reflective masks?
   - Answer: yes in the sphere-UV diagnostic. With an observed reflective-mask false-negative rate of 0.34294871794871795, normal refinement plus routing reduced leakage from 0.48688553583972904 to 0.19090032877604535.

6. What are the main failure cases?
   - Current risks:
     - The current renderer is analytic and simpler than Blender/Cycles.
     - The optimizer is a global normal-offset search, not a dense tangent-space normal map.
     - The UV metric uses a sphere-parameterized atlas for the analytic sphere, not a general unwrap.
     - Oracle mask exclusion remains a very strong baseline.

7. Should the project continue, pivot, or stop?
   - Decision: continue the MVP, but only to the next stricter validation. Do not claim final method success yet.

## Decision Criteria

Continue only if:

- Reflection-cycle loss is correlated with normal correctness.
- Reflective-region normal error improves by at least 10 percent.
- Specular leakage decreases compared with all-pixel and noisy-mask baking.
- The method provides information beyond simply excluding reflective pixels.

Current assessment:

- First three checks pass.
- The fourth check is only partially satisfied: the method improves over noisy mask exclusion and gives much better albedo RMSE in the proxy, but it does not beat oracle mask exclusion on leakage. This requires the next stricter milestone before a strong continue decision.

Pivot if:

- Mask-only baking matches the method.
- Feature correspondences are too ambiguous.
- Normal error does not improve.
- Improvements require ground-truth masks only.

Stop if:

- Reflection-cycle loss has no meaningful relationship with normal correctness on clean synthetic data.
- The core hypothesis is falsified on the clean synthetic fallback scene.

Current stop criteria:

- Not met.

## Next Required Milestone

1. Replace the global normal-offset optimizer with a per-surface or tangent-space normal-map optimizer.
2. Move from the analytic reflected-color lobes to Blender/Cycles or a more explicit near-object analytic reflection scene.
3. Keep the same all-pixel, oracle-mask, noisy-mask, reflection-routing, and normal-refinement-plus-routing baselines.
4. Re-run the go/no-go decision. If oracle mask-only still matches the proposed method and the method does not add value under noisy masks or UV seams, pivot to the benchmark/leakage-metric direction.
