# RefMotion-GS Full Go/No-Go Audit

## Verdict

PIVOT

The Milestone 3.3 diagnostic revision is reproducible, in scope, and useful as evidence, but it does not justify further dense-normal optimization implementation as the next project track. The revision confirms the same central failure from the earlier Milestone 3.3 audit: dense objective descent does not translate into meaningful reflective-region dense normal improvement in the current finite-object scene.

This is not a stop decision because the reflection-cycle loss still orders ground-truth normals better than perturbed normals, routing still beats all-pixel and noisy-mask baselines, and an in-scope fallback direction exists. It is a pivot decision because the dense-normal path now satisfies the pivot triggers in `PHASE3_PLAN.md` section 8.14.8.

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
- `refmotion_gs_mvp/outputs/phase3/milestone_33_post_result_audit.md`
- `refmotion_gs_mvp/outputs/phase3/milestone_33_revision_short_audit.md`
- `refmotion_gs_mvp/outputs/phase3/milestone_33_revision_diagnostics/metrics.json`
- `refmotion_gs_mvp/outputs/phase3/milestone_33_revision_diagnostics/summary.md`
- `refmotion_gs_mvp/src/phase3_revision_diagnostics.py`
- `refmotion_gs_mvp/src/dense_normal_optimization.py`
- `refmotion_gs_mvp/src/near_object_scene.py`
- `refmotion_gs_mvp/scripts/run_phase3_milestone33.py`
- `refmotion_gs_mvp/scripts/run_phase3_milestone33_revision.py`
- `refmotion_gs_mvp/tests/test_near_object_scene.py`
- `refmotion_gs_mvp/tests/test_phase3_milestone33_runner.py`
- `refmotion_gs_mvp/tests/test_phase3_revision_diagnostics.py`
- `refmotion_gs_mvp/tests/test_phase3_milestone33_revision_runner.py`
- `outputs/phase2/theory_rewrite.md`
- `outputs/phase2/reviewer_attack.md`
- `outputs/phase2/core_contribution_reduction.md`
- `outputs/phase2/final_go_no_go.md`

Fresh verification commands:

```bash
pytest refmotion_gs_mvp/tests/test_phase3_revision_diagnostics.py -q
pytest refmotion_gs_mvp/tests/test_phase3_milestone33_revision_runner.py -q
pytest refmotion_gs_mvp/tests -q
python -m py_compile refmotion_gs_mvp/src/*.py refmotion_gs_mvp/scripts/*.py
python refmotion_gs_mvp/scripts/run_phase3_milestone33_revision.py --out-dir /tmp/refmotion_gs_mvp_m33_revision_audit
jq empty refmotion_gs_mvp/outputs/phase3/milestone_33_revision_diagnostics/metrics.json
jq empty /tmp/refmotion_gs_mvp_m33_revision_audit/metrics.json
diff -q refmotion_gs_mvp/outputs/phase3/milestone_33_revision_diagnostics/metrics.json /tmp/refmotion_gs_mvp_m33_revision_audit/metrics.json
```

Observed:

- Revision diagnostics tests: `2 passed in 1.92s`.
- Revision runner test: `1 passed in 2.80s`.
- Full test suite: `31 passed in 61.60s`.
- Python compilation: exit code `0`.
- Temporary revision runner: exit code `0`, printed `revise: dense trajectory diagnostics explain the failed 10 percent normal gate`.
- `jq empty` on saved revision `metrics.json`: exit code `0`.
- `jq empty` on temporary rerun `metrics.json`: exit code `0`.
- `diff -q` between saved and temporary rerun `metrics.json`: exit code `0`.

## Pass/Fail Table

| Criterion | Status | Evidence |
|---|---|---|
| Scope discipline | PASS | Saved revision flags are false for learned near-field reflection fields, inter-reflection residuals, full PBR optimization, relighting/material editing, and representation-novelty claims. |
| Formulation A compliance | PASS | The revision keeps the reflected-ray / reflection-cycle diagnostic path and does not introduce a learned reflection field. |
| Gradient/evidence path | FAIL FOR DENSE-NORMAL CONTINUATION | Objective decreases from `0.014386876237571697` to `0.010304391097315124`, but reflective-region normal error changes only from `5.710456219994247` deg to `5.666570971472453` deg. |
| Baseline preservation | PASS | All-pixel, oracle mask exclusion, noisy mask-only, reflection-confidence routing, normal-refinement-plus-routing, dense no-cycle ablation, and dense reflection-cycle optimizer remain present. |
| Mask-only threat | FAIL FOR METHOD CLAIM | Oracle mask exclusion leakage is `0.17595366303189766`; normal-refinement-plus-routing leakage is `0.4714538905111631`. |
| Normal evidence | FAIL | Final reflective-region dense normal improvement is `0.7685068728508346%`, far below the required `10%` gate. |
| Texture evidence | PARTIAL | Normal-refinement-plus-routing beats all-pixel and noisy-mask leakage but is worse than reflection-confidence routing and far worse than oracle mask exclusion. |
| Renderer / scene validity | PARTIAL | `reflector_hit_fraction` is `0.15492957746478872`, barely above the `0.15` gate, and `34` of `64` active texels have zero finite-reflector hits. |
| Tests | PASS | Targeted revision tests and the full suite passed in this audit. |
| Reproducibility | PASS | The runner reproduced byte-identical metrics in `/tmp/refmotion_gs_mvp_m33_revision_audit`. |
| Reviewer-risk coverage | FAIL FOR PAPER CLAIM | The evidence does not overcome mask-only, MaterialRefGS / photometric-variation, or texture-only objections. It only supports a diagnostic benchmark direction. |
| Claim discipline | PASS | The revision summary does not claim relighting, material editing, full PBR, representation novelty, or paper-level success. |

## Major Findings

1. The diagnostic revision is technically complete, but it strengthens the case against continuing the current dense-normal optimization track. It reconstructs the accepted-update trajectory and shows that `5` of `8` accepted dense objective updates worsen reflective-region normal error.

2. The objective signal is not absent, but it is too weak and misaligned for the current claim. A positive correlation of `0.29366840127375765` between objective and reflective error means lower objective tends to align only weakly with lower error, while the final improvement remains below `1%`.

3. Active finite-reflector support is too sparse for a confident dense-normal supervision claim in this scene. `34` of `64` active texels have no finite reflector hits, the mean active-texel hit fraction is `0.17395833333333333`, and the minimum is `0.0`.

4. Normal refinement does not improve the routing result. Normal-refinement-plus-routing leakage is `0.4714538905111631`, worse than reflection-confidence routing at `0.4632458373229172` and far worse than oracle mask exclusion at `0.17595366303189766`.

5. The method still has residual diagnostic value. Loss ordering remains correct near ground truth, the runner is reproducible, and routing beats all-pixel and noisy-mask baselines. That supports pivoting to a benchmark / leakage-metric direction rather than stopping the project.

6. Further dense-normal implementation would be a research detour unless the formulation or scene is substantially redesigned. Such a redesign would need a new plan and audit, not another incremental optimizer tweak.

## Required Revisions

- P0: Do not implement more dense-normal optimization code from the current Milestone 3.3 track.
- P0: Treat Milestone 3.3 revision as accepted diagnostic evidence, not as validation that the dense-normal method works.
- P0: Pivot planning must define a narrower RefMotion-GS direction centered on diagnostic benchmark and leakage metrics for reflective reconstruction, using the existing evidence and baselines.
- P0: The pivot plan must preserve the strict scope guard: no learned near-field reflection field, no inter-reflection residual, no full PBR optimization, no relighting or material editing claims, and no representation-novelty framing.
- P1: Keep the dense-normal failure evidence in future writeups so the project does not silently revert to an unsupported normal-refinement claim.
- P1: If dense normals are ever revisited, require a new pre-implementation audit with a substantially different scene/formulation and explicit acceptance gates.

## Decision

- Verdict: `PIVOT`.
- The project should pivot away from further dense-normal optimizer implementation under the current Phase 3 setup.
- The project should not stop because the existing synthetic infrastructure, Formulation A diagnostics, leakage metrics, and baseline comparisons remain useful.
- The next action is planning only: write a pivot plan for a benchmark / leakage-metric direction using GPT-5.5 high.

## Next Action

Create a RefMotion-GS pivot plan for the benchmark / leakage-metric direction. The plan must convert the current evidence into a bounded next phase that evaluates reflective reconstruction failures, texture leakage, mask-only baselines, and reflection-motion diagnostics without claiming dense-normal optimization success.
