# Milestone 3.2 Pre-Implementation Authorization Audit Prompt

Use this prompt when `NEXT_ACTION.md` asks for the GPT-5.5 xhigh authorization audit before Milestone 3.2 dense / tangent-space normal optimization begins.

## Role

You are Codex performing a **pre-implementation authorization audit** for RefMotion-GS Milestone 3.2 inside `/home/liuly/Surface_Reconstruction/Glossy/new_idea`.

Use **GPT-5.5 xhigh**. Be adversarial, code-grounded, and evidence-bound.

This is **not** a post-result go/no-go audit.

- Do not require dense normal optimization results yet.
- Do not implement Milestone 3.2 code.
- Do not change source, scripts, tests, or experiment outputs unless the audit verdict requires workflow or plan repair.
- Audit whether Milestone 3.2 is sufficiently specified, inside RefMotion-GS scope, testable, and safe to begin.

## Required Reads

Read all of:

1. `refmotion_gs_mvp/AGENTS.md`
2. `refmotion_gs_mvp/ACTIVE_SCOPE.md`
3. `refmotion_gs_mvp/OPERATING_PROTOCOL.md`
4. `refmotion_gs_mvp/NEXT_ACTION.md`
5. `refmotion_gs_mvp/PROJECT_PLAN.md`
6. `refmotion_gs_mvp/PHASE3_PLAN.md`
7. `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`
8. `refmotion_gs_mvp/MVP_RESULTS.md`
9. `refmotion_gs_mvp/DECISION_LOG.md`
10. `refmotion_gs_mvp/outputs/phase2/theory_rewrite.md`
11. `refmotion_gs_mvp/outputs/phase2/final_go_no_go.md`
12. `refmotion_gs_mvp/outputs/phase2/reviewer_attack.md`
13. `refmotion_gs_mvp/outputs/phase3/milestone_31_short_audit.md`
14. current source, scripts, and tests named by `PHASE3_PLAN.md` as context only.

## Audit Questions

### A. Scope Compliance

Check whether Milestone 3.2 remains RefMotion-GS and excludes:

- learned near-field reflection fields,
- inter-reflection residuals,
- full PBR optimization,
- relighting or editing,
- novelty claims around mesh, UV, PBR, Gaussian, or other representations.

Reject or block the milestone if it depends on any forbidden component.

### B. Formulation Compliance

Check whether Milestone 3.2:

- still uses Formulation A from `outputs/phase2/theory_rewrite.md`,
- avoids learned reflection fields,
- makes dense normals affect reflected-ray geometry,
- connects dense normals to the reflection-cycle loss path rather than only post-hoc filtering,
- preserves the current reflection-induced multi-view motion claim boundary.

### C. Implementation Readiness

Check whether the plan clearly defines:

- planned files to create or modify,
- tests to add or update before implementation,
- optimizer variables and parameterization,
- normal unit constraints,
- normal smoothness or regularization constraints,
- outputs and result schemas,
- metrics and decision summaries,
- verification commands,
- what counts as pass, revise, pivot, or stop.

Block the milestone if a future implementation session would need to invent these details.

### D. Baseline Preservation

Check whether Milestone 3.2 preserves and reports:

- all-pixel baking,
- oracle mask-only baking,
- noisy mask-only baking,
- reflection-confidence routing,
- normal-refinement-plus-routing,
- dense optimizer without reflection-cycle loss if planned,
- proposed dense reflection-cycle optimizer.

If the dense optimizer without reflection-cycle loss is not planned, decide whether that omission is justified or should be a required fix.

### E. Decision Gates

Check whether Milestone 3.2 defines gates requiring:

- reflective-region normal error to improve by at least 10 percent over perturbed initialization,
- reflection-cycle loss to remain correlated with normal correctness,
- routing to still beat all-pixel and noisy-mask baselines,
- oracle mask exclusion to be reported honestly even if it remains stronger,
- explicit failure criteria for plan repair, pivot, or stop.

Do not require these results before implementation. Require only that the plan makes them measurable and binding.

## Verdict Options

Use exactly one:

- `APPROVED TO IMPLEMENT MILESTONE 3.2`
- `APPROVED WITH REQUIRED FIXES`
- `BLOCKED UNTIL PLAN FIXES`
- `REJECTED / REPLAN REQUIRED`

Use `APPROVED WITH REQUIRED FIXES` only when the fixes are non-P0 or can be resolved without changing the implementation direction. If any P0 plan detail is missing, use `BLOCKED UNTIL PLAN FIXES`.

## Required Output

Write:

`refmotion_gs_mvp/outputs/phase3/milestone_32_preimplementation_audit.md`

Use this structure:

```markdown
# Milestone 3.2 Pre-Implementation Authorization Audit

## Verdict

APPROVED TO IMPLEMENT MILESTONE 3.2 / APPROVED WITH REQUIRED FIXES / BLOCKED UNTIL PLAN FIXES / REJECTED / REPLAN REQUIRED

## Evidence Reviewed

- ...

## Pass/Fail Table

| Criterion | Status | Evidence |
|---|---|---|
| Scope compliance | PASS/FAIL | ... |

## Findings

1. ...

## Required Fixes

- P0: ...
- P1: ...

## Authorization Decision

- ...

## Next Action

- ...
```

Then update:

- `refmotion_gs_mvp/DECISION_LOG.md`
- `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`
- `refmotion_gs_mvp/NEXT_ACTION.md`

If the verdict is `APPROVED TO IMPLEMENT MILESTONE 3.2`, or `APPROVED WITH REQUIRED FIXES` with no P0 blockers, update `NEXT_ACTION.md` to point to Milestone 3.2 implementation using GPT-5.5 high.

If the verdict is `BLOCKED UNTIL PLAN FIXES` or `REJECTED / REPLAN REQUIRED`, update `NEXT_ACTION.md` to point to the exact planning repair task. Stop after writing the audit and workflow updates.
