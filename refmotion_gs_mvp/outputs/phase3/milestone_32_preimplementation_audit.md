# Milestone 3.2 Pre-Implementation Authorization Audit

## Verdict

BLOCKED UNTIL PLAN FIXES

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
  - `refmotion_gs_mvp/src/decision_checks.py`
  - `refmotion_gs_mvp/src/experiment_protocol.py`
  - `refmotion_gs_mvp/scripts/run_mvp_diagnostics.py`
  - `refmotion_gs_mvp/scripts/run_phase3_milestone31.py`
  - `refmotion_gs_mvp/tests/test_feature_matching_and_losses.py`
  - `refmotion_gs_mvp/tests/test_normal_optimization_and_baking.py`

## Pass/Fail Table

| Criterion | Status | Evidence |
|---|---|---|
| Scope compliance | PASS | `ACTIVE_SCOPE.md` and `PHASE3_PLAN.md` keep the active project as RefMotion-GS and explicitly exclude learned near-field reflection fields, inter-reflection residuals, full PBR optimization, relighting, material editing, and representation-novelty claims. |
| Formulation compliance | PASS WITH REQUIRED DETAIL | `outputs/phase2/theory_rewrite.md` defines Formulation A with optional tangent-space normal maps and reflected-ray geometry. `PHASE3_PLAN.md` says Milestone 3.2 must keep Formulation A, but it does not yet specify exactly how the dense normal variables enter the existing reflected-ray loss path. |
| Implementation readiness | FAIL | `PHASE3_PLAN.md` lists required pre-implementation details for Milestone 3.2, including exact normal-update parameterization, smoothness/regularization terms, sampling count and seeds, comparison to global rotation, and result schema, but it does not define those details. |
| Test readiness | FAIL | The plan does not name Milestone 3.2 test files, test functions, red/green sequence, or expected assertions for dense/tangent normal optimization. |
| Baseline preservation | PASS WITH REQUIRED DETAIL | The plan preserves all MVP texture/leakage baselines and decision checks, but it does not specify the dense optimizer ablation without reflection-cycle loss or explain why that ablation is unnecessary. |
| Metric and output readiness | FAIL | Minimum metrics are listed, but the exact `metrics.json` schema, summary sections, output directory, and machine-readable decision checks for Milestone 3.2 are not specified. |
| Decision gates | PASS WITH REQUIRED DETAIL | Phase-level continue/revise/pivot/stop gates exist, and Milestone 3.2 lists minimum metrics. The plan still needs Milestone 3.2-specific pass/revise/pivot criteria tied to those metrics and outputs. |
| Reviewer-risk coverage | PASS WITH REQUIRED DETAIL | The plan names MaterialRefGS, SpecTRe-GS, Ref-DGS, TextureSplat, and mask-only risks. Milestone 3.2 still needs an explicit ablation and reporting plan that separates reflected-ray geometry from photometric-variation and texture-only explanations. |
| Code-change safety | PASS | This audit did not implement Milestone 3.2 code and did not change source, scripts, or tests. |

## Findings

1. Milestone 3.2 is conceptually in scope. A dense or tangent-space normal diagnostic is allowed because it tests whether reflection-induced multi-view motion supervises reflective-region normals under less favorable degrees of freedom.

2. Implementation is not authorized because the plan is under-specified at the exact point that the plan itself marks as mandatory. `PHASE3_PLAN.md` says exact parameterization, regularization, sampling, seed, comparison, and schema details are required before implementation, but it leaves them as requirements rather than decisions.

3. The existing implementation is still a global normal-rotation diagnostic. `src/normal_optimization.py` only exposes `optimize_global_normal_rotation`, and the current passing tests validate global rotation rather than dense or tangent-space normal variables.

4. Formulation A remains the correct formulation boundary. `outputs/phase2/theory_rewrite.md` explicitly allows optional tangent-space normal maps and says normal changes should affect reflected-ray geometry, while avoiding learned reflection fields. The Milestone 3.2 plan must bind implementation to that path.

5. The mask-only objection remains central. Milestone 3.1 preserves the result that `routing_beats_oracle_mask` is false, with oracle mask leakage `0.18894842742715495` versus normal-refinement-plus-routing leakage `0.19090032877604535`. Milestone 3.2 must keep oracle-mask reporting and explain any continuation only through measured noisy-mask robustness, albedo, seam, or normal-accuracy evidence.

## Required Fixes

- P0: Add a dedicated Milestone 3.2 implementation subplan to `PHASE3_PLAN.md`.
- P0: Define the dense / tangent-space normal parameterization exactly, including shape, coordinate frame, initialization from perturbed normals, unit-normal projection, and how the variables update `normals` passed into `reflection_cycle_loss`.
- P0: Define smoothness or regularization terms exactly, including neighborhood definition, mask behavior, weight names/defaults, and whether regularization applies only to reflective/object pixels or all object pixels.
- P0: Define the optimizer family, iteration count, step sizes or learning rate, deterministic seeds, sampling count, and acceptance/update rule.
- P0: Define all files to create or modify for Milestone 3.2 and explicitly keep source changes out of forbidden components.
- P0: Define tests before implementation, including at least one loss-ordering or normal-error test for the dense/tangent optimizer, one schema/baseline test, and one guardrail test showing forbidden components remain absent.
- P0: Define the Milestone 3.2 output directory and exact `metrics.json` / `summary.md` schema.
- P0: Define the baseline and ablation suite, including all existing MVP baselines and either a dense optimizer without reflection-cycle loss or an explicit, evidence-based justification for omitting that ablation.
- P0: Define Milestone 3.2-specific pass/revise/pivot/stop criteria. At minimum, reflective-region normal error must improve by at least 10 percent over perturbed initialization, reflection-cycle loss must remain correlated with normal correctness, routing must beat all-pixel and noisy-mask baselines, and oracle mask exclusion must be reported honestly.
- P1: State how the Milestone 3.2 summary will address MaterialRefGS / photometric-variation, TextureSplat / texture-only, SpecTRe-GS / Ref-DGS, and mask-only objections without claiming relighting, editing, full PBR, or representation novelty.

## Authorization Decision

- Milestone 3.2 implementation is not authorized yet.
- The correct next action is a planning repair, not experiment code.
- The project should not pivot or stop: the MVP signal remains unfalsified, Milestone 3.1 passed, and the planned Milestone 3.2 direction is in scope once the P0 specification gaps are closed.

## Next Action

- Update `PHASE3_PLAN.md` with the Milestone 3.2 P0 implementation subplan listed above.
- Do not implement Milestone 3.2 code during that planning repair.
- After the planning repair, rerun the Milestone 3.2 pre-implementation authorization audit using GPT-5.5 xhigh.
