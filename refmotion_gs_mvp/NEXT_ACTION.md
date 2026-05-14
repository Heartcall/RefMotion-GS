# RefMotion-GS Next Action

## Current Next Action

**Start or resume this work in a GPT-5.5 xhigh session, then run the major-stage audit using refmotion_gs_mvp/PROMPTS/full_xhigh_audit_prompt.md. Audit whether Milestone 3.2 dense / tangent-space normal optimization from refmotion_gs_mvp/PHASE3_PLAN.md is sufficiently specified, inside RefMotion-GS scope, and safe to begin. Do not implement Milestone 3.2 until the audit verdict is APPROVED or APPROVED WITH REQUIRED FIXES and all P0 fixes are resolved.**

## Action Type

Major-stage audit.

## Required Prompt

`PROMPTS/full_xhigh_audit_prompt.md`

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

## Completed Phase 3 Audit Verdict

`PLAN APPROVED WITH REQUIRED FIXES`

Audit report:

`outputs/phase3/full_go_no_go.md`

P0 planning repair file:

`PHASE3_PLAN.md`

Short audit report:

`outputs/phase3/phase3_plan_short_audit.md`

Step 1 red-test evidence:

`pytest refmotion_gs_mvp/tests/test_decision_checks.py -q` exited 2 with `ModuleNotFoundError: No module named 'refmotion_gs_mvp.src.decision_checks'`.

Step 2 green-test evidence:

`pytest refmotion_gs_mvp/tests/test_decision_checks.py -q` passed with `2 passed in 0.01s` after adding `refmotion_gs_mvp/src/decision_checks.py`.

Step 3 red-test evidence:

`pytest refmotion_gs_mvp/tests/test_experiment_protocol.py -q` exited 2 with `ModuleNotFoundError: No module named 'refmotion_gs_mvp.src.experiment_protocol'`.

Step 4 green-test evidence:

`pytest refmotion_gs_mvp/tests/test_experiment_protocol.py -q` passed with `2 passed in 0.02s` after adding `refmotion_gs_mvp/src/experiment_protocol.py`; `python -m py_compile refmotion_gs_mvp/src/experiment_protocol.py` exited 0.

Step 5 runner evidence:

`python refmotion_gs_mvp/scripts/run_phase3_milestone31.py --out-dir refmotion_gs_mvp/outputs/phase3/milestone_31_framework` exited 0, wrote `metrics.json` and `summary.md`, preserved the existing MVP metric sections from `outputs/run_latest/metrics.json`, and recorded `implemented_dense_normal_optimization: false` plus `implemented_learned_near_field_reflection: false`.

Step 6 full-verification evidence:

`pytest refmotion_gs_mvp/tests -q` passed with `20 passed in 9.59s`; `python -m py_compile refmotion_gs_mvp/src/*.py refmotion_gs_mvp/scripts/run_mvp_diagnostics.py refmotion_gs_mvp/scripts/run_phase3_milestone31.py` exited 0; `python refmotion_gs_mvp/scripts/run_phase3_milestone31.py --out-dir refmotion_gs_mvp/outputs/phase3/milestone_31_framework` exited 0 and preserved the required baseline suite, decision checks, summary, and Phase 3 forbidden-component flags.

Milestone 3.1 short-audit evidence:

`outputs/phase3/milestone_31_short_audit.md` records verdict `PASS`; Milestone 3.1 is accepted, but `routing_beats_oracle_mask` remains false and Milestone 3.2 must not begin without a GPT-5.5 xhigh major-stage audit.

Major-stage audit gate evidence:

The continue-current-work gate was checked in a session that was not explicitly started as GPT-5.5 xhigh. Per `PROMPTS/continue_current_work_prompt.md`, the major-stage audit was not run, and this file was updated to request a GPT-5.5 xhigh audit session explicitly.

## Phase 3 Audit Question

Is the proposed Phase 3 plan still inside RefMotion-GS scope, and does it directly address the unresolved MVP weakness that routing nearly matches but does not beat oracle mask exclusion on leakage?

## Milestone Numbering Convention

Use this convention unless a future `PHASE3_PLAN.md` explicitly overrides it:

- Milestone 3.1: Experiment framework refactor.
- Milestone 3.2: Dense / tangent-space normal optimization.

## Candidate Next Action After Audit

Only after the P0 planning fixes are resolved:

Candidate Milestone 3.2: create a stricter normal-optimization milestone that replaces `optimize_global_normal_rotation` with a per-surface or tangent-space normal-map diagnostic while keeping Formulation A, current baselines, and analytic reproducibility.

Candidate Milestone 3.2 must not introduce learned near-field reflection fields, inter-reflection residuals, full PBR optimization, relighting, or material editing.

## Minimum Verification For Candidate Milestone 3.2

```bash
pytest refmotion_gs_mvp/tests -q
python -m py_compile refmotion_gs_mvp/src/*.py refmotion_gs_mvp/scripts/run_mvp_diagnostics.py
python refmotion_gs_mvp/scripts/run_mvp_diagnostics.py --out-dir refmotion_gs_mvp/outputs/run_latest
```

If Candidate Milestone 3.2 adds a new diagnostic runner, also run it into a dedicated output directory and write a markdown summary beside its metrics.

## Required End State

At the end of the next session:

- update `IMPLEMENTATION_LOG.md`,
- update or create a Phase 3 result summary,
- update `DECISION_LOG.md`,
- update this file with the next exact task,
- run short audit for a small milestone or GPT-5.5 xhigh full audit for a major stage.
