# RefMotion-GS Operating Protocol

This protocol lets future Codex sessions continue the project internally without asking the user for a new prompt.

## Source Of Truth

Read these files in order at the start of every session:

1. `ACTIVE_SCOPE.md`
2. `NEXT_ACTION.md`
3. `PROJECT_PLAN.md`
4. `IMPLEMENTATION_LOG.md`
5. `MVP_RESULTS.md`
6. `DECISION_LOG.md`
7. Relevant `outputs/phase2/*.md`
8. Relevant source, scripts, tests, and result files under `refmotion_gs_mvp/`

## Entry Prompts

Use the appropriate entry prompt for the current workflow state:

- **Entry A: Continue current work** -> `PROMPTS/continue_current_work_prompt.md`
- **Entry B: Execute current milestone** -> `PROMPTS/milestone_implementation_prompt.md`
- **Entry C: Small milestone audit** -> `PROMPTS/short_audit_prompt.md`
- **Entry D: Major-stage full audit** -> `PROMPTS/full_xhigh_audit_prompt.md`

When in doubt, start with Entry A and follow `NEXT_ACTION.md` exactly. Do not use Entry B until `NEXT_ACTION.md` explicitly allows implementation.

## NEXT_ACTION Schema

`NEXT_ACTION.md` must contain exactly these fields:

```markdown
# RefMotion-GS Next Action

## Current Next Action
<one exact action>

## Action Type
one of:
- planning
- implementation
- short_audit
- major_preimplementation_audit
- major_post_result_audit
- paper_writing
- workflow_repair

## Required Model
GPT-5.5 high or GPT-5.5 xhigh

## Required Prompt
path to the prompt file, or "infer from action type"

## Required Reads
files to read before executing

## Success Criteria
conditions for considering this action complete

## Stop Conditions
conditions that require stopping or asking the user

## Expected Files To Create Or Update
list of files

## Next Action Update Rule
how to update NEXT_ACTION.md after completion
```

`NEXT_ACTION.md` must contain only the current action, not long history.

Historical evidence belongs in `IMPLEMENTATION_LOG.md` or `DECISION_LOG.md`, not `NEXT_ACTION.md`.

## Model Gate Policy

The default command:

```text
Use refmotion_gs_mvp/PROMPTS/continue_current_work_prompt.md.
```

is treated as operator confirmation that the CLI model has already been set to the model required by `NEXT_ACTION.md`.

Codex should not attempt to independently inspect the backend model label.

- Model selection is controlled by the operator through Codex CLI `/model`.
- If the user explicitly says the model has not been switched to the model required by `NEXT_ACTION.md`, stop and request the required model.
- For major audits, follow the required audit prompt and do not implement code.

## Main Loop

1. Read `ACTIVE_SCOPE.md` and `NEXT_ACTION.md`.
2. If `NEXT_ACTION.md` says the next action is planning, create or update the plan first.
3. If `NEXT_ACTION.md` says the next action is implementation, execute only the current milestone.
4. After implementation, run tests and verification commands.
5. Write results to logs and result files.
6. Classify the milestone as `small` or `major`.
7. For small milestones, run a short audit using `PROMPTS/short_audit_prompt.md`.
8. For major stages, require a GPT-5.5 xhigh full go/no-go audit using `PROMPTS/full_xhigh_audit_prompt.md`.
9. Update `DECISION_LOG.md`.
10. Update `NEXT_ACTION.md` with the exact next task.
11. Stop only if the next step needs user input, environment access, scope change, pivot, or abandonment.

## Action Types

### Planning

Planning means the next step is to write, revise, or audit a phase plan before implementation. Planning work must:

- re-read `ACTIVE_SCOPE.md` and current evidence,
- identify the next milestone and success gate,
- list exact files to create or modify,
- list exact verification commands,
- avoid introducing out-of-scope methods,
- end by updating `NEXT_ACTION.md`.

Use `PROMPTS/phase_plan_prompt.md`.

### Implementation

Implementation means the next step is to build only the current milestone. Implementation work must:

- write or update tests first for new core behavior when feasible,
- modify only files required by the current milestone,
- keep the implementation compatible with the existing NumPy/PyTest analytic MVP unless the audited plan explicitly allows more,
- run verification commands,
- write a result summary,
- classify the milestone and audit it,
- update logs and next action.

Use `PROMPTS/milestone_implementation_prompt.md`.

## Milestone Size Classification

Classify a milestone as **small** when all are true:

- affects one narrow module or script,
- does not change the central hypothesis or evaluation criteria,
- does not introduce a new data source, renderer, optimizer family, or baseline family,
- can be verified with existing tests plus one targeted command.

Classify a milestone as **major** when any are true:

- starts or closes a phase,
- changes the project plan or go/no-go status,
- changes the reflection-cycle formulation,
- introduces a new optimizer family such as dense tangent-space normal maps,
- introduces Blender/Cycles or another renderer path,
- changes the benchmark/baseline suite,
- changes the paper claim, scope, or pivot decision.

Major stages require GPT-5.5 xhigh full audit before implementation is considered accepted.

## Audit Prompt Policy

- Use pre-implementation audit prompts before starting major implementation milestones.
- Use `full_xhigh_audit_prompt.md` only after a major stage has produced implementation results or when making a go/no-go / pivot / stop decision.

## Scope Guard

Always enforce:

- The project is RefMotion-GS, not full RefTex-GS.
- Do not implement learned near-field reflection fields.
- Do not implement inter-reflection residuals.
- Do not implement full PBR optimization.
- Do not claim relighting or material editing.
- Do not frame mesh, UV, PBR, or Gaussian representation as the novelty.
- Treat mesh and UV only as scaffolding for normal and texture-leakage evaluation.

If a planned task violates these rules, update `DECISION_LOG.md`, revise `NEXT_ACTION.md` to request a scope decision, and stop.

## Required Evidence Style

## Session End Summary

At the end of every session summary, include:

- Next exact action from `NEXT_ACTION.md`
- Recommended next model
- One-line reason for the model choice

Model policy:

- Use GPT-5.5 high for planning repairs, implementation, debugging, and short audits.
- Use GPT-5.5 xhigh for major-stage audits, go/no-go decisions, novelty-risk decisions, pivot/stop decisions, and theory-critical reviews.
- Use GPT-5.5 medium only for low-risk repetitive code cleanup, formatting, or mechanical refactors that do not affect claims, metrics, experiments, or scope.

If `NEXT_ACTION.md` requires a major-stage audit or a go/no-go decision, recommend GPT-5.5 xhigh.
If `NEXT_ACTION.md` requires implementation, debugging, planning repair, or short audit, recommend GPT-5.5 high.
If uncertain, recommend GPT-5.5 high, except for go/no-go or pivot decisions, where GPT-5.5 xhigh is mandatory.

Every result update must separate:

- **Evidence:** commands, metrics, files written, observed failures.
- **Inference:** what the evidence supports.
- **Decision:** continue, revise, pivot, stop, or needs audit.
- **Next action:** exact next task and verification command.

Avoid paper-level claims unless a full audit accepts them.

## Default Commands

```bash
pytest refmotion_gs_mvp/tests -q
python -m py_compile refmotion_gs_mvp/src/*.py refmotion_gs_mvp/scripts/run_mvp_diagnostics.py
python refmotion_gs_mvp/scripts/run_mvp_diagnostics.py --out-dir refmotion_gs_mvp/outputs/run_latest
```

Add command variants in `NEXT_ACTION.md` when a milestone needs a new output directory such as `refmotion_gs_mvp/outputs/phase3_milestone_31/`.

## Stop Conditions

Stop and ask the user only if one of these is true:

- user input is required to choose between materially different research directions,
- the next step needs environment access that Codex cannot obtain, such as installing Blender or downloading external dependencies,
- the task would change project scope beyond `ACTIVE_SCOPE.md`,
- evidence indicates a pivot or abandonment decision is needed,
- a full audit rejects the current phase and no in-scope repair is obvious.
