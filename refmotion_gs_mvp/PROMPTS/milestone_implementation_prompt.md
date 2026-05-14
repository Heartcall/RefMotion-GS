# Milestone Implementation Prompt

Use this prompt in a fresh Codex session when `NEXT_ACTION.md` says the next action is implementation.

## Role

You are Codex working inside `/home/liuly/Surface_Reconstruction/Glossy/new_idea`. The active project is `refmotion_gs_mvp`, named RefMotion-GS.

Use GPT-5.5 high for implementation. Execute only the current milestone named in `refmotion_gs_mvp/NEXT_ACTION.md`.

## Required Reads

Read, in order:

1. `refmotion_gs_mvp/ACTIVE_SCOPE.md`
2. `refmotion_gs_mvp/NEXT_ACTION.md`
3. `refmotion_gs_mvp/OPERATING_PROTOCOL.md`
4. `refmotion_gs_mvp/PROJECT_PLAN.md`
5. `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`
6. `refmotion_gs_mvp/MVP_RESULTS.md`
7. `refmotion_gs_mvp/DECISION_LOG.md`
8. Any plan or result file referenced by `NEXT_ACTION.md`
9. Relevant source, scripts, tests, and output metrics under `refmotion_gs_mvp/`

## Scope Guard

Do not implement:

- learned near-field reflection fields,
- inter-reflection residuals,
- full PBR optimization,
- relighting,
- material editing.

Do not frame mesh, UV, PBR, or Gaussian representation as novelty.

If the milestone requires one of these, stop, update `DECISION_LOG.md`, and set `NEXT_ACTION.md` to request a user scope decision.

## Implementation Loop

1. Restate the current milestone in one concise internal note.
2. Identify the exact files and tests affected.
3. Add or update tests for new core behavior where feasible.
4. Implement the smallest change that satisfies the milestone.
5. Run targeted tests.
6. Run default verification unless the milestone plan gives a stricter command set:

```bash
pytest refmotion_gs_mvp/tests -q
python -m py_compile refmotion_gs_mvp/src/*.py refmotion_gs_mvp/scripts/run_mvp_diagnostics.py
python refmotion_gs_mvp/scripts/run_mvp_diagnostics.py --out-dir refmotion_gs_mvp/outputs/run_latest
```

7. If a new runner exists, run it into a dedicated output directory.
8. Write a result summary next to the output metrics.
9. Update `IMPLEMENTATION_LOG.md` with evidence, inference, and next action.
10. Classify the milestone as small or major.
11. Run short audit for small milestones or GPT-5.5 xhigh full audit for major stages.
12. Update `DECISION_LOG.md`.
13. Update `NEXT_ACTION.md` with the exact next task.

## Required Evidence

Record:

- commands run,
- test pass/fail counts,
- output paths,
- key metrics,
- whether loss remains correlated with normal correctness,
- whether reflective normal error improves,
- whether routing beats all-pixel and noisy-mask baselines,
- whether routing beats or fails to beat oracle mask exclusion,
- failure cases and scope risks.

## Completion Rule

Do not stop after implementation unless `NEXT_ACTION.md` is updated. Stop only if the next step needs user input, environment access, scope change, pivot, or abandonment.

