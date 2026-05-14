# RefMotion-GS Decision Log

This log records project decisions that future Codex sessions must preserve unless new evidence justifies a change.

## 2026-05-14: Scope Reduction Accepted

**Evidence:**

- `outputs/phase2/novelty_audit.md` identifies the full RefTex-GS package as over-combined.
- `outputs/phase2/core_contribution_reduction.md` identifies reflection-motion supervision as the defensible core.
- `outputs/phase2/final_go_no_go.md` recommends continuing only after reduction.

**Decision:**

Continue as RefMotion-GS, not full RefTex-GS.

**Implication:**

Future work must not implement learned near-field reflection fields, inter-reflection residuals, full PBR optimization, relighting, or material editing as first-paper scope.

## 2026-05-14: Analytic Renderer Fallback Accepted For MVP

**Evidence:**

- `IMPLEMENTATION_LOG.md` records that `blender` was unavailable on `PATH`.
- `PROJECT_PLAN.md` allows an analytic synthetic renderer fallback for Milestone 1.
- Existing tests and diagnostics run on `generate_analytic_dataset`.

**Decision:**

Use the analytic renderer for the first MVP path, while treating Blender/Cycles or a more explicit near-object analytic scene as stricter Phase 3 validation.

**Implication:**

Analytic results can support continue-with-caution decisions, but cannot support a final paper-level claim.

## 2026-05-14: Preliminary MVP Continue With Caution

**Evidence:**

- `MVP_RESULTS.md` reports monotonic loss increase from 0 to 10 degree normal perturbations.
- Reflective normal error improved from 5.7091979244066104 degrees to 0.3569152456956942 degrees in the constrained global-offset diagnostic.
- Sphere-UV leakage improved from all-pixel `0.8937587779761458` and noisy-mask `0.48688553583972904` to normal-refinement-plus-routing `0.19090032877604535`.
- Oracle mask exclusion leakage was still slightly better at `0.18894842742715495`.

**Decision:**

Continue the MVP, but only to stricter validation. Do not claim the method beats mask-only under ideal masks.

**Implication:**

Phase 3 must test value beyond simple exclusion, especially under noisy masks, UV seams, denser normal degrees of freedom, and stronger synthetic reflection realism.

## 2026-05-14: Persistent Internal Workflow Created

**Evidence:**

- `AGENTS.md`, `OPERATING_PROTOCOL.md`, `ACTIVE_SCOPE.md`, `NEXT_ACTION.md`, and `PROMPTS/*.md` define a resumable Codex workflow.

**Decision:**

Future sessions should read `ACTIVE_SCOPE.md` and `NEXT_ACTION.md` first, execute the current planning or implementation task, run verification, audit the result, update logs, and write the next exact action.

**Implication:**

The user should not need to restate the project prompt unless a stop condition is reached.

## 2026-05-14: Continue-Current-Work Xhigh Gate Fixed

**Evidence:**

- `PROMPTS/continue_current_work_prompt.md` now explicitly distinguishes xhigh and non-xhigh sessions for major-stage audits.
- `NEXT_ACTION.md` now makes the Phase 3 planning audit executable in a GPT-5.5 xhigh session instead of only stating a gate.

**Decision:**

Fixed the continue-current-work gate so that an xhigh session runs required major-stage audits instead of stopping merely because an xhigh audit is required.

**Implication:**

Future xhigh sessions should run `PROMPTS/full_xhigh_audit_prompt.md` or a dedicated Phase 3 audit prompt when `NEXT_ACTION.md` requires a major-stage audit.

## 2026-05-14: Phase 3 Planning Audit Completed

**Evidence:**

- `refmotion_gs_mvp/outputs/phase3/full_go_no_go.md` records the Phase 3 planning audit.
- No dedicated `PHASE3_PLAN.md` or equivalent Phase 3 plan file was present before the audit.
- MVP metrics still show the reduced hypothesis is not falsified, but normal-refinement plus routing does not beat oracle mask exclusion on leakage.

**Decision:**

The Phase 3 concept is **PLAN APPROVED WITH REQUIRED FIXES**. Implementation remains blocked until P0 planning fixes are resolved.

**Implication:**

The next action is to create a dedicated Phase 3 plan, with Milestone 3.1 as experiment framework refactor and Milestone 3.2 as dense / tangent-space normal optimization.

## 2026-05-14: Phase 3 Plan Created

**Evidence:**

- Created `refmotion_gs_mvp/PHASE3_PLAN.md`.
- The plan defines Milestone 3.1 as experiment framework refactor and Milestone 3.2 as dense / tangent-space normal optimization.
- The plan includes files, tests, output directories, verification commands, required baselines, decision gates, and scope exclusions.

**Decision:**

The P0 planning repair from `outputs/phase3/full_go_no_go.md` has been drafted. It still needs a short audit before implementation starts.

**Implication:**

Future sessions should audit `PHASE3_PLAN.md` using `PROMPTS/short_audit_prompt.md` before starting Milestone 3.1 code.

## 2026-05-14: Phase 3 Plan Short Audit Passed

**Evidence:**

- `outputs/phase3/phase3_plan_short_audit.md` records the short audit.
- The audit confirmed `PHASE3_PLAN.md` resolves the P0 planning fixes, preserves scope, preserves MVP baselines, keeps dense / tangent-space normal optimization in Milestone 3.2, and defines Milestone 3.1 implementation tests and outputs.
- No source, script, test, or `outputs/run_latest` diffs were reported during the audit.

**Decision:**

`PHASE3_PLAN.md` passes short audit. Milestone 3.1 implementation may begin.

**Implication:**

The next session should implement only Milestone 3.1 from `PHASE3_PLAN.md`, starting with decision-check tests.

## 2026-05-14: Milestone 3.1 Framework Verification Passed

**Evidence:**

- `pytest refmotion_gs_mvp/tests -q` passed with `20 passed in 9.59s`.
- `python -m py_compile refmotion_gs_mvp/src/*.py refmotion_gs_mvp/scripts/run_mvp_diagnostics.py refmotion_gs_mvp/scripts/run_phase3_milestone31.py` exited 0.
- `python refmotion_gs_mvp/scripts/run_phase3_milestone31.py --out-dir refmotion_gs_mvp/outputs/phase3/milestone_31_framework` exited 0.
- `outputs/phase3/milestone_31_framework/metrics.json` contains the required baseline suite and decision checks.
- `outputs/phase3/milestone_31_framework/summary.md` explicitly reports `routing_beats_oracle_mask: false`.
- Phase 3 metadata records `implemented_dense_normal_optimization: false` and `implemented_learned_near_field_reflection: false`.

**Decision:**

Milestone 3.1 implementation satisfies the framework refactor verification gate and is ready for the required short audit.

**Implication:**

Future sessions should run `PROMPTS/short_audit_prompt.md` before starting Milestone 3.2 or any dense / tangent-space normal optimization work.

## 2026-05-14: Milestone 3.1 Short Audit Passed

**Evidence:**

- `outputs/phase3/milestone_31_short_audit.md` records the short audit.
- The audit checked Milestone 3.1 source helpers, tests, runner, logs, `outputs/phase3/milestone_31_framework/metrics.json`, and `outputs/phase3/milestone_31_framework/summary.md`.
- Full verification evidence remains `20 passed in 9.59s`, Python compilation exit 0, and Phase 3 runner exit 0.
- The audit confirmed the required baseline suite is present and that `summary.md` reports `routing_beats_oracle_mask: false`.
- The audit found no implementation of dense normal optimization, learned near-field reflection fields, inter-reflection residuals, full PBR optimization, relighting, or material editing.

**Decision:**

Milestone 3.1 short audit verdict is `PASS`. The framework refactor is accepted.

**Implication:**

Milestone 3.2 is a major method-validation step. Future sessions must run a GPT-5.5 xhigh major-stage audit before implementing dense / tangent-space normal optimization.

## 2026-05-14: Milestone 3.2 Xhigh Audit Gate Enforced

**Evidence:**

- `NEXT_ACTION.md` requires a GPT-5.5 xhigh major-stage audit before Milestone 3.2 implementation.
- `PROMPTS/continue_current_work_prompt.md` requires stopping rather than running a major-stage audit when the current session is not GPT-5.5 xhigh.
- The current session was not explicitly started as GPT-5.5 xhigh.

**Decision:**

Do not run the Milestone 3.2 major-stage audit in this session. Require a GPT-5.5 xhigh audit session.

**Implication:**

Milestone 3.2 remains blocked. Future sessions should start with GPT-5.5 xhigh and run `PROMPTS/full_xhigh_audit_prompt.md`; no dense / tangent-space normal optimization should begin before that audit passes.

## 2026-05-14: Milestone 3.2 Pre-Implementation Audit Separated

**Evidence:**

- `NEXT_ACTION.md` previously pointed the Milestone 3.2 pre-implementation gate to `PROMPTS/full_xhigh_audit_prompt.md`.
- `PROMPTS/full_xhigh_audit_prompt.md` is a post-result go/no-go audit prompt and asks for evidence from an already completed major stage.
- Milestone 3.2 has not been implemented yet.
- Created `PROMPTS/pre_milestone_32_audit_prompt.md` for GPT-5.5 xhigh pre-implementation authorization.
- Updated `OPERATING_PROTOCOL.md` to distinguish pre-implementation audit prompts from post-result full go/no-go audits.
- Updated `NEXT_ACTION.md` to use `PROMPTS/pre_milestone_32_audit_prompt.md`.

**Decision:**

Separated Milestone 3.2 pre-implementation authorization audit from post-result full go/no-go audit to prevent Codex from requiring dense-normal results before implementation.

**Implication:**

Future GPT-5.5 xhigh sessions should run the Milestone 3.2 pre-implementation authorization audit, not the post-result full go/no-go audit. Milestone 3.2 code remains blocked until that authorization audit approves implementation or approves it with no P0 blockers.

## 2026-05-14: Generic Continue-Current-Work Dispatcher

**Evidence:**

- Updated `PROMPTS/continue_current_work_prompt.md` with a generic dispatch rule based on `NEXT_ACTION.md` fields.
- Added the `NEXT_ACTION.md` schema to `OPERATING_PROTOCOL.md`.
- Created `PROMPTS/pre_major_milestone_audit_prompt.md` as a reusable pre-implementation audit prompt for major milestones.
- Rewrote `NEXT_ACTION.md` to contain only the current Milestone 3.2 pre-implementation audit action.

**Decision:**

Generalized the continue-current-work command into a dispatcher. Future user commands can remain generic; task specificity lives in NEXT_ACTION.md.

**Implication:**

Future sessions should be able to continue by using only `PROMPTS/continue_current_work_prompt.md`. The dispatcher must read `NEXT_ACTION.md`, select the required prompt, execute only the current action, update logs/results/decision state, rewrite `NEXT_ACTION.md`, and stop.
