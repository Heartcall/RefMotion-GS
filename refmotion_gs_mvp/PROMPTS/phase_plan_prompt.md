# Phase Plan Prompt

Use this prompt in a fresh Codex session when `NEXT_ACTION.md` says the next action is planning.

## Role

You are Codex working inside `/home/liuly/Surface_Reconstruction/Glossy/new_idea`. The active project is `refmotion_gs_mvp`, named RefMotion-GS.

Use GPT-5.5 high for planning unless a full go/no-go audit is explicitly required.

## Required Reads

Before writing or changing a plan, read:

1. `refmotion_gs_mvp/ACTIVE_SCOPE.md`
2. `refmotion_gs_mvp/NEXT_ACTION.md`
3. `refmotion_gs_mvp/OPERATING_PROTOCOL.md`
4. `refmotion_gs_mvp/PROJECT_PLAN.md`
5. `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`
6. `refmotion_gs_mvp/MVP_RESULTS.md`
7. `refmotion_gs_mvp/DECISION_LOG.md`
8. `outputs/phase2/final_go_no_go.md`
9. `outputs/phase2/theory_rewrite.md`
10. `outputs/phase2/reviewer_attack.md`
11. Relevant current source, scripts, tests, and output metrics under `refmotion_gs_mvp/`

## Scope Guard

The active project is RefMotion-GS, not full RefTex-GS.

Do not plan:

- learned near-field reflection fields,
- inter-reflection residuals,
- full PBR optimization,
- relighting,
- material editing,
- novelty claims around mesh, UV, PBR, or Gaussian representation.

If the best next step would require any of the above, record the issue in `DECISION_LOG.md`, update `NEXT_ACTION.md` to request a user scope decision, and stop.

## Planning Task

Create or update the next phase plan. The plan must:

1. state the exact phase objective,
2. state why the phase is needed based on current evidence,
3. define the next milestone only as far as it can be verified,
4. list exact files to create or modify,
5. list exact tests to add or update,
6. list exact verification commands,
7. define pass, revise, pivot, and stop criteria,
8. preserve the existing MVP baselines:
   - all-pixel baking,
   - oracle reflective-mask exclusion,
   - noisy mask-only baking,
   - reflection-confidence routing,
   - normal-refinement plus routing,
9. identify whether the milestone is small or major,
10. identify whether it needs a short audit or GPT-5.5 xhigh full go/no-go audit.

## Current Phase 3 Direction

The current active frontier is stricter validation after the analytic MVP:

- replace global normal-offset optimization with per-surface or tangent-space normal-map optimization,
- improve reflection-scene realism through Blender/Cycles if available or a more explicit analytic near-object reflection scene,
- test whether the method adds value beyond mask-only exclusion,
- keep the contribution framed as reflection-motion supervision.

## Required Outputs

Update or create a phase plan under `refmotion_gs_mvp/` or `refmotion_gs_mvp/outputs/phase3/`.

Then update:

- `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`
- `refmotion_gs_mvp/DECISION_LOG.md`
- `refmotion_gs_mvp/NEXT_ACTION.md`

The final `NEXT_ACTION.md` entry must be exact enough that a future Codex session can start implementation without asking the user what to do.

