# Pre-Implementation Authorization Audit

## Verdict

APPROVED TO IMPLEMENT

## Evidence Reviewed

- `refmotion_gs_mvp/AGENTS.md`
- `refmotion_gs_mvp/ACTIVE_SCOPE.md`
- `refmotion_gs_mvp/OPERATING_PROTOCOL.md`
- `refmotion_gs_mvp/NEXT_ACTION.md`
- `refmotion_gs_mvp/PROMPTS/continue_current_work_prompt.md`
- `refmotion_gs_mvp/PROMPTS/pre_major_milestone_audit_prompt.md`
- `refmotion_gs_mvp/PHASE3_PLAN.md`
- `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`
- `refmotion_gs_mvp/MVP_RESULTS.md`
- `refmotion_gs_mvp/DECISION_LOG.md`
- `refmotion_gs_mvp/outputs/phase3/milestone_31_short_audit.md`
- `refmotion_gs_mvp/outputs/phase3/milestone_31_framework/summary.md`
- `refmotion_gs_mvp/outputs/phase3/milestone_31_framework/metrics.json`
- `outputs/phase2/theory_rewrite.md`
- `outputs/phase2/reviewer_attack.md`
- `outputs/phase2/core_contribution_reduction.md`
- Context-only source and tests:
  - `refmotion_gs_mvp/src/losses.py`
  - `refmotion_gs_mvp/src/normal_optimization.py`
  - `refmotion_gs_mvp/src/uv_baking.py`
  - `refmotion_gs_mvp/src/decision_checks.py`
  - `refmotion_gs_mvp/src/experiment_protocol.py`
  - `refmotion_gs_mvp/scripts/run_phase3_milestone31.py`
  - current test file list under `refmotion_gs_mvp/tests/`

## Pass/Fail Table

| Criterion | Status | Evidence |
|---|---|---|
| Scope compliance | PASS | `ACTIVE_SCOPE.md` and `PHASE3_PLAN.md` keep the project as RefMotion-GS and explicitly exclude learned near-field reflection fields, inter-reflection residuals, full PBR optimization, relighting, material editing, and representation-novelty claims. |
| Formulation compliance | PASS | `outputs/phase2/theory_rewrite.md` defines Formulation A with optional tangent-space normal maps. `PHASE3_PLAN.md` binds Milestone 3.2 to the same path by composing `n_opt = normalize(n_init + a * t1 + b * t2)` and passing the composed normals into `reflection_cycle_loss`, which uses reflected directions and reflected-ray candidate matching. |
| Implementation readiness | PASS | `PHASE3_PLAN.md` defines dense grid shape, tangent frame construction, initialization, clipping, smoothness/L2 regularization, deterministic coordinate-search settings, active texel selection, files to create, outputs, verification commands, and completion/failure criteria. |
| Test readiness | PASS | The plan names `test_dense_normal_optimization.py` and `test_phase3_milestone32_runner.py` with unit-length, 10 percent reflective-error improvement, no-cycle ablation, schema, baseline, and forbidden-component assertions. |
| Baseline preservation | PASS | The plan preserves all-pixel baking, oracle mask exclusion, noisy mask-only baking, reflection-confidence routing, normal-refinement-plus-routing, the global-rotation reference, a dense no-cycle ablation, and the proposed dense reflection-cycle optimizer. |
| Metric and output readiness | PASS | The plan specifies `outputs/phase3/milestone_32_dense_normals/`, `metrics.json`, `summary.md`, `dense_loss_history.png`, required metric sections, phase flags, and machine-readable decision checks. |
| Decision gates | PASS | Milestone 3.2 pass/revise/pivot/stop gates are explicit: dense reflective-region normal error must improve at least 10 percent, the dense reflection-cycle optimizer must beat the no-cycle ablation, loss correlation must remain valid, routing must beat all-pixel and noisy-mask baselines, oracle mask exclusion must be reported honestly, and forbidden components remain stop conditions. |
| Reviewer-risk coverage | PASS | The plan keeps mask-only and texture-only baselines, preserves oracle-mask reporting, states MaterialRefGS is not fully closed by this milestone, and avoids SpecTRe-GS / Ref-DGS overlap by forbidding learned near-field reflection fields and local reflection Gaussians. |
| Code-change safety | PASS | This audit did not implement Milestone 3.2 code and did not modify source, scripts, or tests. |

## Findings

1. The previous P0 blockers are resolved. The earlier audit was blocked because Milestone 3.2 lacked exact parameterization, regularization, optimizer settings, tests, output schema, and ablations. `PHASE3_PLAN.md` now specifies those items in Sections 7.2 through 7.10.

2. The milestone remains inside the reduced RefMotion-GS scope. It tests whether reflection-induced multi-view motion can supervise reflective-region normals under denser degrees of freedom. It does not add learned near-field reflection fields, inter-reflection residuals, full PBR optimization, relighting, material editing, or representation-novelty claims.

3. The formulation path is sufficiently bound to Formulation A. Dense tangent coefficients change surface normals, and those normals are passed into the existing `reflection_cycle_loss` reflected-ray geometry path. The plan does not authorize a learned reflection field or a post-hoc texture-only filter as the core signal.

4. The implementation plan is concrete enough for a GPT-5.5 high implementation session to proceed without inventing major method details. Minor API names inside `dense_normal_optimization.py` can be chosen during test-first implementation because the plan fixes the behavior, schema, and verification commands.

5. The baseline and decision gates are appropriately skeptical. The plan preserves oracle mask exclusion and requires a no-cycle dense ablation, so a future result cannot claim success from dense degrees of freedom or mask-only behavior alone.

## Required Fixes

- P0: none.
- P1: During implementation, keep public helper names small and test-driven so the new dense normal module remains auditable.
- P1: In the Milestone 3.2 summary, explicitly state that MaterialRefGS / photometric-variation risk is not fully closed unless a later baseline is added.

## Authorization Decision

- Milestone 3.2 is authorized for implementation.
- Implementation must be limited to Milestone 3.2 from `PHASE3_PLAN.md`.
- Use GPT-5.5 high for implementation.
- Do not implement experiment code beyond the planned dense / tangent-space normal optimization diagnostic, runner, tests, and result outputs.
- After implementation and verification, because Milestone 3.2 is a major method-validation milestone, update `NEXT_ACTION.md` to require a GPT-5.5 xhigh post-result audit before accepting the milestone.

## Next Action

- Implement Milestone 3.2 dense / tangent-space normal optimization using `refmotion_gs_mvp/PROMPTS/milestone_implementation_prompt.md`.
- Start with the planned tests in `refmotion_gs_mvp/tests/test_dense_normal_optimization.py` and `refmotion_gs_mvp/tests/test_phase3_milestone32_runner.py`.
- Run the verification commands specified in `PHASE3_PLAN.md`.
