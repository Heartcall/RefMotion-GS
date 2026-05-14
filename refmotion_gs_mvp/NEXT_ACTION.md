# RefMotion-GS Next Action

## Current Next Action
Run the Milestone 3.2 pre-implementation authorization audit.

## Action Type
major_preimplementation_audit

## Required Model
GPT-5.5 xhigh

## Required Prompt
refmotion_gs_mvp/PROMPTS/pre_major_milestone_audit_prompt.md

## Required Reads
- refmotion_gs_mvp/ACTIVE_SCOPE.md
- refmotion_gs_mvp/OPERATING_PROTOCOL.md
- refmotion_gs_mvp/PHASE3_PLAN.md
- refmotion_gs_mvp/IMPLEMENTATION_LOG.md
- refmotion_gs_mvp/MVP_RESULTS.md
- refmotion_gs_mvp/DECISION_LOG.md
- refmotion_gs_mvp/outputs/phase3/milestone_31_short_audit.md
- outputs/phase2/theory_rewrite.md
- outputs/phase2/reviewer_attack.md
- outputs/phase2/core_contribution_reduction.md

## Success Criteria
- The audit determines whether Milestone 3.2 dense / tangent-space normal optimization is sufficiently specified, in scope, testable, and safe to implement.
- The audit does not require Milestone 3.2 results yet.
- The audit writes `refmotion_gs_mvp/outputs/phase3/milestone_32_preimplementation_audit.md`.
- The audit updates `DECISION_LOG.md`.
- The audit updates `IMPLEMENTATION_LOG.md`.
- The audit updates `NEXT_ACTION.md`.

## Stop Conditions
- If the current session is not GPT-5.5 xhigh, stop and request xhigh.
- If the audit verdict is `BLOCKED UNTIL PLAN FIXES` or `REJECTED / REPLAN REQUIRED`, do not implement Milestone 3.2.
- If the audit verdict is `APPROVED TO IMPLEMENT` or `APPROVED WITH REQUIRED FIXES` without P0 blockers, set `NEXT_ACTION.md` to implement Milestone 3.2 using GPT-5.5 high.

## Expected Files To Create Or Update
- refmotion_gs_mvp/outputs/phase3/milestone_32_preimplementation_audit.md
- refmotion_gs_mvp/DECISION_LOG.md
- refmotion_gs_mvp/IMPLEMENTATION_LOG.md
- refmotion_gs_mvp/NEXT_ACTION.md

## Next Action Update Rule
- If approved with no P0 blockers, replace this file with an `implementation` action for Milestone 3.2 using GPT-5.5 high and `refmotion_gs_mvp/PROMPTS/milestone_implementation_prompt.md`.
- If blocked or rejected, replace this file with the exact planning repair task using GPT-5.5 high unless the audit says xhigh is required.
