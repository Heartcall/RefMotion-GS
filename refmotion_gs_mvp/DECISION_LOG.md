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

