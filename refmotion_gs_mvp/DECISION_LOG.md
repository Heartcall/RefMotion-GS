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

## 2026-05-14: Explicit Operator Model Confirmation Gate

**Evidence:**

- Codex CLI UI controls model selection through `/model`, but the assistant cannot reliably inspect the backend model label from inside the prompt.
- The previous workflow asked the assistant to determine whether the current session was GPT-5.5 xhigh, causing false stops after operator-side model switches.
- Updated `PROMPTS/continue_current_work_prompt.md` with a model confirmation rule.
- Updated `OPERATING_PROTOCOL.md` with a model gate policy and recommended generic command.
- Updated `NEXT_ACTION.md` so required xhigh gates are satisfied by explicit operator confirmation in the user command.

**Decision:**

Fixed the model gate so that explicit operator confirmation satisfies the required-model check. Codex should no longer stop merely because it cannot independently inspect the backend model label.

**Implication:**

For required xhigh actions, future sessions should proceed when the user command explicitly confirms that Codex has been switched to the required model. If no explicit confirmation is present, the workflow should request GPT-5.5 xhigh plus model confirmation and stop.

## 2026-05-14: Milestone 3.2 Pre-Implementation Audit Blocked On Plan Detail

**Evidence:**

- `outputs/phase3/milestone_32_preimplementation_audit.md` records the GPT-5.5 xhigh pre-implementation authorization audit.
- The audit confirmed Milestone 3.2 is conceptually in scope and remains inside RefMotion-GS.
- `PHASE3_PLAN.md` requires exact normal-update parameterization, regularization, sampling, seeds, comparison, and result schema before Milestone 3.2 implementation.
- Those details are not yet defined in `PHASE3_PLAN.md`.
- The audit found no need to pivot or stop, and no experiment code was implemented.

**Decision:**

Milestone 3.2 implementation is `BLOCKED UNTIL PLAN FIXES`. The next action is a planning repair, not dense / tangent-space normal optimization code.

**Implication:**

Future sessions should update `PHASE3_PLAN.md` with the missing Milestone 3.2 P0 implementation subplan, then rerun the pre-implementation authorization audit with GPT-5.5 xhigh before any Milestone 3.2 code begins.

## 2026-05-14: Milestone 3.2 Planning Repair Completed

**Evidence:**

- Updated `PHASE3_PLAN.md` with a dedicated Milestone 3.2 implementation subplan.
- The repaired plan defines the dense / tangent-space normal parameterization, optimizer variables, unit-normal projection, smoothness and L2 regularization, deterministic coordinate-search settings, planned files, tests, output schema, baselines, ablations, verification commands, and decision gates.
- The plan keeps Milestone 3.2 inside RefMotion-GS scope and continues to forbid learned near-field reflection fields, inter-reflection residuals, full PBR optimization, relighting, material editing, and representation-novelty claims.
- No source, script, test, or experiment-output code was changed during the planning repair.

**Decision:**

The Milestone 3.2 P0 planning repair is complete. Implementation remains blocked until a GPT-5.5 xhigh pre-implementation authorization audit approves the repaired plan.

**Implication:**

Future sessions should rerun the Milestone 3.2 pre-implementation authorization audit using `PROMPTS/pre_major_milestone_audit_prompt.md`. If approved with no P0 blockers, the next action may become Milestone 3.2 implementation using GPT-5.5 high.

## 2026-05-15: Standard Continue Prompt As Model Confirmation

**Evidence:**

- Updated `PROMPTS/continue_current_work_prompt.md` so invoking the standard continue prompt is treated as operator confirmation that Codex CLI has already been switched to the model required by `NEXT_ACTION.md`.
- Updated `OPERATING_PROTOCOL.md` with the same default-command model gate policy.
- Updated `NEXT_ACTION.md` to remove the old requirement for a separate explicit model-confirmation phrase.
- Preserved the rule that major audits must follow the required audit prompt and must not implement experiment code.

**Decision:**

Changed the model gate so the standard continue prompt itself serves as operator confirmation that the required model has been selected in Codex CLI.

**Implication:**

Future users can invoke `Use refmotion_gs_mvp/PROMPTS/continue_current_work_prompt.md.` without adding a separate model-confirmation phrase. Codex should stop for model reasons only when the user explicitly says the required model has not been selected.

## 2026-05-15: Milestone 3.2 Pre-Implementation Audit Approved

**Evidence:**

- Reran the Milestone 3.2 pre-implementation authorization audit using `PROMPTS/pre_major_milestone_audit_prompt.md`.
- `PHASE3_PLAN.md` now defines the dense / tangent-space normal parameterization, regularization, deterministic coordinate-search optimizer, tests, output schema, baseline suite, ablations, verification commands, and decision gates.
- `outputs/phase3/milestone_32_preimplementation_audit.md` records the verdict.
- No Milestone 3.2 experiment code was implemented during the audit.

**Decision:**

Milestone 3.2 is `APPROVED TO IMPLEMENT`.

**Implication:**

Future sessions should implement only Milestone 3.2 using GPT-5.5 high and `PROMPTS/milestone_implementation_prompt.md`. After implementation and verification, the milestone must receive a GPT-5.5 xhigh post-result audit before acceptance.

## 2026-05-15: Milestone 3.2 Implementation Completed Pending Audit

**Evidence:**

- Implemented `src/dense_normal_optimization.py` and `scripts/run_phase3_milestone32.py`.
- Added Milestone 3.2 tests for dense normal composition, dense cycle optimization, no-cycle ablation, and runner schema/scope flags.
- `pytest refmotion_gs_mvp/tests -q` passed with `24 passed in 49.26s`.
- Python compilation exited 0 for all source modules and MVP/Phase 3 runners.
- `run_phase3_milestone32.py` wrote `metrics.json`, `summary.md`, and `dense_loss_history.png`.
- Dense reflective-region normal error improved by `11.305327524690204` percent over perturbed initialization.
- Dense reflection-cycle optimizer beat the no-cycle dense ablation on reflective normal error.
- Routing beat all-pixel and noisy-mask baselines, but did not beat oracle mask exclusion.

**Decision:**

Milestone 3.2 implementation is complete but not accepted. It requires a GPT-5.5 xhigh post-result full go/no-go audit.

**Implication:**

Future sessions must not continue into Milestone 3.3 or paper claims yet. The next action is a major post-result audit using `PROMPTS/full_xhigh_audit_prompt.md`.

## 2026-05-15: Milestone 3.2 Post-Result Audit Requires Revision

**Evidence:**

- `outputs/phase3/milestone_32_post_result_audit.md` records the full go/no-go audit.
- Fresh verification passed:
  - `pytest refmotion_gs_mvp/tests/test_dense_normal_optimization.py -q`: `3 passed in 32.09s`.
  - `pytest refmotion_gs_mvp/tests/test_phase3_milestone32_runner.py -q`: `1 passed in 7.91s`.
  - `pytest refmotion_gs_mvp/tests -q`: `24 passed in 48.97s`.
  - Python compilation exited 0.
  - `run_phase3_milestone32.py` exited 0.
- Dense reflective-region normal error improved by `11.305327524690204` percent and beat the no-cycle dense ablation.
- Routing beat all-pixel and noisy-mask baselines, but did not beat oracle mask exclusion.
- The produced runner configuration records `sample_count = 40` and `update_radius = 1`, while `PHASE3_PLAN.md` listed `sample_count = 250` and described single-texel coordinate proposals.

**Decision:**

Milestone 3.2 audit verdict is `GO AFTER REVISION`. The current candidate result is promising but not accepted until the P0 plan/result documentation revisions are resolved.

**Implication:**

Future sessions should repair the Milestone 3.2 plan/result documentation before starting Milestone 3.3. Required revisions must align the plan and result summary with the executed runner configuration, or rerun/report the strict planned configuration.

## 2026-05-15: Milestone 3.2 Audit Revision Documentation Repaired

**Evidence:**

- Updated `PHASE3_PLAN.md` to explicitly distinguish the accepted Milestone 3.2 smoke configuration from stricter deferred settings.
- The accepted smoke configuration is `sample_count = 40` and `update_radius = 1`.
- The stricter deferred settings remain `sample_count = 250` and `update_radius = 0` for a future explicit rerun if needed.
- Updated `outputs/phase3/milestone_32_dense_normals/summary.md` to state that dense normal improvement is marginal, the global-rotation reference remains stronger, and oracle mask exclusion remains substantially stronger on leakage.
- No source, script, test, or experiment metric JSON was changed during this planning repair.

**Decision:**

The P0 documentation repair from the Milestone 3.2 post-result audit is complete as a planning/result-summary revision. Milestone 3.2 is still not accepted until this revision state passes a short audit.

**Implication:**

Future sessions should run `PROMPTS/short_audit_prompt.md` against the revised Milestone 3.2 plan/result state before moving to Milestone 3.3 or any stronger claim.

## 2026-05-15: Milestone 3.2 Revision Short Audit Passed

**Evidence:**

- `outputs/phase3/milestone_32_revision_short_audit.md` records the short audit.
- The audit confirmed `PHASE3_PLAN.md` and `outputs/phase3/milestone_32_dense_normals/summary.md` now match the executed Milestone 3.2 smoke configuration: `sample_count = 40` and `update_radius = 1`.
- The summary reports marginal dense normal improvement, stronger global-rotation reference, and stronger oracle-mask leakage.
- Verification passed:
  - `pytest refmotion_gs_mvp/tests/test_phase3_milestone32_runner.py -q`: `1 passed in 7.69s`.
  - `python -m py_compile refmotion_gs_mvp/src/dense_normal_optimization.py refmotion_gs_mvp/scripts/run_phase3_milestone32.py`: exit code 0.
  - `jq empty refmotion_gs_mvp/outputs/phase3/milestone_32_dense_normals/metrics.json`: exit code 0.
  - `git diff --name-only refmotion_gs_mvp/src refmotion_gs_mvp/scripts refmotion_gs_mvp/tests`: no paths printed.

**Decision:**

Milestone 3.2 revision short audit verdict is `PASS`. The revision state is accepted as a documented lower-cost analytic smoke-result state.

**Implication:**

Future sessions may proceed to a GPT-5.5 xhigh pre-implementation authorization audit for Milestone 3.3 stricter scene or renderer validation. Do not implement Milestone 3.3 before that audit.

## 2026-05-15: Milestone 3.3 Pre-Implementation Audit Blocked On Plan Detail

**Evidence:**

- `outputs/phase3/milestone_33_preimplementation_audit.md` records the GPT-5.5 xhigh pre-implementation authorization audit.
- `PHASE3_PLAN.md` currently defines Milestone 3.3 only at a high level: prefer Blender/Cycles if available, otherwise use a more explicit analytic near-object reflection scene, keep ground truth and baselines, and preserve deterministic summaries.
- `which blender` exited 1 in this session, so Blender/Cycles cannot be assumed available.
- The plan does not yet define Milestone 3.3 scene design, files, tests, output schema, metrics, verification commands, baseline mapping, fallback trigger, or decision gates.
- No Milestone 3.3 source, script, or test code was implemented during the audit.

**Decision:**

Milestone 3.3 implementation is `BLOCKED UNTIL PLAN FIXES`. The next action is a planning repair, not stricter-scene implementation.

**Implication:**

Future sessions should update `PHASE3_PLAN.md` with a complete Milestone 3.3 implementation subplan, using the analytic near-object fallback unless Blender/Cycles access is explicitly made available. After repair, rerun the GPT-5.5 xhigh pre-implementation authorization audit before implementing Milestone 3.3 code.

## 2026-05-15: Milestone 3.3 Planning Repair Completed

**Evidence:**

- `PHASE3_PLAN.md` now contains an implementation-grade Milestone 3.3 plan for analytic near-object fallback validation.
- The plan records Blender/Cycles as unavailable in the current workflow because `which blender` exited `1` during the pre-implementation audit.
- The plan defines deterministic reflector geometry, camera split, ground-truth outputs, public API, tests, output schema, verification commands, preserved baselines, and decision gates.
- No source, script, test, or experiment-result files were modified during this planning repair.

**Decision:**

Milestone 3.3 is ready for a rerun of the GPT-5.5 xhigh pre-implementation authorization audit. Implementation remains blocked until that audit returns `APPROVED TO IMPLEMENT` or `APPROVED WITH REQUIRED FIXES` without P0 blockers.

**Implication:**

Future sessions should run `PROMPTS/pre_major_milestone_audit_prompt.md` against the repaired Milestone 3.3 plan before implementing any Milestone 3.3 experiment code.

## 2026-05-15: Milestone 3.3 Pre-Implementation Audit Approved With P1 Fixes

**Evidence:**

- `outputs/phase3/milestone_33_preimplementation_audit.md` records the rerun pre-implementation authorization audit.
- The repaired `PHASE3_PLAN.md` now specifies the Milestone 3.3 analytic near-object fallback implementation path, scene design, file/API targets, tests, output schema, verification commands, baseline preservation, reviewer-risk coverage, and decision gates.
- `which blender` still exits `1`, so the analytic near-object fallback remains the current implementation path.
- No source, script, or test files were modified during the audit.

**Decision:**

Milestone 3.3 is `APPROVED WITH REQUIRED FIXES`. The remaining fixes are P1 implementation-time clarifications, not P0 blockers.

**Implication:**

Future sessions should implement only Milestone 3.3 using GPT-5.5 high and `PROMPTS/milestone_implementation_prompt.md`. After implementation and verification, the milestone must receive a GPT-5.5 xhigh post-result full go/no-go audit before acceptance.

## 2026-05-15: Milestone 3.3 Implementation Completed Pending Audit

**Evidence:**

- Implemented the analytic near-object fallback scene and Milestone 3.3 runner.
- Added tests for near-object scene determinism, finite reflector hit fraction, explicit `trace_reflector_color` return order, loss preference for ground-truth normals, runner schema, baseline preservation, and scope flags.
- Verification passed:
  - `pytest refmotion_gs_mvp/tests/test_near_object_scene.py -q`: `3 passed in 1.66s`.
  - `pytest refmotion_gs_mvp/tests/test_phase3_milestone33_runner.py -q`: `1 passed in 8.70s`.
  - `pytest refmotion_gs_mvp/tests -q`: `28 passed in 58.58s`.
  - Python compilation exited `0`.
  - Milestone 3.3 runner exited `0`.
  - `jq empty` on `metrics.json` exited `0`.
- Milestone 3.3 metrics:
  - `reflector_hit_fraction`: `0.15492957746478872`.
  - `loss_correlated_near_gt`: `true`.
  - `dense_normal_error_improves_10_percent`: `false`.
  - dense reflective-region normal improvement: `0.7685068728508346` percent.
  - `dense_beats_no_cycle_ablation`: `true`.
  - `routing_beats_all_pixels`: `true`.
  - `routing_beats_noisy_mask`: `true`.
  - `routing_beats_oracle_mask`: `false`.
  - forbidden-component flags remain false.

**Decision:**

Milestone 3.3 implementation is complete but not accepted. It produced valid outputs and preserved scope, but the dense-normal improvement gate failed.

**Implication:**

Future sessions must run a GPT-5.5 xhigh post-result full go/no-go audit before deciding whether Milestone 3.3 should be revised, narrowed, pivoted, or stopped. Do not proceed to paper claims or a new implementation milestone before that audit.

## 2026-05-15: Milestone 3.3 Post-Result Audit Requires Revision

**Evidence:**

- `outputs/phase3/milestone_33_post_result_audit.md` records the GPT-5.5 xhigh full go/no-go audit.
- Fresh verification passed:
  - `pytest refmotion_gs_mvp/tests/test_near_object_scene.py -q`: `3 passed in 1.56s`.
  - `pytest refmotion_gs_mvp/tests/test_phase3_milestone33_runner.py -q`: `1 passed in 8.90s`.
  - `pytest refmotion_gs_mvp/tests -q`: `28 passed in 61.46s`.
  - Python compilation commands exited `0`.
  - Milestone 3.3 runner exited `0`.
  - `jq empty` on Milestone 3.3 `metrics.json` exited `0`.
- Milestone 3.3 stayed in scope and preserved forbidden-component flags.
- Milestone 3.3 failed the dense-normal improvement gate:
  - dense reflective-region normal improvement: `0.7685068728508346` percent.
  - required gate: at least `10` percent.
- Oracle mask exclusion remains substantially stronger on leakage than normal-refinement-plus-routing.

**Decision:**

Milestone 3.3 verdict is `GO AFTER REVISION`. The implementation is reproducible and in scope, but it is not accepted as a passing major validation result.

**Implication:**

Future sessions should run a Milestone 3.3 revision planning repair using GPT-5.5 high. The repair must define diagnostics for the failed dense-normal gate before any new experiment code is implemented. Do not proceed to paper writing or stronger claims from the current Milestone 3.3 result.

## 2026-05-15: Milestone 3.3 Revision Planning Repair Completed

**Evidence:**

- `PHASE3_PLAN.md` now includes section `8.14 Milestone 3.3 Revision: Dense-Normal Gate Failure Diagnostics`.
- The revision subplan records the failed dense-normal gate from the post-result audit:
  - dense reflective-region normal improvement: `0.7685068728508346` percent.
  - required gate: at least `10` percent.
- The subplan defines required diagnostics for objective-versus-normal-error trajectory, accepted-update normal-error history, active texel and finite-reflector hit coverage, non-reflective normal drift, routing comparisons, oracle-mask status, and reflector primitive reconciliation.
- No source, script, test, or experiment-result metric files were changed during the planning repair.

**Decision:**

Milestone 3.3 planning repair is complete. The next step is a bounded diagnostic revision implementation, not paper writing, broader method expansion, or a pivot.

**Implication:**

Future sessions should implement only the Milestone 3.3 diagnostic revision using GPT-5.5 high. After implementation and verification, run a short audit before treating the revision state as accepted.

## 2026-05-15: Milestone 3.3 Diagnostic Revision Implemented Pending Short Audit

**Evidence:**

- Created the Milestone 3.3 diagnostic revision module, runner, tests, and output directory.
- Fresh verification passed:
  - `pytest refmotion_gs_mvp/tests/test_phase3_revision_diagnostics.py -q`: `2 passed in 1.86s`.
  - `pytest refmotion_gs_mvp/tests/test_phase3_milestone33_revision_runner.py -q`: `1 passed in 2.72s`.
  - `pytest refmotion_gs_mvp/tests -q`: `31 passed in 67.55s`.
  - Python compilation exited `0`.
  - revision runner exited `0`.
  - `jq empty` on revision `metrics.json` exited `0`.
- Key diagnostics:
  - dense objective decreased from `0.014386876237571697` to `0.010304391097315124`.
  - final reflective-region normal improvement remained `0.7685068728508346` percent.
  - `worsened_reflective_update_count`: `5` of `8` accepted updates.
  - `active_texels_without_finite_hits`: `34` of `64`.
  - normal-refinement-plus-routing is worse than reflection-confidence routing on UV leakage.
  - oracle mask exclusion remains substantially stronger on leakage.
- Existing audited Milestone 3.3 and Milestone 3.2 result files were preserved.

**Decision:**

Milestone 3.3 diagnostic revision implementation is complete but not accepted. It requires a short audit before the revision state can be used for any next decision.

**Implication:**

Future sessions should run `PROMPTS/short_audit_prompt.md` using GPT-5.5 high. If the short audit passes, decide the exact next planning or revision action from the diagnostic evidence. If the short audit finds pivot or stop evidence, escalate to GPT-5.5 xhigh go/no-go / pivot review.

## 2026-05-15: Milestone 3.3 Diagnostic Revision Short Audit Escalates to Go/No-Go

**Evidence:**

- `outputs/phase3/milestone_33_revision_short_audit.md` records the short audit.
- Fresh verification passed:
  - `pytest refmotion_gs_mvp/tests/test_phase3_revision_diagnostics.py -q`: `2 passed in 1.94s`.
  - `pytest refmotion_gs_mvp/tests/test_phase3_milestone33_revision_runner.py -q`: `1 passed in 2.76s`.
  - Python compilation exited `0`.
  - `jq empty` on revision `metrics.json` exited `0`.
- The diagnostic revision remains in scope and preserves forbidden-component flags.
- The revision explains but does not fix the failed dense-normal gate:
  - final reflective-region normal improvement remains `0.7685068728508346` percent.
  - `5` of `8` accepted dense updates worsen reflective-region normal error.
  - `34` of `64` active texels have no finite reflector hits.
  - normal-refinement-plus-routing is worse than reflection-confidence routing and far worse than oracle mask exclusion on leakage.

**Decision:**

The diagnostic revision passes as a small diagnostic implementation, but it is not accepted as a validation pass. The evidence creates pivot-risk and requires a GPT-5.5 xhigh go/no-go / pivot audit before any further implementation.

**Implication:**

Future sessions should run a major post-result audit using `PROMPTS/full_xhigh_audit_prompt.md`. Do not implement new experiment code until that audit decides whether to revise the dense-normal formulation/scene, pivot toward benchmark/leakage-metric work, or stop.

## 2026-05-15: Milestone 3.3 Diagnostic Revision Full Audit Pivots Project Direction

**Evidence:**

- `outputs/phase3/milestone_33_revision_full_go_no_go.md` records the GPT-5.5 xhigh full go/no-go / pivot audit.
- Fresh verification passed:
  - `pytest refmotion_gs_mvp/tests/test_phase3_revision_diagnostics.py -q`: `2 passed in 1.92s`.
  - `pytest refmotion_gs_mvp/tests/test_phase3_milestone33_revision_runner.py -q`: `1 passed in 2.80s`.
  - `pytest refmotion_gs_mvp/tests -q`: `31 passed in 61.60s`.
  - Python compilation exited `0`.
  - temporary revision runner exited `0`.
  - saved and temporary rerun `metrics.json` matched by `diff -q`.
- The revision remains in scope and reproducible.
- Dense-normal evidence remains below the acceptance gate:
  - final reflective-region normal improvement: `0.7685068728508346` percent.
  - `5` of `8` accepted dense updates worsen reflective-region normal error.
  - `34` of `64` active texels have no finite reflector hits.
  - normal-refinement-plus-routing is worse than reflection-confidence routing and far worse than oracle mask exclusion on leakage.

**Decision:**

Full audit verdict is `PIVOT`. RefMotion-GS should pivot away from further dense-normal optimizer implementation under the current Phase 3 setup and toward a benchmark / leakage-metric direction.

**Implication:**

Future sessions should create a pivot plan using GPT-5.5 high. Do not implement more dense-normal optimization code unless a future audited plan introduces a substantially different in-scope formulation and passes pre-implementation review.
