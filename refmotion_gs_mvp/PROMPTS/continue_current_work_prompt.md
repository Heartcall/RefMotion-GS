# Continue Current Work Prompt

Use this prompt in a fresh Codex session when the user wants the project to continue without providing a new task description.

## Role

You are Codex working inside `/home/liuly/Surface_Reconstruction/Glossy/new_idea`. The active project is `refmotion_gs_mvp`, named RefMotion-GS.

Use GPT-5.5 high unless `NEXT_ACTION.md` or `OPERATING_PROTOCOL.md` requires GPT-5.5 xhigh for a major-stage full audit.

## Required Startup

Before taking any project action, read:

1. `refmotion_gs_mvp/AGENTS.md`
2. `refmotion_gs_mvp/ACTIVE_SCOPE.md`
3. `refmotion_gs_mvp/OPERATING_PROTOCOL.md`
4. `refmotion_gs_mvp/NEXT_ACTION.md`
5. `refmotion_gs_mvp/DECISION_LOG.md`
6. latest entries in `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`
7. latest decision/evidence in `refmotion_gs_mvp/MVP_RESULTS.md`
8. latest relevant result files under `refmotion_gs_mvp/outputs/`
9. any source, scripts, tests, plans, or prompt files explicitly named by `NEXT_ACTION.md`

## Execution Rule

Continue exactly from `NEXT_ACTION.md`.

- If `NEXT_ACTION.md` says the next action is a planning audit, run the audit prompt it names.
- If `NEXT_ACTION.md` says the next action is implementation, execute only the named milestone.
- If `NEXT_ACTION.md` says the next action is a small audit, use `PROMPTS/short_audit_prompt.md`.
- If `NEXT_ACTION.md` says the next action is a major-stage audit, use `PROMPTS/full_xhigh_audit_prompt.md`.

If a major-stage audit is required:

- If the current session is GPT-5.5 xhigh, run the audit now using `PROMPTS/full_xhigh_audit_prompt.md` or the audit prompt named by `NEXT_ACTION.md`.
- If the current session is not GPT-5.5 xhigh, stop after updating `NEXT_ACTION.md` to request a GPT-5.5 xhigh audit session.
- Do not perform a major-stage audit with a weaker model.

Do not invent a different next task. Do not begin implementation when `NEXT_ACTION.md` says audit or planning is required first.

Execute at most one current action per session. After completing that action, update `NEXT_ACTION.md` with the next exact task and stop. Do not automatically continue into the next action in the same session unless `NEXT_ACTION.md` explicitly says the current action includes that substep.

During planning or audit actions, do not implement experiment code or silently fix files unless the named prompt explicitly requests a workflow-file repair.

## Scope Guard

The active project is RefMotion-GS, not full RefTex-GS.

Do not implement or claim:

- learned near-field reflection fields,
- inter-reflection residuals,
- full PBR optimization,
- relighting,
- material editing,
- mesh representation novelty,
- UV representation novelty,
- PBR representation novelty,
- Gaussian representation novelty.

Mesh, UV, baking, and Gaussian-related components are allowed only as implementation or evaluation scaffolding when `NEXT_ACTION.md` and the current plan allow them.

## When To Ask The User

Do not ask the user for a new prompt. Ask only if blocked by one of these conditions:

- environment access is required,
- required data or files are missing,
- the next step would change project scope,
- evidence requires a pivot decision,
- evidence requires a stop or abandonment decision,
- `OPERATING_PROTOCOL.md` defines a stop condition for the current state.

## Required End State

Before finishing the session, update the persistent workflow state required by the completed action:

- write or update logs/results,
- update `DECISION_LOG.md` when a decision is made,
- update `NEXT_ACTION.md` with the exact next task,
- record verification commands and observed outputs,
- stop only under the allowed blocked conditions.
