# RefMotion-GS Next Action

## Current Next Action

**Run Phase 3 planning audit or begin Milestone 3.1 only after plan audit passes.**

## Action Type

Planning audit first.

## Required Startup Reads

1. `ACTIVE_SCOPE.md`
2. `OPERATING_PROTOCOL.md`
3. `PROJECT_PLAN.md`
4. `IMPLEMENTATION_LOG.md`
5. `MVP_RESULTS.md`
6. `DECISION_LOG.md`
7. `outputs/phase2/final_go_no_go.md`
8. `outputs/phase2/theory_rewrite.md`
9. `outputs/phase2/reviewer_attack.md`
10. Current source/tests/scripts under `refmotion_gs_mvp/`

## Phase 3 Audit Question

Is the proposed Phase 3 plan still inside RefMotion-GS scope, and does it directly address the unresolved MVP weakness that routing nearly matches but does not beat oracle mask exclusion on leakage?

## Candidate Milestone 3.1

Only after the Phase 3 plan audit passes:

Create a stricter normal-optimization milestone that replaces `optimize_global_normal_rotation` with a per-surface or tangent-space normal-map diagnostic while keeping Formulation A, current baselines, and analytic reproducibility.

Milestone 3.1 must not introduce learned near-field reflection fields, inter-reflection residuals, full PBR optimization, relighting, or material editing.

## Minimum Verification For Milestone 3.1

```bash
pytest refmotion_gs_mvp/tests -q
python -m py_compile refmotion_gs_mvp/src/*.py refmotion_gs_mvp/scripts/run_mvp_diagnostics.py
python refmotion_gs_mvp/scripts/run_mvp_diagnostics.py --out-dir refmotion_gs_mvp/outputs/run_latest
```

If Milestone 3.1 adds a new diagnostic runner, also run it into a dedicated output directory and write a markdown summary beside its metrics.

## Required End State

At the end of the next session:

- update `IMPLEMENTATION_LOG.md`,
- update or create a Phase 3 result summary,
- update `DECISION_LOG.md`,
- update this file with the next exact task,
- run short audit for a small milestone or GPT-5.5 xhigh full audit for a major stage.

