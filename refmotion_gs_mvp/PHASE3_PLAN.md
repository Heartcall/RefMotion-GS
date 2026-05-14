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

**Audit requirement before implementation:** GPT-5.5 xhigh full or targeted go/no-go audit.

Milestone 3.2 must not start until Milestone 3.1 passes and is audited.

Purpose:

- Replace the favorable global rotation search with a less favorable per-surface or tangent-space normal diagnostic.
- Keep Formulation A and the baseline suite unchanged.
- Show whether reflective normal error still improves under denser normal degrees of freedom.

Required plan before implementation:

- Exact parameterization of the normal update.
- Exact smoothness or regularization terms.
- Exact sampling count and seeds.
- Exact comparison to global-rotation evidence.
- Exact result schema extending the Milestone 3.1 schema.

Minimum metrics:

- reflective-region normal angular error before and after,
- non-reflective normal angular error before and after,
- reflection-cycle loss history,
- all texture/leakage baseline metrics,
- `routing_beats_all_pixels`,
- `routing_beats_noisy_mask`,
- `routing_beats_oracle_mask`.

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

## 11. Next Workflow Step

Run a short audit of this plan using `PROMPTS/short_audit_prompt.md`.

If the short audit passes:

- update `NEXT_ACTION.md` to begin Milestone 3.1 implementation only.

If the short audit fails:

- revise this plan and rerun the short audit.

