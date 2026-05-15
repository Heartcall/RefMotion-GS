# RefMotion-GS Phase 3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use the project workflow in `AGENTS.md` and `OPERATING_PROTOCOL.md`. Implement task-by-task only after `NEXT_ACTION.md` names the current milestone. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the analytic MVP into a stricter, reproducible Phase 3 validation pipeline that can test whether reflection-motion supervision adds value beyond mask-only exclusion under less favorable optimization and scene conditions.

**Architecture:** Phase 3 first refactors the current monolithic MVP diagnostics into reusable experiment components and stable result schemas without changing method behavior. Dense / tangent-space normal optimization is deferred to Milestone 3.2, after the Milestone 3.1 framework proves it can reproduce the existing MVP baselines and decision checks.

**Tech Stack:** Python, NumPy, PyTest, Matplotlib/Pillow, existing `refmotion_gs_mvp/src` modules. Blender/Cycles remains optional and must not block Milestone 3.1.

---

## 1. Scope Lock

The active project remains **RefMotion-GS**, not full RefTex-GS.

Do not implement or claim:

- learned near-field reflection fields,
- inter-reflection residuals,
- full PBR optimization,
- relighting,
- material editing,
- mesh representation novelty,
- UV representation novelty,
- PBR representation novelty,
- Gaussian representation novelty.

Mesh, UV, baking, and Gaussian-related items are scaffolding only.

## 2. Evidence That Motivates Phase 3

Current MVP evidence from `MVP_RESULTS.md` and `outputs/run_latest/metrics.json`:

- Reflection-cycle loss is correlated with normal correctness on the analytic scene.
- Reflective-region normal error improved from `5.7091979244066104` degrees to `0.3569152456956942` degrees under the current global-rotation optimizer.
- Sphere-UV leakage improved from all-pixel `0.8937587779761458` and noisy-mask `0.48688553583972904` to normal-refinement-plus-routing `0.19090032877604535`.
- Oracle mask exclusion leakage is still slightly better at `0.18894842742715495`.
- The current renderer uses analytic reflected-color lobes, not Blender/Cycles or explicit near-object reflected geometry.

Inference:

- The reduced hypothesis is not falsified.
- The current evidence is not strong enough for a paper-level claim.
- Phase 3 must make the mask-only threat, optimizer-favorability threat, and renderer-validity threat explicit gates.

## 3. Milestone Numbering

Use this convention unless a future audit explicitly overrides it:

- **Milestone 3.1:** Experiment framework refactor.
- **Milestone 3.2:** Dense / tangent-space normal optimization.
- **Milestone 3.3:** Stricter scene or renderer validation.
- **Milestone 3.4:** Phase 3 go/no-go audit and paper-claim boundary update.

Dense / tangent-space normal optimization is Milestone 3.2, not Milestone 3.1.

## 4. Phase Gates

### Continue

Continue only if all are true:

- Existing MVP decision checks remain reproducible.
- The framework records all baselines and metrics in stable JSON and markdown outputs.
- Later Milestone 3.2 improves reflective normal error under less favorable normal degrees of freedom.
- Routing beats all-pixel and noisy-mask baselines and is analyzed against oracle mask exclusion.

### Revise

Revise if any are true:

- Metrics are not reproducible across repeated runs with the same seed.
- The result schema drops any MVP baseline.
- The plan or implementation makes dense normal optimization part of Milestone 3.1.
- The framework cannot compare against oracle mask exclusion.

### Pivot

Pivot to a benchmark/leakage-metric direction if any are true after Milestone 3.2 or 3.3:

- Mask-only baking matches the proposed method in all meaningful settings.
- Dense/tangent normal optimization does not improve reflective-region normal error.
- Improvements depend on ground-truth masks only.
- Feature correspondences are too ambiguous outside the current analytic scene.

### Stop

Stop if either is true:

- Reflection-cycle loss loses meaningful relationship with normal correctness on clean controlled data.
- The core reflection-motion hypothesis is falsified before adding higher-capacity components.

## 5. Required Baselines

Every Phase 3 milestone that reports texture or leakage metrics must include:

- `all_pixels`
- `oracle_mask_exclusion`
- `noisy_mask_only`
- `reflection_confidence_routing`
- `normal_refinement_plus_routing`

Every decision summary must report:

- `routing_beats_all_pixels`
- `routing_beats_noisy_mask`
- `routing_beats_oracle_mask`

`routing_beats_oracle_mask` is not required to be true for early continuation, but it must be reported and interpreted. If it remains false, the summary must explain whether the method still adds value under noisy masks, albedo RMSE, UV seams, or normal accuracy.

## 6. Milestone 3.1: Experiment Framework Refactor

**Classification:** small-to-medium implementation milestone.

**Audit requirement after completion:** short audit using `PROMPTS/short_audit_prompt.md`.

**Purpose:** Extract reusable experiment and reporting structure from `scripts/run_mvp_diagnostics.py` while preserving current MVP behavior and metrics.

**Non-goals:**

- Do not implement dense / tangent-space normal optimization.
- Do not change the loss formulation.
- Do not add Blender/Cycles integration.
- Do not change current metric definitions.
- Do not claim performance improvement.

### Files

Create:

- `refmotion_gs_mvp/src/experiment_protocol.py`
- `refmotion_gs_mvp/src/decision_checks.py`
- `refmotion_gs_mvp/scripts/run_phase3_milestone31.py`
- `refmotion_gs_mvp/tests/test_experiment_protocol.py`
- `refmotion_gs_mvp/tests/test_decision_checks.py`

Modify only if needed:

- `refmotion_gs_mvp/scripts/run_mvp_diagnostics.py`
- `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`
- `refmotion_gs_mvp/DECISION_LOG.md`
- `refmotion_gs_mvp/NEXT_ACTION.md`

Do not modify:

- `refmotion_gs_mvp/src/synthetic_scene.py`
- `refmotion_gs_mvp/src/losses.py`
- `refmotion_gs_mvp/src/normal_optimization.py`
- `refmotion_gs_mvp/src/uv_baking.py`
- `refmotion_gs_mvp/src/metrics.py`

These files may be read, but Milestone 3.1 should not change their behavior.

### Output Contract

Milestone 3.1 must write:

- `refmotion_gs_mvp/outputs/phase3/milestone_31_framework/metrics.json`
- `refmotion_gs_mvp/outputs/phase3/milestone_31_framework/summary.md`

The `metrics.json` must include:

```json
{
  "dataset": {},
  "loss_landscape": {},
  "normal_optimization": {},
  "texture_baking": {
    "specular_leakage_score": {},
    "albedo_rmse": {}
  },
  "uv_texture_baking": {
    "specular_leakage_score": {},
    "albedo_rmse": {}
  },
  "decision_checks": {
    "loss_correlated_near_gt": true,
    "normal_error_improves_10_percent": true,
    "routing_beats_all_pixels": true,
    "routing_beats_noisy_mask": true,
    "routing_beats_oracle_mask": false
  },
  "phase3": {
    "milestone": "3.1",
    "purpose": "experiment_framework_refactor",
    "implemented_dense_normal_optimization": false,
    "implemented_learned_near_field_reflection": false
  }
}
```

The exact numeric values may differ only if the runner intentionally uses a different output directory with the same seeds and existing MVP code path. Any difference from `outputs/run_latest/metrics.json` must be explained in `summary.md`.

### Test Plan

Add tests before implementation:

- `tests/test_decision_checks.py::test_decision_checks_preserve_mvp_thresholds`
  - Build a small dictionary with MVP-style leakage values.
  - Assert `routing_beats_all_pixels` and `routing_beats_noisy_mask` are true.
  - Assert `routing_beats_oracle_mask` is false when oracle leakage is lower.

- `tests/test_decision_checks.py::test_decision_checks_require_all_baselines`
  - Omit one required baseline from a metric dictionary.
  - Assert the decision-check helper raises `KeyError` or a project-defined validation error.

- `tests/test_experiment_protocol.py::test_phase3_metadata_blocks_forbidden_components`
  - Create Milestone 3.1 metadata.
  - Assert dense normal optimization and learned near-field reflection flags are false.

- `tests/test_experiment_protocol.py::test_result_summary_mentions_oracle_mask_status`
  - Generate a summary string or summary data structure from metrics where `routing_beats_oracle_mask` is false.
  - Assert the summary explicitly mentions oracle mask status.

### Implementation Steps

- [ ] **Step 1: Add decision-check tests**

Run:

```bash
pytest refmotion_gs_mvp/tests/test_decision_checks.py -q
```

Expected before implementation: fails because `decision_checks.py` does not exist.

- [ ] **Step 2: Implement `src/decision_checks.py`**

Required public functions:

```python
def compute_routing_decision_checks(uv_leakage: dict[str, float]) -> dict[str, bool]:
    ...

def require_baselines(metric_values: dict[str, float], required: tuple[str, ...] | None = None) -> None:
    ...
```

The required baselines are exactly:

```python
(
    "all_pixels",
    "oracle_mask_exclusion",
    "noisy_mask_only",
    "reflection_confidence_routing",
    "normal_refinement_plus_routing",
)
```

- [ ] **Step 3: Add experiment protocol tests**

Run:

```bash
pytest refmotion_gs_mvp/tests/test_experiment_protocol.py -q
```

Expected before implementation: fails because `experiment_protocol.py` does not exist.

- [ ] **Step 4: Implement `src/experiment_protocol.py`**

Required public functions:

```python
def phase3_milestone_metadata(milestone: str, purpose: str) -> dict:
    ...

def write_summary(path, metrics: dict) -> None:
    ...
```

For Milestone 3.1, metadata must include:

```python
{
    "milestone": "3.1",
    "purpose": "experiment_framework_refactor",
    "implemented_dense_normal_optimization": False,
    "implemented_learned_near_field_reflection": False,
}
```

- [ ] **Step 5: Add `scripts/run_phase3_milestone31.py`**

The script should call the existing MVP diagnostic path, attach Phase 3 metadata, recompute decision checks through `src/decision_checks.py`, and write `summary.md`.

Run:

```bash
python refmotion_gs_mvp/scripts/run_phase3_milestone31.py --out-dir refmotion_gs_mvp/outputs/phase3/milestone_31_framework
```

Expected: writes `metrics.json`, plots/images inherited from the MVP runner if reused, and `summary.md`.

- [ ] **Step 6: Run full verification**

Run:

```bash
pytest refmotion_gs_mvp/tests -q
python -m py_compile refmotion_gs_mvp/src/*.py refmotion_gs_mvp/scripts/run_mvp_diagnostics.py refmotion_gs_mvp/scripts/run_phase3_milestone31.py
python refmotion_gs_mvp/scripts/run_phase3_milestone31.py --out-dir refmotion_gs_mvp/outputs/phase3/milestone_31_framework
```

Expected:

- all tests pass,
- Python compilation exits 0,
- Milestone 3.1 metrics and summary are written,
- `phase3.implemented_dense_normal_optimization` is false,
- `phase3.implemented_learned_near_field_reflection` is false.

### Milestone 3.1 Pass Criteria

Pass if all are true:

- Tests pass.
- `run_phase3_milestone31.py` writes the required output files.
- The required baseline suite is present.
- Decision checks are present and interpretable.
- Existing MVP decision checks remain consistent with `outputs/run_latest/metrics.json`.
- No forbidden component is implemented.
- `summary.md` explicitly discusses oracle mask status.

Revise if any are true:

- Output schema is missing a required section.
- A baseline is missing.
- The runner changes metric behavior without explanation.
- The summary hides `routing_beats_oracle_mask`.

Stop and request user input if:

- Refactoring requires changing core loss, renderer, or optimization behavior.
- Any forbidden component appears necessary to pass Milestone 3.1.

## 7. Milestone 3.2: Dense / Tangent-Space Normal Optimization

**Classification:** major method-validation milestone.

**Audit requirement before implementation:** GPT-5.5 xhigh pre-implementation authorization audit using `PROMPTS/pre_major_milestone_audit_prompt.md`.

Milestone 3.2 must not start until Milestone 3.1 passes and is audited.

Purpose:

- Replace the favorable global rotation search with a less favorable per-surface or tangent-space normal diagnostic.
- Keep Formulation A and the baseline suite unchanged.
- Show whether reflective normal error still improves under denser normal degrees of freedom.

### 7.1 Scope And Non-Goals

Milestone 3.2 remains a diagnostic on the existing analytic MVP dataset. It does not add a learned reflection field, inter-reflection residual, full PBR optimization, relighting, material editing, renderer integration, or representation-novelty claim.

Allowed implementation:

- a shared tangent-space normal-offset grid over the existing analytic sphere UV parameterization,
- deterministic NumPy coordinate-search optimization,
- smoothness and magnitude regularization,
- existing Formulation A `reflection_cycle_loss`,
- existing texture/leakage baseline suite,
- a diagnostic ablation with dense variables but no reflection-cycle loss.

Do not change:

- `src/synthetic_scene.py`
- `src/losses.py` behavior or loss semantics,
- `src/uv_baking.py` metric definitions,
- existing Milestone 3.1 runner outputs.

### 7.2 Normal Parameterization

Create a shared sphere-UV tangent normal grid:

```python
normal_delta_uv: np.ndarray  # shape: (uv_height, uv_width, 2)
uv_height = 16
uv_width = 32
```

Each texel stores two tangent coefficients `(a, b)`. For every object pixel with surface point `x`, compute UV with the existing `sphere_points_to_uv(x)` convention and nearest-neighbor texel lookup. Let `n_init(view, y, x)` be the perturbed initialization normal.

Define a deterministic tangent frame from the surface point:

```text
radial = normalize(surface_point)
reference = [0, 1, 0] if abs(dot(radial, [0, 1, 0])) < 0.95 else [1, 0, 0]
t1 = normalize(cross(reference, radial))
t2 = normalize(cross(radial, t1))
```

The optimized normal at a pixel is:

```text
n_opt = normalize(n_init + a(texel) * t1 + b(texel) * t2)
```

This keeps Formulation A unchanged: dense normals affect reflected-ray geometry because `n_opt` is passed into `reflection_cycle_loss`, which computes reflected directions and reflected-ray candidate matching.

Initialization:

- build `n_init` by rotating all object normals from `dataset.normals` by `8.0` degrees around the x axis, matching the MVP global-rotation diagnostic,
- initialize `normal_delta_uv` to zeros,
- never use ground-truth normals inside the optimizer objective; ground truth is used only for metrics.

Unit constraint:

- every composed pixel normal must be normalized after adding tangent offsets,
- texel coefficients are clipped to `[-0.35, 0.35]` after every accepted update.

### 7.3 Objective And Regularization

Main objective:

```text
L_total = L_cycle(normals(normal_delta_uv))
          + lambda_smooth * L_smooth(normal_delta_uv)
          + lambda_l2 * L_l2(normal_delta_uv)
```

Defaults:

```text
lambda_smooth = 0.02
lambda_l2 = 0.001
loss_seed = 59
```

Sampling policy after the Milestone 3.2 post-result audit:

- The optimizer helper supports `sample_count = 250` as the stricter planned setting.
- The accepted Milestone 3.2 result-producing smoke run uses `sample_count = 40` for repeatable Codex execution time.
- Reports that use `sample_count = 40` must call the result a lower-cost analytic smoke diagnostic, not a full dense-normal validation.
- A later strict rerun may raise `sample_count` to `250`, but that must be recorded as a separate action and must not be conflated with the current Milestone 3.2 evidence.

Smoothness:

```text
L_smooth = mean over valid neighbor pairs of
           ||delta[u, v] - delta[u + 1, v]||_2^2
         + ||delta[u, v] - delta[u, v + 1]||_2^2
```

Use horizontal wrap for the sphere-UV `u` axis. Do not wrap the polar `v` axis. Include only texels that receive at least one object-pixel observation in `dataset.object_mask`; inactive texels remain zero.

Magnitude:

```text
L_l2 = mean ||delta[u, v]||_2^2
```

The ablation without reflection-cycle loss uses:

```text
L_no_cycle = lambda_smooth * L_smooth + lambda_l2 * L_l2
```

It starts from the same `n_init` and zero delta grid. Its expected behavior is to provide no meaningful normal recovery beyond smoothing/magnitude bias; it is included to show that dense degrees of freedom alone do not explain any improvement.

### 7.4 Optimizer

Use deterministic coordinate search, not learned fields or autograd-heavy training.

Defaults:

```text
iterations = 8
initial_step = 0.08
step_decay = 0.5
min_step = 0.01
max_active_texels = 64
seed = 53
```

Local proposal policy after the Milestone 3.2 post-result audit:

- `update_radius = 0` means a strict single-texel coordinate proposal.
- The accepted Milestone 3.2 result-producing smoke run uses `update_radius = 1`, applying the same signed tangent-channel step to the selected texel and its immediate valid sphere-UV neighbors.
- This remains a deterministic dense tangent-space coordinate search because no learned reflection field, autograd training, image-color fitting field, or new objective is introduced; the proposal only changes the local support of a candidate coordinate step.
- Reports using `update_radius = 1` must explicitly record it and must not describe the run as strict single-texel coordinate search.

Active texels:

- rank texels by count of reflective object pixels mapped to that texel,
- optimize the top `max_active_texels` texels,
- keep all other texels fixed at zero for the first Milestone 3.2 diagnostic.

Per iteration:

1. Evaluate current `L_total`.
2. For each active texel, each tangent channel, and signs `[-1, +1]`, try one step. If `update_radius > 0`, apply that candidate step to the selected texel neighborhood with horizontal UV wrap and clipped polar rows.
3. Compose normals, normalize, evaluate `L_total`.
4. Accept the single best candidate if it improves objective.
5. If no candidate improves objective, halve the step.
6. Stop early if `step < min_step`.

Record:

- `loss_history`,
- accepted update `(iteration, texel_y, texel_x, channel, step, loss)`,
- `update_radius` for each accepted update,
- active texel count,
- final step size.

### 7.5 Files

Create:

- `refmotion_gs_mvp/src/dense_normal_optimization.py`
- `refmotion_gs_mvp/scripts/run_phase3_milestone32.py`
- `refmotion_gs_mvp/tests/test_dense_normal_optimization.py`
- `refmotion_gs_mvp/tests/test_phase3_milestone32_runner.py`

Modify only if needed:

- `refmotion_gs_mvp/src/experiment_protocol.py`
- `refmotion_gs_mvp/src/decision_checks.py`
- `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`
- `refmotion_gs_mvp/DECISION_LOG.md`
- `refmotion_gs_mvp/NEXT_ACTION.md`

Do not modify for Milestone 3.2:

- `refmotion_gs_mvp/src/synthetic_scene.py`
- `refmotion_gs_mvp/src/losses.py`
- `refmotion_gs_mvp/src/uv_baking.py`
- `refmotion_gs_mvp/src/metrics.py`
- `refmotion_gs_mvp/outputs/run_latest/`

### 7.6 Tests

Add tests before implementation:

- `tests/test_dense_normal_optimization.py::test_tangent_delta_normals_are_unit_length`
  - create a small analytic dataset,
  - build zero and nonzero tangent deltas,
  - assert composed object normals are finite and unit length.

- `tests/test_dense_normal_optimization.py::test_dense_cycle_optimizer_reduces_reflective_error`
  - generate a small deterministic dataset,
  - perturb object normals by 8 degrees,
  - run the dense optimizer with small settings,
  - assert reflective normal error improves by at least 10 percent,
  - assert final objective is not higher than initial objective.

- `tests/test_dense_normal_optimization.py::test_no_cycle_dense_ablation_does_not_use_reflection_cycle_loss`
  - run the no-cycle ablation,
  - assert it records `uses_reflection_cycle_loss: False`,
  - assert it preserves finite unit normals.

- `tests/test_phase3_milestone32_runner.py::test_milestone32_runner_schema_and_scope_flags`
  - run a reduced runner configuration into a temporary directory,
  - assert `metrics.json` includes `dense_normal_optimization`, `dense_no_cycle_ablation`, `texture_baking`, `uv_texture_baking`, `decision_checks`, and `phase3`,
  - assert `phase3.milestone == "3.2"`,
  - assert forbidden-component flags remain false,
  - assert all required MVP baselines remain present.

### 7.7 Output Contract

Milestone 3.2 writes:

- `refmotion_gs_mvp/outputs/phase3/milestone_32_dense_normals/metrics.json`
- `refmotion_gs_mvp/outputs/phase3/milestone_32_dense_normals/summary.md`
- `refmotion_gs_mvp/outputs/phase3/milestone_32_dense_normals/dense_loss_history.png`
- optional visual diagnostics for UV normal-delta magnitude and leakage bars.

`metrics.json` must include:

```json
{
  "dataset": {},
  "loss_landscape": {},
  "global_rotation_reference": {},
  "dense_normal_optimization": {
    "parameterization": "sphere_uv_tangent_delta_grid",
    "uv_height": 16,
    "uv_width": 32,
    "active_texels": 64,
    "uses_reflection_cycle_loss": true,
    "init_reflective_error_deg": 0.0,
    "final_reflective_error_deg": 0.0,
    "reflective_error_improvement_percent": 0.0,
    "init_nonreflective_error_deg": 0.0,
    "final_nonreflective_error_deg": 0.0,
    "loss_history": [],
    "accepted_updates": [],
    "lambda_smooth": 0.02,
    "lambda_l2": 0.001,
    "sample_count": 40,
    "seed": 53,
    "loss_seed": 59,
    "update_radius": 1
  },
  "dense_no_cycle_ablation": {
    "uses_reflection_cycle_loss": false,
    "init_reflective_error_deg": 0.0,
    "final_reflective_error_deg": 0.0,
    "reflective_error_improvement_percent": 0.0,
    "loss_history": []
  },
  "texture_baking": {
    "specular_leakage_score": {},
    "albedo_rmse": {}
  },
  "uv_texture_baking": {
    "specular_leakage_score": {},
    "albedo_rmse": {}
  },
  "decision_checks": {
    "loss_correlated_near_gt": true,
    "dense_normal_error_improves_10_percent": true,
    "dense_beats_no_cycle_ablation": true,
    "routing_beats_all_pixels": true,
    "routing_beats_noisy_mask": true,
    "routing_beats_oracle_mask": false
  },
  "phase3": {
    "milestone": "3.2",
    "purpose": "dense_tangent_space_normal_optimization",
    "implemented_dense_normal_optimization": true,
    "implemented_learned_near_field_reflection": false,
    "implemented_inter_reflection_residual": false,
    "implemented_full_pbr_optimization": false,
    "claimed_relighting_or_editing": false
  }
}
```

The exact numeric values are filled by the runner. Placeholder zeros above define schema shape only.

The schema above reflects the current accepted Milestone 3.2 smoke result. If a future action reruns a strict configuration, the summary and logs must clearly distinguish that run from the `sample_count = 40`, `update_radius = 1` result.

`summary.md` must explicitly report:

- whether dense reflective normal error improves by at least 10 percent,
- whether dense reflection-cycle optimization beats the no-cycle dense ablation,
- the exact runner configuration, including UV grid, active texels, dense iterations, sample count, update radius, seed, and loss seed,
- that the current accepted result is a lower-cost smoke diagnostic when `sample_count = 40`,
- that `update_radius = 1` is a local-neighborhood proposal and not strict single-texel coordinate search,
- whether routing beats all-pixel and noisy-mask baselines,
- whether routing beats oracle mask exclusion,
- if oracle mask remains better, the measured reason for continuing or revising,
- whether the dense normal improvement is marginal relative to the 10 percent gate,
- how the dense result compares to the favorable global-rotation reference,
- that the result is still synthetic analytic evidence and not a paper-level claim.

### 7.8 Baselines And Ablations

Required texture/leakage baselines:

- `all_pixels`
- `oracle_mask_exclusion`
- `noisy_mask_only`
- `reflection_confidence_routing`
- `normal_refinement_plus_routing`

Required normal-optimization comparisons:

- `global_rotation_reference`: existing `optimize_global_normal_rotation` behavior from the MVP, rerun with the same dataset and reported as a reference only.
- `dense_no_cycle_ablation`: same dense parameterization and regularization, but without `reflection_cycle_loss`.
- `dense_reflection_cycle_optimizer`: the proposed Milestone 3.2 optimizer using `L_total`.

The dense optimizer is allowed to underperform the global-rotation reference because the global search is intentionally favorable. It must beat the perturbed initialization by at least 10 percent in reflective-region normal error to pass.

### 7.9 Verification Commands

Run:

```bash
pytest refmotion_gs_mvp/tests/test_dense_normal_optimization.py -q
pytest refmotion_gs_mvp/tests/test_phase3_milestone32_runner.py -q
pytest refmotion_gs_mvp/tests -q
python -m py_compile refmotion_gs_mvp/src/*.py refmotion_gs_mvp/scripts/run_mvp_diagnostics.py refmotion_gs_mvp/scripts/run_phase3_milestone31.py refmotion_gs_mvp/scripts/run_phase3_milestone32.py
python refmotion_gs_mvp/scripts/run_phase3_milestone32.py --out-dir refmotion_gs_mvp/outputs/phase3/milestone_32_dense_normals
```

### 7.10 Pass / Revise / Pivot / Stop

Pass Milestone 3.2 if all are true:

- all tests pass,
- Python compilation exits 0,
- the runner writes `metrics.json`, `summary.md`, and `dense_loss_history.png`,
- dense reflective-region normal error improves by at least 10 percent over perturbed initialization,
- dense reflection-cycle optimizer improves more than the no-cycle dense ablation,
- reflection-cycle loss remains correlated with normal correctness,
- routing beats all-pixel and noisy-mask baselines,
- oracle mask exclusion is reported honestly,
- no forbidden component is implemented or claimed.

Revise if any are true:

- dense normal error improves less than 10 percent but loss decreases,
- dense optimizer does not beat no-cycle ablation,
- routing beats all-pixel but not noisy-mask baking,
- output schema or summary is missing required fields,
- runtime is too high for repeatable smoke validation.

Pivot after audit if any are true:

- dense normal optimization cannot improve reflective-region normal error while no-cycle or mask-only baselines explain the texture gains,
- oracle mask exclusion remains stronger and no measured noisy-mask, albedo, seam, or normal-accuracy signal justifies continuing,
- feature correspondences are too ambiguous under dense degrees of freedom.

Stop if either is true:

- reflection-cycle loss no longer correlates with normal correctness on the controlled analytic scene,
- implementing the milestone would require learned near-field reflection fields, inter-reflection residuals, full PBR optimization, relighting, material editing, or representation-novelty claims.

### 7.11 Reviewer-Risk Reporting

Milestone 3.2 summaries must state:

- MaterialRefGS / photometric-variation risk is not fully closed; this milestone tests reflected-ray geometry against internal ablations, not a full MaterialRefGS baseline.
- TextureSplat / texture-only risk is addressed only by preserving texture-only and mask-only leakage baselines.
- SpecTRe-GS and Ref-DGS overlap is avoided because no learned near-field reflection field or local reflection Gaussian is implemented.
- Mask-only threat remains binding; oracle mask exclusion must be reported even if it beats the proposed method.

## 8. Milestone 3.3: Stricter Scene Or Renderer Validation

**Classification:** major validation milestone.

**Audit requirement before implementation:** GPT-5.5 xhigh pre-implementation authorization audit using `PROMPTS/pre_major_milestone_audit_prompt.md`.

**Post-result audit requirement:** GPT-5.5 xhigh full go/no-go audit before treating the stage as accepted evidence.

Purpose:

- Address the analytic reflected-lobe limitation by replacing pure direction-color lobes with explicit finite reflected objects.
- Preserve Formulation A from `outputs/phase2/theory_rewrite.md`: reflection-induced multi-view motion supervises reflective-region normals through reflected-ray geometry.
- Test whether the Milestone 3.2 dense / tangent-space normal signal survives when reflected appearance is generated by analytic near-object ray intersections, not only by a smooth far-field color function.

### 8.1 Current Implementation Path

- `which blender` exited `1` during the Milestone 3.3 pre-implementation audit on 2026-05-15.
- The current implementation path is the analytic near-object fallback.
- Do not block Milestone 3.3 on Blender/Cycles unless the user explicitly provides Blender/Cycles access and `NEXT_ACTION.md` is updated.
- If Blender/Cycles becomes available, amend this plan and rerun the GPT-5.5 xhigh pre-implementation authorization audit before using it.

### 8.2 Scope Lock

Milestone 3.3 must not implement or claim:

- learned near-field reflection fields,
- inter-reflection residuals,
- full PBR optimization,
- relighting or material editing,
- mesh, UV, PBR, or Gaussian representation novelty.

Allowed:

- analytic reflector primitives used only to synthesize observed reflected color and ground-truth diagnostics,
- fixed roughness / reflective masks,
- deterministic geometric ray intersections for a controlled validation scene.

The reflected objects are part of the synthetic data generator, not learned scene components and not a renderer novelty claim.

### 8.3 Analytic Near-Object Scene Design

Create a deterministic near-object reflection dataset whose output is compatible with the existing `AnalyticDataset` data structure.

Primary object:

- sphere centered at the origin with radius `1.0`,
- surface normal is the normalized sphere point,
- base albedo is fixed and low-saturation, matching the existing synthetic scene style,
- reflective mask is deterministic: object pixels with `normal[1] > -0.25`,
- roughness is fixed as `0.05` on reflective pixels and `0.85` elsewhere.

Camera path:

- default `num_views = 6`, `width = 28`, `height = 24`, `seed = 173`,
- cameras use the existing circular `Camera.look_at` convention,
- train/evaluation split is recorded as `train_view_indices = [0, 1, 2, 3]` and `test_view_indices = [4, 5]`,
- if an implementation changes the view count, it must record the exact split in `metrics.json` and `summary.md`.

Reflector primitives:

- use at least three finite colored analytic primitives outside the primary sphere,
- default primitive form is colored sphere intersection because it is deterministic and easy to test,
- planned defaults:
  - red reflector sphere: center `[1.75, 0.10, 1.15]`, radius `0.45`, color `[0.95, 0.10, 0.08]`,
  - green reflector sphere: center `[-1.55, 0.35, 1.35]`, radius `0.40`, color `[0.08, 0.85, 0.18]`,
  - blue reflector sphere: center `[0.15, 1.45, -1.55]`, radius `0.50`, color `[0.12, 0.22, 0.95]`.

Reflection observation rule:

- for each object pixel, compute outgoing direction from surface point to camera center,
- reflect the outgoing direction around the candidate or ground-truth normal,
- intersect that reflected ray against the finite reflector primitives,
- use the nearest positive hit color when a reflector is hit,
- use the existing far-field fallback color only when no finite reflector is hit,
- record `reflector_hit_mask` and `reflector_id` for diagnostics.

This scene is stricter than the current analytic reflected-color lobe scene because small normal changes can alter finite-object hit / miss status, hit identity, and reflected color discontinuities. It still remains a controlled analytic dataset with ground-truth normals, albedo, reflective masks, reflected colors, and deterministic seeds.

### 8.4 Formulation And Optimizer Reuse

Milestone 3.3 must reuse the Milestone 3.2 formulation and optimizer path:

- use `reflection_cycle_loss` as the geometry signal,
- use `make_initial_perturbed_normals` with the same default `8.0` degree perturbation unless the runner records a different value,
- use `optimize_dense_tangent_normals` for the proposed dense reflection-cycle optimizer,
- use `run_dense_no_cycle_ablation` as the dense optimizer without reflection-cycle loss,
- use the existing global-rotation optimizer as a reference baseline,
- use ground-truth normals only for metrics and controlled loss-landscape checks, not for optimizer updates.

Default dense-normal smoke configuration:

- `uv_height = 16`,
- `uv_width = 32`,
- `iterations = 8`,
- `max_active_texels = 64`,
- `sample_count = 50`,
- `loss_seed = 71`,
- `seed = 67`,
- `update_radius = 1`,
- `lambda_smooth = 0.02`,
- `lambda_l2 = 0.001`.

Default loss-landscape configuration:

- evaluate `0deg`, `5deg`, and `10deg` normal perturbations,
- use `sample_count = 140`,
- use `seed = 31`.

### 8.5 Files To Create Or Modify

Create:

- `refmotion_gs_mvp/src/near_object_scene.py`
- `refmotion_gs_mvp/scripts/run_phase3_milestone33.py`
- `refmotion_gs_mvp/tests/test_near_object_scene.py`
- `refmotion_gs_mvp/tests/test_phase3_milestone33_runner.py`

Update only if needed for exports:

- `refmotion_gs_mvp/src/__init__.py`

Do not modify existing Milestone 3.2 metrics, summaries, source files, or experiment outputs while implementing Milestone 3.3 unless a later audit explicitly authorizes a compatibility fix.

### 8.6 Planned Public API

`refmotion_gs_mvp/src/near_object_scene.py` should expose:

```python
@dataclass(frozen=True)
class ReflectorPrimitive:
    center: np.ndarray
    radius: float
    color: np.ndarray

@dataclass(frozen=True)
class NearObjectSceneResult:
    dataset: AnalyticDataset
    reflector_hit_mask: np.ndarray
    reflector_id: np.ndarray
    train_view_indices: list[int]
    test_view_indices: list[int]
    reflectors: tuple[ReflectorPrimitive, ...]

def trace_reflector_color(
    surface_points: np.ndarray,
    reflected_dirs: np.ndarray,
    reflectors: tuple[ReflectorPrimitive, ...],
    fallback_color: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    ...

def generate_near_object_reflection_dataset(
    num_views: int = 6,
    width: int = 28,
    height: int = 24,
    seed: int = 173,
) -> NearObjectSceneResult:
    ...
```

`NearObjectSceneResult.dataset` must be an `AnalyticDataset` so existing loss, optimization, metric, and baking code can run unchanged.

### 8.7 Tests To Add Before Implementation

`refmotion_gs_mvp/tests/test_near_object_scene.py`:

- `test_near_object_scene_is_deterministic_and_has_reflector_hits`
  - generate the dataset twice with identical parameters,
  - assert image, normal, albedo, roughness, mask, reflected-color, and hit-mask arrays match,
  - assert `reflector_hit_fraction` over reflective pixels is at least `0.15`.
- `test_near_object_scene_preserves_refmotion_scope_flags`
  - assert no returned metadata claims learned reflection fields, inter-reflection residuals, full PBR, relighting, or material editing.
- `test_near_object_loss_prefers_ground_truth_normals`
  - compute `reflection_cycle_loss` for ground-truth normals and for an `8.0` degree perturbed initialization,
  - assert ground-truth loss is lower on the near-object dataset with a fixed sample count and seed.

`refmotion_gs_mvp/tests/test_phase3_milestone33_runner.py`:

- run `run_phase3_milestone33.py` into a temporary output directory,
- assert `metrics.json` and `summary.md` are written,
- assert the output schema includes dataset, reflectors, loss landscape, global-rotation reference, dense normal optimization, dense no-cycle ablation, pixel baking, UV baking, decision checks, and Phase 3 scope flags,
- assert `phase3.used_blender_cycles` is `false`,
- assert all forbidden-component flags are `false`,
- assert all required baselines are present:
  - `all_pixels`,
  - `oracle_mask_exclusion`,
  - `noisy_mask_only`,
  - `reflection_confidence_routing`,
  - `normal_refinement_plus_routing`,
  - `dense_no_cycle_ablation`,
  - `dense_reflection_cycle_optimizer`.

### 8.8 Output Contract

Write Milestone 3.3 results under:

```text
refmotion_gs_mvp/outputs/phase3/milestone_33_near_object_scene/
```

Required files:

- `metrics.json`
- `summary.md`
- `dense_loss_history.png`
- `reflector_hit_map.png`

Optional files:

- `leakage_bars.png`
- `loss_landscape.png`

`metrics.json` must include:

```json
{
  "dataset": {
    "scene_type": "analytic_near_object_reflection",
    "num_views": 6,
    "width": 28,
    "height": 24,
    "seed": 173,
    "train_view_indices": [0, 1, 2, 3],
    "test_view_indices": [4, 5],
    "object_pixels": 0,
    "reflective_pixels": 0,
    "reflector_hit_fraction": 0.0
  },
  "reflectors": [
    {"center": [0.0, 0.0, 0.0], "radius": 0.0, "color": [0.0, 0.0, 0.0]}
  ],
  "loss_landscape": {},
  "global_rotation_reference": {},
  "dense_normal_optimization": {},
  "dense_no_cycle_ablation": {},
  "pixel_baking": {},
  "uv_texture_baking": {},
  "decision_checks": {},
  "phase3": {
    "milestone": "3.3",
    "purpose": "stricter_scene_or_renderer_validation",
    "renderer_path": "analytic_near_object_fallback",
    "used_blender_cycles": false,
    "implements_learned_near_field_reflection_field": false,
    "implements_inter_reflection_residual": false,
    "implements_full_pbr_optimization": false,
    "claims_relighting_or_material_editing": false,
    "claims_representation_novelty": false
  }
}
```

The zero values above are schema placeholders only. The runner must write measured values.

`summary.md` must report:

- why analytic near-object fallback was used,
- whether finite reflector hit fraction is sufficient,
- loss-landscape ordering,
- dense normal improvement over perturbed initialization,
- dense reflection-cycle optimizer versus dense no-cycle ablation,
- routing versus all-pixel, noisy-mask, and oracle-mask baselines,
- whether oracle-mask exclusion remains stronger,
- all forbidden-component flags,
- pass / revise / pivot / stop recommendation.

### 8.9 Baseline Preservation

Milestone 3.3 must preserve and report:

- all-pixel baking,
- oracle mask-only baking / oracle mask exclusion,
- noisy mask-only baking,
- reflection-confidence routing,
- normal-refinement-plus-routing,
- global normal rotation reference,
- dense optimizer without reflection-cycle loss,
- dense reflection-cycle optimizer.

Oracle mask exclusion must remain an honest comparator. Beating all-pixel and noisy-mask baselines is not enough for a strong claim if oracle mask exclusion is still better.

### 8.10 Verification Commands

Implementation verification must run:

```bash
pytest refmotion_gs_mvp/tests/test_near_object_scene.py -q
pytest refmotion_gs_mvp/tests/test_phase3_milestone33_runner.py -q
pytest refmotion_gs_mvp/tests -q
python -m py_compile refmotion_gs_mvp/src/*.py refmotion_gs_mvp/scripts/run_mvp_diagnostics.py refmotion_gs_mvp/scripts/run_phase3_milestone31.py refmotion_gs_mvp/scripts/run_phase3_milestone32.py refmotion_gs_mvp/scripts/run_phase3_milestone33.py
python refmotion_gs_mvp/scripts/run_phase3_milestone33.py --out-dir refmotion_gs_mvp/outputs/phase3/milestone_33_near_object_scene
jq empty refmotion_gs_mvp/outputs/phase3/milestone_33_near_object_scene/metrics.json
```

### 8.11 Decision Gates

Pass to post-result xhigh go/no-go audit if all are true:

- tests and verification commands pass,
- `reflector_hit_fraction >= 0.15` on reflective pixels,
- reflection-cycle loss remains correlated with normal correctness on `0deg`, `5deg`, and `10deg` perturbations,
- reflective-region normal error improves by at least `10%` over the perturbed initialization,
- dense reflection-cycle optimizer beats dense no-cycle ablation on reflective-region normal error,
- normal-refinement-plus-routing beats all-pixel baking,
- normal-refinement-plus-routing beats noisy-mask-only baking,
- oracle mask exclusion is reported honestly whether it wins or loses,
- all forbidden-component flags remain false.

Revise and rerun the milestone if any are true:

- tests pass but `reflector_hit_fraction < 0.15`,
- dense normal improvement is positive but below `10%`,
- output schema, summary, or plots are incomplete,
- runtime exceeds a practical smoke-test budget and can be reduced without changing scope.

Pivot after audit if any are true:

- dense normal optimization does not improve reflective-region normal error while no-cycle or mask-only baselines explain the texture gains,
- oracle mask exclusion remains stronger and no measured noisy-mask, albedo, seam, or normal-accuracy signal justifies continuing,
- explicit finite reflected objects make feature correspondences too ambiguous for Formulation A under the current data regime.

Stop if either is true:

- reflection-cycle loss no longer correlates with normal correctness on the stricter analytic near-object scene,
- implementing the milestone would require learned near-field reflection fields, inter-reflection residuals, full PBR optimization, relighting, material editing, or representation-novelty claims.

### 8.12 Reviewer-Risk Coverage

Milestone 3.3 summaries must state:

- MaterialRefGS / photometric-variation risk is still not fully closed because this is a controlled analytic validation, not a MaterialRefGS baseline.
- TextureSplat / texture-only risk is addressed only through retained texture-only, mask-only, and routing baselines.
- SpecTRe-GS and Ref-DGS overlap is avoided because no learned near-field reflection field or local reflection Gaussian is introduced.
- The stricter-scene result is evidence for RefMotion-GS geometry supervision only if it preserves the loss-correlation, normal-improvement, and routing-baseline gates above.

### 8.13 Implementation Sequence

Use test-first implementation:

1. Add failing tests in `test_near_object_scene.py` and `test_phase3_milestone33_runner.py` for determinism, reflector-hit fraction, loss preference for ground-truth normals, output schema, baseline coverage, and scope flags.
2. Implement `near_object_scene.py` with deterministic reflector primitives and `NearObjectSceneResult`.
3. Implement `run_phase3_milestone33.py` by reusing Milestone 3.2 optimization, baking, metrics, plotting, and decision-check patterns.
4. Run the verification commands in section 8.10.
5. Write `outputs/phase3/milestone_33_near_object_scene/summary.md`, update `IMPLEMENTATION_LOG.md`, update `DECISION_LOG.md`, and update `NEXT_ACTION.md` to the post-result xhigh go/no-go audit only after verification completes.

### 8.14 Milestone 3.3 Revision: Dense-Normal Gate Failure Diagnostics

**Classification:** small diagnostic revision to a major validation milestone.

**Reason for revision:** the Milestone 3.3 post-result full audit returned `GO AFTER REVISION`. The analytic near-object fallback is reproducible and in scope, but the dense reflection-cycle optimizer improved reflective-region normal error by only `0.7685068728508346%`, below the required `10%` gate. The dense objective decreased from `0.014386876237571697` to `0.010304391097315124`, so the revision must determine whether objective descent is aligned with normal correctness under dense tangent-space variables.

This revision is diagnostic and bounded. It must not implement a learned near-field reflection field, inter-reflection residual, full PBR optimization, relighting, material editing, or any representation-novelty claim. It must not replace Formulation A. It must not treat a noisy-mask or all-pixel win as enough for a strong claim when oracle mask exclusion remains stronger.

#### 8.14.1 Evidence To Preserve

The revision starts from the existing Milestone 3.3 result:

- `reflector_hit_fraction`: `0.15492957746478872`.
- loss landscape:
  - `0deg`: `0.01518530465164876`,
  - `5deg`: `0.015862829735769086`,
  - `10deg`: `0.01802097308944506`.
- dense reflection-cycle optimizer:
  - initial reflective error: `5.710456219994247` deg,
  - final reflective error: `5.666570971472453` deg,
  - improvement: `0.7685068728508346%`,
  - final non-reflective error: `6.27701088254727` deg.
- global rotation reference:
  - final reflective error: `2.4356515786729616` deg,
  - improvement: `57.347513318727174%`.
- UV leakage:
  - all pixels: `0.9658763096531678`,
  - oracle mask exclusion: `0.17595366303189766`,
  - noisy mask-only: `0.5556875799054598`,
  - reflection-confidence routing: `0.4632458373229172`,
  - normal-refinement-plus-routing: `0.4714538905111631`.

The current output shows normal-refinement-plus-routing is worse than reflection-confidence routing on leakage. Future summaries must state this explicitly.

#### 8.14.2 Reflector Primitive Reconciliation

The pre-implementation plan listed reflector radii `0.45`, `0.40`, and `0.50`, but the implemented Milestone 3.3 result used radii `0.765`, `0.68`, and `0.85`. The revision must not hide this mismatch.

For the revision, treat the implemented radii as the recorded Milestone 3.3 diagnostic scene because they produced the audited output and met the minimum finite-hit gate. The revision summary must report:

- implemented centers and radii exactly as stored in `metrics.json`,
- why the larger radii are used: to obtain a minimum finite-reflector hit fraction in a low-resolution smoke scene,
- that `reflector_hit_fraction = 0.15492957746478872` is barely above the gate and not a strong realism claim,
- whether the observed dense-normal failure may be sensitive to finite-hit coverage.

Do not retune reflector geometry during this revision unless the revision implementation records the retuned geometry in a separate output directory and does not overwrite the audited Milestone 3.3 output.

#### 8.14.3 Files To Create Or Modify

Create:

- `refmotion_gs_mvp/src/phase3_revision_diagnostics.py`
- `refmotion_gs_mvp/scripts/run_phase3_milestone33_revision.py`
- `refmotion_gs_mvp/tests/test_phase3_revision_diagnostics.py`
- `refmotion_gs_mvp/tests/test_phase3_milestone33_revision_runner.py`

Write outputs under:

```text
refmotion_gs_mvp/outputs/phase3/milestone_33_revision_diagnostics/
```

Required output files:

- `metrics.json`
- `summary.md`
- `objective_vs_normal_error.png`
- `reflector_hit_coverage_by_texel.png`

Optional output files:

- `nonreflective_drift.png`
- `routing_leakage_comparison.png`

Do not modify during this revision:

- `refmotion_gs_mvp/outputs/phase3/milestone_33_near_object_scene/metrics.json`
- `refmotion_gs_mvp/outputs/phase3/milestone_33_near_object_scene/summary.md`
- `refmotion_gs_mvp/outputs/phase3/milestone_32_dense_normals/`
- `refmotion_gs_mvp/outputs/run_latest/`

Modify only if needed to support diagnostics:

- `refmotion_gs_mvp/src/dense_normal_optimization.py`
- `refmotion_gs_mvp/scripts/run_phase3_milestone33.py`

Any modification to existing source must preserve current Milestone 3.2 and 3.3 behavior by default.

#### 8.14.4 Required Diagnostic API

`refmotion_gs_mvp/src/phase3_revision_diagnostics.py` must expose:

```python
@dataclass(frozen=True)
class DenseTrajectoryDiagnostics:
    objective_history: list[float]
    reflective_error_history: list[float]
    nonreflective_error_history: list[float]
    reflective_improvement_history: list[float]
    objective_reflective_error_correlation: float | None
    accepted_update_count: int
    worsened_reflective_update_count: int

@dataclass(frozen=True)
class CoverageDiagnostics:
    reflector_hit_fraction: float
    active_texel_count: int
    active_texel_hit_fraction_mean: float
    active_texel_hit_fraction_min: float
    active_texels_without_finite_hits: int

def replay_dense_updates_for_diagnostics(
    dataset: AnalyticDataset,
    initial_normals: np.ndarray,
    accepted_updates: list[dict],
    uv_height: int,
    uv_width: int,
) -> DenseTrajectoryDiagnostics:
    ...

def compute_reflector_hit_coverage_by_texel(
    scene: NearObjectSceneResult,
    uv_height: int,
    uv_width: int,
    active_texels: list[tuple[int, int]],
) -> CoverageDiagnostics:
    ...
```

Implementation notes:

- Reconstruct dense normal deltas by replaying `accepted_updates` from zero deltas.
- Use the same local-neighborhood semantics as `update_radius` in `dense_normal_optimization.py`.
- Compute reflective and non-reflective angular error after each accepted update.
- Compute `objective_reflective_error_correlation` only when at least three paired samples exist and both series have nonzero variance; otherwise record `null` in JSON.
- Count an accepted update as worsened if reflective-region normal error increases relative to the previous accepted state.
- Compute finite-reflector hit coverage only over reflective object pixels.

#### 8.14.5 Runner Requirements

`refmotion_gs_mvp/scripts/run_phase3_milestone33_revision.py` must:

1. Regenerate the deterministic near-object scene using the existing Milestone 3.3 defaults.
2. Rerun the existing Milestone 3.3 dense reflection-cycle optimizer with the same default smoke configuration:
   - `uv_height = 16`,
   - `uv_width = 32`,
   - `dense_iterations = 8`,
   - `max_active_texels = 64`,
   - `sample_count = 50`,
   - `seed = 67`,
   - `loss_seed = 71`,
   - `update_radius = 1`.
3. Recompute the existing texture and UV baselines or import them from a fresh in-process Milestone 3.3 run; do not rely on stale JSON alone.
4. Write `metrics.json` with these top-level sections:
   - `dataset`,
   - `reflectors`,
   - `baseline_milestone33_decision_checks`,
   - `dense_trajectory_diagnostics`,
   - `coverage_diagnostics`,
   - `routing_diagnostics`,
   - `phase3`,
   - `recommendation`.
5. Write `summary.md` with evidence, inference, decision, and next action.

`routing_diagnostics` must include:

```json
{
  "uv_leakage": {
    "all_pixels": 0.0,
    "oracle_mask_exclusion": 0.0,
    "noisy_mask_only": 0.0,
    "reflection_confidence_routing": 0.0,
    "normal_refinement_plus_routing": 0.0
  },
  "normal_refinement_improves_over_reflection_confidence": false,
  "normal_refinement_beats_noisy_mask": true,
  "normal_refinement_beats_oracle_mask": false
}
```

The exact values above are placeholders for schema shape only. The runner must write measured values.

#### 8.14.6 Tests

Add tests before implementation:

- `tests/test_phase3_revision_diagnostics.py::test_dense_update_replay_reports_error_trajectory`
  - generate a small near-object scene,
  - create perturbed normals,
  - run the dense optimizer with reduced settings,
  - replay accepted updates,
  - assert history lengths match `accepted_update_count + 1`,
  - assert all reflective and non-reflective errors are finite,
  - assert `worsened_reflective_update_count` is an integer greater than or equal to zero.

- `tests/test_phase3_revision_diagnostics.py::test_reflector_hit_coverage_reports_active_texel_support`
  - generate the default near-object scene,
  - compute active texels from reflective observations,
  - compute coverage diagnostics,
  - assert `reflector_hit_fraction >= 0.15`,
  - assert `active_texel_count > 0`,
  - assert `0.0 <= active_texel_hit_fraction_min <= active_texel_hit_fraction_mean <= 1.0`.

- `tests/test_phase3_milestone33_revision_runner.py::test_milestone33_revision_runner_schema_and_scope`
  - run the revision runner into a temporary directory with reduced settings,
  - assert `metrics.json`, `summary.md`, `objective_vs_normal_error.png`, and `reflector_hit_coverage_by_texel.png` are written,
  - assert top-level schema sections are present,
  - assert forbidden-component flags remain false,
  - assert `routing_diagnostics.normal_refinement_improves_over_reflection_confidence` is present,
  - assert the summary states that oracle mask exclusion remains an honest comparator.

#### 8.14.7 Verification Commands

Run:

```bash
pytest refmotion_gs_mvp/tests/test_phase3_revision_diagnostics.py -q
pytest refmotion_gs_mvp/tests/test_phase3_milestone33_revision_runner.py -q
pytest refmotion_gs_mvp/tests -q
python -m py_compile refmotion_gs_mvp/src/*.py refmotion_gs_mvp/scripts/run_mvp_diagnostics.py refmotion_gs_mvp/scripts/run_phase3_milestone31.py refmotion_gs_mvp/scripts/run_phase3_milestone32.py refmotion_gs_mvp/scripts/run_phase3_milestone33.py refmotion_gs_mvp/scripts/run_phase3_milestone33_revision.py
python refmotion_gs_mvp/scripts/run_phase3_milestone33_revision.py --out-dir refmotion_gs_mvp/outputs/phase3/milestone_33_revision_diagnostics
jq empty refmotion_gs_mvp/outputs/phase3/milestone_33_revision_diagnostics/metrics.json
```

Expected:

- all tests pass,
- Python compilation exits `0`,
- the revision runner writes the required files,
- no forbidden-component flags are true,
- `summary.md` explicitly states whether dense objective descent aligned with reflective-region normal improvement,
- `summary.md` explicitly states whether normal-refinement-plus-routing is worse than reflection-confidence routing,
- `summary.md` explicitly reports oracle mask exclusion status.

#### 8.14.8 Pass / Revise / Pivot / Stop

Pass the revision if all are true:

- verification commands pass,
- required revision output files are written,
- dense trajectory diagnostics explain whether objective descent aligns with reflective normal correctness,
- reflector-hit coverage diagnostics report active-texel finite-hit support,
- routing diagnostics explicitly compare normal-refinement-plus-routing with reflection-confidence routing, noisy-mask-only, and oracle mask exclusion,
- all forbidden-component flags remain false,
- no existing Milestone 3.2 or audited Milestone 3.3 result files are overwritten.

Revise again if any are true:

- diagnostics are incomplete or not reproducible,
- trajectory history cannot be reconstructed from accepted updates,
- coverage metrics are missing active texel support,
- summaries omit oracle mask exclusion or the reflection-confidence routing comparison.

Pivot after audit if any are true:

- objective descent is anti-correlated with reflective-region normal correctness or repeatedly worsens normal error,
- finite-reflector hit coverage is too sparse to support dense normal supervision even after reporting active-texel coverage,
- normal-refinement-plus-routing remains worse than reflection-confidence routing and oracle mask exclusion, with no normal-accuracy evidence justifying further dense-normal work.

Stop if either is true:

- reflection-cycle loss no longer correlates with normal correctness under the regenerated revision run,
- further progress would require learned near-field reflection fields, inter-reflection residuals, full PBR optimization, relighting, material editing, or representation-novelty claims.

#### 8.14.9 Audit Requirement After Revision

This revision is a small diagnostic revision to a major validation milestone. After implementation:

- run a short audit using `PROMPTS/short_audit_prompt.md`,
- do not treat Milestone 3.3 as accepted evidence until the short audit passes,
- if the short audit finds pivot or stop evidence, update `NEXT_ACTION.md` to a GPT-5.5 xhigh go/no-go / pivot decision.

## 9. Reviewer-Risk Coverage

MaterialRefGS / photometric variation:

- Phase 3 summaries must state that current evidence is geometric reflected-ray correspondence, not a comparison against MaterialRefGS.
- A future baseline should compare reflected-ray geometry against a photometric-variation-only routing score before paper claims.

SpecTRe-GS and Ref-DGS:

- Phase 3 must continue avoiding learned local reflection fields and near-field ray-traced rendering claims.
- The contribution remains supervision and leakage diagnosis, not near-field reflection rendering.

TextureSplat / texture-only threat:

- Phase 3 must keep texture-only and mask-only baselines.
- Any UV or atlas result is an evaluation surface, not a novelty claim.

Mask-only threat:

- Every Phase 3 result summary must report whether the method beats noisy mask and whether it beats oracle mask.
- If oracle mask remains better, continuation must be justified only by noisy-mask robustness, normal accuracy, UV seam behavior, or another explicitly measured signal.

## 10. Current P0 Fix Status

This plan resolves the P0 planning fixes from `outputs/phase3/full_go_no_go.md` by defining:

- Milestone 3.1 as experiment framework refactor only.
- Milestone 3.2 as dense / tangent-space normal optimization only after 3.1 passes.
- Exact files to create or modify for Milestone 3.1.
- Exact output directories and result-summary filenames.
- Exact tests to add before implementation.
- Exact verification commands.
- The required baseline suite and decision checks.
- The scope lock against forbidden components.
- How the plan addresses oracle-mask leakage, global-rotation optimizer favorability, analytic renderer limitations, MaterialRefGS, and TextureSplat.
- The Milestone 3.2 P0 implementation subplan required by `outputs/phase3/milestone_32_preimplementation_audit.md`, including exact parameterization, regularization, optimizer settings, tests, outputs, baselines, and decision gates.
- The Milestone 3.3 P0 implementation subplan required by `outputs/phase3/milestone_33_preimplementation_audit.md`, including the analytic near-object fallback path, scene design, public API, tests, output schema, verification commands, baselines, and decision gates.
- The Milestone 3.3 post-result audit revision subplan required by `outputs/phase3/milestone_33_post_result_audit.md`, including dense trajectory diagnostics, active-texel finite-reflector coverage diagnostics, routing comparison diagnostics, reflector primitive reconciliation, verification commands, and pass / revise / pivot / stop gates.

## 11. Next Workflow Step

Rerun the GPT-5.5 xhigh Milestone 3.3 pre-implementation authorization audit using `PROMPTS/pre_major_milestone_audit_prompt.md`.

If the audit returns `APPROVED TO IMPLEMENT` or `APPROVED WITH REQUIRED FIXES` with no P0 blockers:

- update `NEXT_ACTION.md` to begin Milestone 3.3 implementation only.

If the audit returns `BLOCKED UNTIL PLAN FIXES`:

- revise this plan and rerun the pre-implementation authorization audit.
