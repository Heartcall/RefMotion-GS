# RefMotion-GS Next Action

## Current Next Action
Create a RefMotion-GS pivot plan for the benchmark / leakage-metric direction. The plan must pivot away from further dense-normal optimizer implementation under the current Phase 3 setup and define a bounded next phase for evaluating reflective reconstruction failures, texture leakage, mask-only baselines, and reflection-motion diagnostics. Do not implement experiment code during this planning action.

## Action Type
planning

## Required Model
GPT-5.5 high

## Required Prompt
refmotion_gs_mvp/PROMPTS/phase_plan_prompt.md

## Required Reads
- refmotion_gs_mvp/AGENTS.md
- refmotion_gs_mvp/ACTIVE_SCOPE.md
- refmotion_gs_mvp/OPERATING_PROTOCOL.md
- refmotion_gs_mvp/PROJECT_PLAN.md
- refmotion_gs_mvp/PHASE3_PLAN.md
- refmotion_gs_mvp/IMPLEMENTATION_LOG.md
- refmotion_gs_mvp/MVP_RESULTS.md
- refmotion_gs_mvp/DECISION_LOG.md
- refmotion_gs_mvp/outputs/phase3/milestone_33_revision_full_go_no_go.md
- refmotion_gs_mvp/outputs/phase3/milestone_33_revision_short_audit.md
- refmotion_gs_mvp/outputs/phase3/milestone_33_revision_diagnostics/metrics.json
- refmotion_gs_mvp/outputs/phase3/milestone_33_revision_diagnostics/summary.md
- outputs/phase2/theory_rewrite.md
- outputs/phase2/reviewer_attack.md
- outputs/phase2/core_contribution_reduction.md
- outputs/phase2/final_go_no_go.md

## Success Criteria
- The pivot plan defines the next RefMotion-GS phase as a benchmark / leakage-metric direction rather than more dense-normal optimizer implementation.
- The plan states which current dense-normal evidence caused the pivot.
- The plan preserves the strict RefMotion-GS scope:
  - no learned near-field reflection field,
  - no inter-reflection residual,
  - no full PBR optimization,
  - no relighting or material editing claims,
  - no mesh, UV, PBR, or Gaussian representation novelty claim.
- The plan defines exact files to create or modify, expected outputs, metrics, baselines, verification commands, and audit gates.
- The plan updates `DECISION_LOG.md`, `IMPLEMENTATION_LOG.md`, and `NEXT_ACTION.md`.

## Stop Conditions
- If the pivot plan would require changing project scope beyond RefMotion-GS, stop and ask the user.
- If the pivot plan requires external data or environment access not available in the workspace, stop and request the missing access.
- Do not implement experiment code during this planning action.

## Expected Files To Create Or Update
- refmotion_gs_mvp/PHASE4_PIVOT_PLAN.md
- refmotion_gs_mvp/IMPLEMENTATION_LOG.md
- refmotion_gs_mvp/DECISION_LOG.md
- refmotion_gs_mvp/NEXT_ACTION.md

## Next Action Update Rule
- After the pivot plan is written, set `NEXT_ACTION.md` to a short audit of the pivot plan using GPT-5.5 high.
- If the plan reveals a major go/no-go, novelty-risk, or stop decision, set `NEXT_ACTION.md` to a GPT-5.5 xhigh audit instead.
