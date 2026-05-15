# RefMotion-GS Full Go/No-Go Audit

## Verdict

GO AFTER REVISION

Milestone 3.2 produced valid in-scope evidence that dense / tangent-space normal optimization can improve reflective-region normals under Formulation A, and the texture-routing gates still beat all-pixel and noisy-mask baselines. The result is not clean enough to advance to Milestone 3.3 without revision because the produced runner configuration diverges from the audited plan in two material ways: the recorded output uses `sample_count = 40` instead of the planned `250`, and the runner uses `update_radius = 1` local-neighborhood proposals while the plan describes single-texel coordinate updates.

## Evidence Reviewed

- `refmotion_gs_mvp/AGENTS.md`
- `refmotion_gs_mvp/ACTIVE_SCOPE.md`
- `refmotion_gs_mvp/OPERATING_PROTOCOL.md`
- `refmotion_gs_mvp/PROJECT_PLAN.md`
- `refmotion_gs_mvp/PHASE3_PLAN.md`
- `refmotion_gs_mvp/NEXT_ACTION.md`
- `refmotion_gs_mvp/PROMPTS/full_xhigh_audit_prompt.md`
- `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`
- `refmotion_gs_mvp/MVP_RESULTS.md`
- `refmotion_gs_mvp/DECISION_LOG.md`
- `refmotion_gs_mvp/outputs/phase3/milestone_31_short_audit.md`
- `refmotion_gs_mvp/outputs/phase3/milestone_32_preimplementation_audit.md`
- `refmotion_gs_mvp/outputs/phase3/milestone_32_dense_normals/metrics.json`
- `refmotion_gs_mvp/outputs/phase3/milestone_32_dense_normals/summary.md`
- `refmotion_gs_mvp/src/dense_normal_optimization.py`
- `refmotion_gs_mvp/scripts/run_phase3_milestone32.py`
- `refmotion_gs_mvp/tests/test_dense_normal_optimization.py`
- `refmotion_gs_mvp/tests/test_phase3_milestone32_runner.py`
- `outputs/phase2/theory_rewrite.md`
- `outputs/phase2/reviewer_attack.md`
- `outputs/phase2/core_contribution_reduction.md`

## Pass/Fail Table

| Criterion | Status | Evidence |
|---|---|---|
| Scope discipline | PASS | The implementation stays inside RefMotion-GS. Phase flags report no learned near-field reflection field, inter-reflection residual, full PBR optimization, relighting, or editing claim. |
| Formulation A | PASS | `compose_dense_normals` applies sphere-UV tangent coefficients to object normals, and `optimize_dense_tangent_normals` passes those normals into `reflection_cycle_loss`. Dense normals affect reflected-ray geometry, not a learned reflection field. |
| Gradient/evidence path | PASS | Dense objective decreases from `0.007726688423605768` to `0.0034211424395956553`, and reflective normal error improves from `5.663940679902162` to `5.0236136352350576` degrees. |
| Baselines | PASS | Metrics include all-pixel baking, oracle mask exclusion, noisy mask-only baking, reflection-confidence routing, normal-refinement-plus-routing, global-rotation reference, dense no-cycle ablation, and dense reflection-cycle optimizer. |
| Mask-only threat | PASS WITH CAUTION | Routing beats all-pixel and noisy-mask leakage, but oracle mask exclusion remains much stronger: `0.18623485108324137` versus `0.35270156748629633`. |
| Normal evidence | PASS WITH CAUTION | Dense reflective normal error improves by `11.305327524690204` percent, barely above the 10 percent gate. The global-rotation reference remains much stronger at `67.41279022743005` percent improvement. |
| Texture evidence | PASS WITH CAUTION | Normal-refinement-plus-routing leakage improves over all-pixel `0.9841678157561735` and noisy-mask `0.47305854764111854`, but not oracle mask exclusion. |
| Renderer validity | PASS WITH CAUTION | Evidence remains analytic synthetic evidence. It is valid for this controlled diagnostic, not a paper-level result. |
| Tests | PASS | Fresh verification: targeted dense tests `3 passed`, runner schema test `1 passed`, full suite `24 passed`. |
| Reproducibility | PASS WITH REVISION | Fresh runner execution rewrote `metrics.json`, `summary.md`, and `dense_loss_history.png` and reproduced the same decision-check pattern. Configuration mismatch with the plan must be resolved. |
| Reviewer risks | PASS WITH CAUTION | Summary reports MaterialRefGS is not fully closed, TextureSplat risk is covered only by texture/mask baselines, and SpecTRe-GS/Ref-DGS overlap is avoided by not adding local reflection fields. |
| Claim discipline | PASS | No paper-level success, relighting, editing, full PBR, or representation-novelty claim is made. |
| Plan/result consistency | FAIL UNTIL REVISED | The planned output schema lists `sample_count = 250`, but the accepted run records `40`. The plan describes per-texel coordinate proposals, but the accepted run records `update_radius = 1`. |

## Major Findings

1. Milestone 3.2 is not falsified. The reflection-cycle dense optimizer improves reflective-region normal error by more than 10 percent and beats the dense no-cycle ablation, whose final reflective error remains unchanged at `5.663940679902162` degrees.

2. The evidence is positive but narrow. The dense improvement is only `11.305327524690204` percent, just above the gate, while the earlier global-rotation diagnostic remains far stronger. This supports continuing with caution, not upgrading claims.

3. The mask-only threat remains binding. The method adds value over all-pixel and noisy-mask baselines, but oracle mask exclusion remains substantially better on leakage. Any future continuation must be justified through noisy-mask robustness, normal accuracy, seam behavior, or stricter scene evidence, not by claiming oracle-mask superiority.

4. The implementation stays within the reduced scope. No learned near-field reflection field, inter-reflection residual, full PBR optimization, relighting, material editing, or representation-novelty path appears in the new source, script, tests, metrics, or summary.

5. The result cannot be accepted as-is because the planned protocol and executed protocol are misaligned. The function default still supports `sample_count = 250` and `update_radius = 0`, but the result-producing runner uses `sample_count = 40` and `update_radius = 1`. That change may be a reasonable smoke-validation choice, but it must be explicitly authorized, explained, and recorded before the milestone is accepted.

## Required Revisions

- P0: Resolve the `sample_count` mismatch. Either rerun and report Milestone 3.2 with the planned `sample_count = 250`, or revise `PHASE3_PLAN.md` and the result summary to state that the accepted Milestone 3.2 run is a lower-cost smoke configuration with `sample_count = 40` and that stronger sampling is deferred.
- P0: Resolve the `update_radius` mismatch. Either rerun the result-producing command with strict single-texel proposals (`update_radius = 0`), or revise `PHASE3_PLAN.md` to explicitly authorize local-neighborhood proposals, explain why they remain a deterministic dense tangent-space coordinate search, and report `update_radius` in the summary.
- P0: Update the Milestone 3.2 result summary to state that the dense normal improvement is marginal, the global-rotation reference remains much stronger, and oracle mask exclusion remains substantially better on leakage.
- P1: Add a reproducibility note in the plan or summary that records the final runner configuration: UV grid, active texels, dense iterations, sample count, local proposal radius, seeds, and output path.

## Decision

- Verdict: GO AFTER REVISION.
- Do not begin Milestone 3.3 yet.
- Milestone 3.2 implementation may remain as the current candidate result, but acceptance requires the P0 plan/result documentation repair above and then an audit of the repaired state.

## Next Action

- Repair the Milestone 3.2 plan/result documentation inconsistencies using GPT-5.5 high.
- Do not implement new experiment code or begin Milestone 3.3 during that repair.
