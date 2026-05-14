# Pre-Major-Milestone Authorization Audit Prompt

Use this prompt when `NEXT_ACTION.md` names a major milestone that needs GPT-5.5 xhigh authorization before implementation begins.

## Role

You are Codex performing a pre-implementation authorization audit for the current major milestone in RefMotion-GS.

Use **GPT-5.5 xhigh**. Be adversarial, code-grounded, and evidence-bound.

This is a pre-implementation authorization audit, not a post-result audit.

- Do not require results from a milestone that has not been implemented yet.
- Do not implement code.
- Audit whether the planned milestone is sufficiently specified, in scope, testable, and safe to begin.
- Use `NEXT_ACTION.md` as the source of the exact milestone, required reads, success criteria, stop conditions, expected output path, and next-action update rule.

## Required Reads

Read:

1. `refmotion_gs_mvp/AGENTS.md`
2. `refmotion_gs_mvp/NEXT_ACTION.md`
3. all files listed under `Required Reads` in `NEXT_ACTION.md`
4. the current plan file named by `NEXT_ACTION.md`
5. relevant logs, result summaries, and decision records named by `NEXT_ACTION.md`

Read source, scripts, tests, and outputs only as context. Do not edit experiment code during this audit.

## Audit Sections

### Scope Compliance

Check whether the planned milestone remains inside RefMotion-GS and excludes:

- learned near-field reflection fields,
- inter-reflection residuals,
- full PBR optimization,
- relighting or material editing,
- representation-novelty claims for mesh, UV, PBR, Gaussian, or other scaffolding.

### Formulation Compliance

Check whether the planned milestone preserves the active formulation and claim boundary. For RefMotion-GS, verify that reflection-induced multi-view motion remains the supervision signal and that any normal changes affect reflected-ray geometry and the reflection-cycle loss path, not only post-hoc filtering.

### Implementation Readiness

Check whether the plan defines:

- files to create or modify,
- public functions or scripts to add,
- optimizer variables and parameterization,
- constraints and regularization,
- deterministic seeds or reproducibility controls,
- output directories and result schemas,
- verification commands,
- completion and failure criteria.

### Test Readiness

Check whether tests are specified before implementation and whether they cover the new behavior, failure modes, and scope guards.

### Baseline Preservation

Check whether required baselines from the active plan remain present and comparable. For RefMotion-GS Phase 3 this normally includes all-pixel baking, oracle mask-only baking, noisy mask-only baking, reflection-confidence routing, normal-refinement-plus-routing, and any required ablation without the new reflection-cycle component.

### Metric And Output Readiness

Check whether the milestone defines metrics, output files, markdown summaries, and machine-readable decision checks clearly enough for a future implementation session to run and audit them without inventing missing details.

### Decision Gates

Check whether the plan defines explicit continue, revise, pivot, stop, and post-result audit gates. Do not require the milestone results yet; require only that the gates are measurable and binding.

### Reviewer-Risk Coverage

Check whether the planned milestone addresses the relevant reviewer threats named by the current plan or `NEXT_ACTION.md`, including mask-only explanations, texture-only explanations, overly favorable optimizers, renderer validity, and out-of-scope novelty drift.

### Verdict

Use exactly one verdict:

- `APPROVED TO IMPLEMENT`
- `APPROVED WITH REQUIRED FIXES`
- `BLOCKED UNTIL PLAN FIXES`
- `REJECTED / REPLAN REQUIRED`

Use `APPROVED WITH REQUIRED FIXES` only when the remaining fixes are not P0 blockers. If a future implementation session would need to invent major plan details, use `BLOCKED UNTIL PLAN FIXES`.

## Required Output

Write the audit report to the output path specified by `NEXT_ACTION.md`.

Use this structure:

```markdown
# Pre-Implementation Authorization Audit

## Verdict

APPROVED TO IMPLEMENT / APPROVED WITH REQUIRED FIXES / BLOCKED UNTIL PLAN FIXES / REJECTED / REPLAN REQUIRED

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

Then update the files required by `NEXT_ACTION.md`, normally:

- `refmotion_gs_mvp/DECISION_LOG.md`
- `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`
- `refmotion_gs_mvp/NEXT_ACTION.md`

If the verdict is `APPROVED TO IMPLEMENT`, or `APPROVED WITH REQUIRED FIXES` with no P0 blockers, update `NEXT_ACTION.md` to point to the milestone implementation using GPT-5.5 high.

If the verdict is `BLOCKED UNTIL PLAN FIXES` or `REJECTED / REPLAN REQUIRED`, update `NEXT_ACTION.md` to point to the exact planning repair task and do not implement code.
