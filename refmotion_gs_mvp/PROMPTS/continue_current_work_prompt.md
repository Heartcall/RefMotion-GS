# Continue Current Work Prompt

Use this prompt in a fresh Codex session when the user wants the project to continue without providing a new task description.

## Role

You are Codex working inside `/home/liuly/Surface_Reconstruction/Glossy/new_idea`. The active project is `refmotion_gs_mvp`, named RefMotion-GS.

Use GPT-5.5 high unless `NEXT_ACTION.md` or `OPERATING_PROTOCOL.md` requires GPT-5.5 xhigh for a major-stage audit, go/no-go decision, pivot/stop decision, novelty-risk decision, or theory-critical review.

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

## Generic Dispatch Rule

Always treat `NEXT_ACTION.md` as the source of the current task.

Read the `Action Type` and `Required Prompt` fields from `NEXT_ACTION.md`.

- If `NEXT_ACTION.md` specifies a `Required Prompt`, use that prompt.
- If no `Required Prompt` is specified, or if it says `infer from action type`, infer the prompt from `Action Type`.
- Execute at most one current action per session.
- After completing the current action, update logs, result files, `DECISION_LOG.md`, and `NEXT_ACTION.md` as required by the selected prompt and current action.
- Stop after completing the current action.
- Do not automatically continue into the next task.

Supported action types:

| Action Type | Prompt |
|---|---|
| `planning` | `PROMPTS/phase_plan_prompt.md` |
| `short_audit` | `PROMPTS/short_audit_prompt.md` |
| `major_post_result_audit` | `PROMPTS/full_xhigh_audit_prompt.md` |
| `major_preimplementation_audit` | the pre-implementation audit prompt named in `NEXT_ACTION.md` |
| `implementation` | `PROMPTS/milestone_implementation_prompt.md` |
| `paper_writing` | `PROMPTS/paper_writing_prompt.md` |
| `workflow_repair` | the current user-approved workflow repair instructions in `NEXT_ACTION.md` |

For `major_preimplementation_audit`, if `NEXT_ACTION.md` does not name a dedicated pre-implementation audit prompt, stop and update `NEXT_ACTION.md` to require one.

## Model Confirmation Rule

Codex cannot reliably inspect the backend model label from inside the prompt. The operator controls the model through Codex CLI `/model`.

When the user invokes this prompt, treat the invocation as operator confirmation that Codex has already been switched to the model required by `NEXT_ACTION.md`.

Therefore:

- If `NEXT_ACTION.md` requires GPT-5.5 xhigh, proceed with the xhigh-required action after reading `NEXT_ACTION.md`.
- Do not stop merely because the assistant cannot independently inspect the backend model label.
- If the user explicitly says the model has not been switched, then stop and request the required model.
- If the action type is a major audit, still follow the required audit prompt and do not implement code.

## Model Gate

If the action type is `major_post_result_audit` or `major_preimplementation_audit`:

- If `NEXT_ACTION.md` requires GPT-5.5 xhigh, treat this prompt invocation as operator confirmation that the required model has been selected and run the required audit now.
- If the user explicitly says the model has not been switched to the model required by `NEXT_ACTION.md`, stop and request the required model.
- Never perform a major-stage audit with a weaker model.
- Never stop merely because xhigh is required when the user invoked this continue prompt without saying the model was not switched.

If the action type is `implementation`, `planning`, `short_audit`, `paper_writing`, or `workflow_repair`, GPT-5.5 high is sufficient unless `NEXT_ACTION.md` explicitly requires GPT-5.5 xhigh.

## Execution Rule

Continue exactly from `NEXT_ACTION.md`.

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
