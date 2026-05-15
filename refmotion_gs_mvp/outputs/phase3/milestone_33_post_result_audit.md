# RefMotion-GS Full Go/No-Go Audit

## Verdict

GO AFTER REVISION

Milestone 3.3 is reproducible and remains inside RefMotion-GS scope, but it does not pass the major validation gate. The analytic near-object scene preserves loss correlation and the dense reflection-cycle optimizer beats the no-cycle ablation, yet reflective-region dense normal error improves by only `0.7685068728508346%`, far below the required `10%` gate. Normal-refinement-plus-routing also remains much worse than oracle mask exclusion on leakage.

This is not a stop decision because the loss still correlates with normal correctness, the dense optimizer improves slightly over initialization, and no forbidden component is required. It is not a pivot decision yet because the result is a narrow but positive signal with clear revision targets. It is not a go decision because the stricter finite-object validation failed the normal-improvement gate.

## Evidence Reviewed

- `refmotion_gs_mvp/AGENTS.md`
- `refmotion_gs_mvp/ACTIVE_SCOPE.md`
- `refmotion_gs_mvp/OPERATING_PROTOCOL.md`
- `refmotion_gs_mvp/NEXT_ACTION.md`
- `refmotion_gs_mvp/PROJECT_PLAN.md`
- `refmotion_gs_mvp/PHASE3_PLAN.md`
- `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`
- `refmotion_gs_mvp/MVP_RESULTS.md`
- `refmotion_gs_mvp/DECISION_LOG.md`
- `refmotion_gs_mvp/outputs/phase3/milestone_33_preimplementation_audit.md`
- `refmotion_gs_mvp/outputs/phase3/milestone_33_near_object_scene/metrics.json`
- `refmotion_gs_mvp/outputs/phase3/milestone_33_near_object_scene/summary.md`
- `refmotion_gs_mvp/outputs/phase3/milestone_32_revision_short_audit.md`
- `refmotion_gs_mvp/outputs/phase3/milestone_32_dense_normals/metrics.json`
- `refmotion_gs_mvp/outputs/phase3/milestone_32_dense_normals/summary.md`
- `outputs/phase2/theory_rewrite.md`
- `outputs/phase2/reviewer_attack.md`
- `outputs/phase2/core_contribution_reduction.md`
- `outputs/phase2/anti_cheating_constraints.md`
- `outputs/phase2/final_go_no_go.md`
- `outputs/phase2/novelty_audit.md`
- `refmotion_gs_mvp/src/near_object_scene.py`
- `refmotion_gs_mvp/src/dense_normal_optimization.py`
- `refmotion_gs_mvp/scripts/run_phase3_milestone33.py`
- `refmotion_gs_mvp/tests/test_near_object_scene.py`
- `refmotion_gs_mvp/tests/test_phase3_milestone33_runner.py`

Fresh verification commands:

```bash
pytest refmotion_gs_mvp/tests/test_near_object_scene.py -q
pytest refmotion_gs_mvp/tests/test_phase3_milestone33_runner.py -q
python -m py_compile refmotion_gs_mvp/src/near_object_scene.py refmotion_gs_mvp/src/dense_normal_optimization.py refmotion_gs_mvp/scripts/run_phase3_milestone33.py
jq empty refmotion_gs_mvp/outputs/phase3/milestone_33_near_object_scene/metrics.json
pytest refmotion_gs_mvp/tests -q
python -m py_compile refmotion_gs_mvp/src/*.py refmotion_gs_mvp/scripts/run_mvp_diagnostics.py refmotion_gs_mvp/scripts/run_phase3_milestone31.py refmotion_gs_mvp/scripts/run_phase3_milestone32.py refmotion_gs_mvp/scripts/run_phase3_milestone33.py
python refmotion_gs_mvp/scripts/run_phase3_milestone33.py --out-dir refmotion_gs_mvp/outputs/phase3/milestone_33_near_object_scene
jq empty refmotion_gs_mvp/outputs/phase3/milestone_33_near_object_scene/metrics.json
```

Observed:

- Targeted near-object scene tests: `3 passed in 1.56s`.
- Targeted Milestone 3.3 runner test: `1 passed in 8.90s`.
- Full test suite: `28 passed in 61.46s`.
- Python compilation commands: exit code `0`.
- Milestone 3.3 runner: exit code `0`.
- `jq empty` on Milestone 3.3 `metrics.json`: exit code `0`.
- Runner decision checks:
  - `loss_correlated_near_gt`: `true`.
  - `reflector_hit_fraction_sufficient`: `true`.
  - `dense_normal_error_improves_10_percent`: `false`.
  - `dense_beats_no_cycle_ablation`: `true`.
  - `routing_beats_all_pixels`: `true`.
  - `routing_beats_noisy_mask`: `true`.
  - `routing_beats_oracle_mask`: `false`.

## Pass/Fail Table

| Criterion | Status | Evidence |
|---|---|---|
| Scope discipline | PASS | Forbidden-component flags are all false: no learned near-field reflection field, inter-reflection residual, full PBR optimization, relighting/material editing, or representation-novelty claim. |
| Formulation A compliance | PASS | Milestone 3.3 reuses `reflection_cycle_loss`, dense tangent-space normals, global-rotation reference, and no-cycle dense ablation. |
| Gradient/evidence path | FAIL FOR ACCEPTANCE | Dense objective decreases from `0.014386876237571697` to `0.010304391097315124`, but reflective normal error improves only from `5.710456219994247` deg to `5.666570971472453` deg. |
| Baseline preservation | PASS | All-pixel, oracle mask exclusion, noisy mask-only, reflection-confidence routing, normal-refinement-plus-routing, global rotation reference, dense no-cycle, and dense reflection-cycle optimizer are present. |
| Mask-only threat | FAIL FOR ACCEPTANCE | Oracle mask exclusion leakage is `0.17595366303189766`; normal-refinement-plus-routing leakage is `0.4714538905111631`. |
| Normal evidence | FAIL | Dense reflective-region normal improvement is `0.7685068728508346%`, below the required `10%` gate. |
| Texture evidence | PARTIAL | Routing beats all-pixel and noisy-mask baselines, but not oracle mask exclusion. Normal-refinement-plus-routing is also slightly worse than reflection-confidence routing on leakage. |
| Renderer validity | PARTIAL | The finite-reflector analytic fallback is stricter than far-field lobes and passes the minimum hit gate, but `reflector_hit_fraction` is only `0.15492957746478872`, barely above `0.15`. |
| Tests | PASS | Targeted tests and full suite passed in the fresh audit run. |
| Reproducibility | PASS | Runner regenerated the output directory and JSON validation passed. |
| Reviewer-risk coverage | PARTIAL | SpecTRe-GS and Ref-DGS overlap is avoided by not learning reflection fields, but MaterialRefGS / photometric-variation and mask-only objections remain unresolved. |
| Claim discipline | PASS | The summary does not claim relighting, material editing, full PBR, representation novelty, or paper-level success. |

## Major Findings

1. Milestone 3.3 is an executable in-scope diagnostic, not an accepted validation result. The source, runner, tests, and outputs are reproducible, but the required dense-normal gate fails.

2. The central dense-normal result is too weak for a go decision. The dense optimizer lowers the reflection-cycle objective substantially, but reflective-region normal error improves by less than one percent and non-reflective error worsens from `6.101541691089956` deg to `6.27701088254727` deg. This suggests the objective descent is not reliably aligned with dense normal correctness in the finite-object scene.

3. The no-cycle ablation does not explain the small normal improvement. The dense reflection-cycle optimizer ends at `5.666570971472453` deg reflective error, while the no-cycle ablation remains at `5.710456219994247` deg. This keeps the signal from being falsified, but it is far below the planned acceptance threshold.

4. The favorable global-rotation reference remains much stronger. It improves reflective error by `57.347513318727174%`, ending at `2.4356515786729616` deg, while the dense optimizer reaches only `0.7685068728508346%` improvement. The gap reinforces that dense degrees of freedom are still not controlled well enough.

5. Texture routing evidence remains partial. Normal-refinement-plus-routing beats all-pixel and noisy-mask baselines, but oracle mask exclusion remains much better. Normal refinement also does not improve leakage over reflection-confidence routing in the Milestone 3.3 output.

6. The finite-reflector setup is only marginally above the visibility gate. `reflector_hit_fraction` is `0.15492957746478872`, just above the `0.15` threshold. The implemented reflector radii are larger than the planned defaults recorded in `PHASE3_PLAN.md`, so the next revision should either justify and record the implemented primitives in the plan or retune the scene with an explicit coverage rationale.

7. The result does not justify paper-level claims. It supports only a narrower diagnostic conclusion: finite analytic reflected objects preserve loss ordering and show a tiny dense-normal signal, but the signal is not yet strong enough to pass the major validation gate.

## Required Revisions

- P0: Do not accept Milestone 3.3 as passing. Treat the current result as `GO AFTER REVISION`.
- P0: Add a focused Milestone 3.3 revision plan before further implementation. The plan must define exact diagnostics, files, commands, and gates for the failed dense-normal improvement result.
- P0: The revision must measure whether dense objective updates actually align with normal correctness. Required diagnostics should include normal-error trajectory across accepted dense updates, objective-versus-normal-error correlation, active texel / reflector-hit coverage, non-reflective normal drift, and comparison against reflection-confidence routing without normal refinement.
- P0: The revision must explicitly handle the reflector primitive mismatch between planned defaults and implemented radii, and must report why the finite-hit fraction is sufficient rather than tuned only to clear the threshold.
- P0: After the revision implementation, rerun the Milestone 3.3 verification commands and require another post-result audit before moving to paper writing or any stronger claim.
- P1: Update future summaries to state when normal-refinement-plus-routing is worse than reflection-confidence routing, not only whether it beats all-pixel and noisy-mask baselines.
- P1: Keep oracle mask exclusion as a first-class comparator in every revised output and do not treat noisy-mask wins as enough for a strong claim.

## Decision

- Verdict: `GO AFTER REVISION`.
- Milestone 3.3 implementation is reproducible and in scope.
- Milestone 3.3 is not accepted because the dense-normal improvement gate failed.
- The project should not pivot or stop yet because loss correlation survives, dense optimization improves slightly over initialization and no-cycle, and no forbidden method is required.
- The next action must be a planning repair for a focused Milestone 3.3 revision, using GPT-5.5 high. Do not implement new experiment code in the audit session.

## Next Action

Run a Milestone 3.3 revision planning repair. Update `PHASE3_PLAN.md` with an exact revision subplan for the failed dense-normal gate, including diagnostics, files, metrics, verification commands, decision gates, and scope guards. Do not implement revision code until the planning repair is complete.
