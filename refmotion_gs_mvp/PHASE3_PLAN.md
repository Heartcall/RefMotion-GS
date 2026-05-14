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
sample_count = 250
loss_seed = 59
```

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

Active texels:

- rank texels by count of reflective object pixels mapped to that texel,
- optimize the top `max_active_texels` texels,
- keep all other texels fixed at zero for the first Milestone 3.2 diagnostic.

Per iteration:

1. Evaluate current `L_total`.
2. For each active texel, each tangent channel, and signs `[-1, +1]`, try one step.
3. Compose normals, normalize, evaluate `L_total`.
4. Accept the single best candidate if it improves objective.
5. If no candidate improves objective, halve the step.
6. Stop early if `step < min_step`.

Record:

- `loss_history`,
- accepted update `(iteration, texel_y, texel_x, channel, step, loss)`,
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
    "sample_count": 250,
    "seed": 53,
    "loss_seed": 59
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

`summary.md` must explicitly report:

- whether dense reflective normal error improves by at least 10 percent,
- whether dense reflection-cycle optimization beats the no-cycle dense ablation,
- whether routing beats all-pixel and noisy-mask baselines,
- whether routing beats oracle mask exclusion,
- if oracle mask remains better, the measured reason for continuing or revising,
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

**Audit requirement before implementation:** GPT-5.5 xhigh go/no-go audit.

Purpose:

- Address the analytic reflected-lobe limitation.
- Prefer Blender/Cycles if available.
- If Blender remains unavailable, implement a more explicit analytic near-object reflection scene without learned reflection fields.

Required:

- Keep ground-truth normals, albedo, roughness or reflective masks.
- Keep all baselines.
- Preserve deterministic seeds and output summaries.

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

## 11. Next Workflow Step

Run a GPT-5.5 xhigh Milestone 3.2 pre-implementation authorization audit using `PROMPTS/pre_major_milestone_audit_prompt.md`.

If the audit returns `APPROVED TO IMPLEMENT` or `APPROVED WITH REQUIRED FIXES` with no P0 blockers:

- update `NEXT_ACTION.md` to begin Milestone 3.2 implementation only.

If the audit returns `BLOCKED UNTIL PLAN FIXES`:

- revise this plan and rerun the pre-implementation authorization audit.
