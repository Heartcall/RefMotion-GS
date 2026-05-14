# Fixed Workflow Files Recheck

## Files Changed

- `AGENTS.md`
- `refmotion_gs_mvp/PROMPTS/continue_current_work_prompt.md`
- `refmotion_gs_mvp/OPERATING_PROTOCOL.md`
- `refmotion_gs_mvp/NEXT_ACTION.md`
- `refmotion_gs_mvp/outputs/audits/fixed_workflow_files_recheck.md`

## Checks Performed

- Read `refmotion_gs_mvp/AGENTS.md` before making project changes.
- Confirmed `refmotion_gs_mvp/AGENTS.md` remains the authoritative project instruction file.
- Confirmed the root `AGENTS.md` points future sessions to `refmotion_gs_mvp/AGENTS.md` before any work.
- Confirmed `PROMPTS/continue_current_work_prompt.md` is self-contained and instructs future sessions to read `ACTIVE_SCOPE.md`, `OPERATING_PROTOCOL.md`, `NEXT_ACTION.md`, `DECISION_LOG.md`, latest logs/results, and continue exactly from `NEXT_ACTION.md`.
- Confirmed `OPERATING_PROTOCOL.md` lists the four entry prompts:
  - Entry A: Continue current work -> `PROMPTS/continue_current_work_prompt.md`
  - Entry B: Execute current milestone -> `PROMPTS/milestone_implementation_prompt.md`
  - Entry C: Small milestone audit -> `PROMPTS/short_audit_prompt.md`
  - Entry D: Major-stage full audit -> `PROMPTS/full_xhigh_audit_prompt.md`
- Confirmed `NEXT_ACTION.md` makes the current action audit-only:
  - "Run the Phase 3 planning audit using PROMPTS/full_xhigh_audit_prompt.md. Do not begin implementation until the audit verdict is PLAN APPROVED or PLAN APPROVED WITH REQUIRED FIXES and all P0 fixes are resolved."
- Confirmed dense / tangent-space normal optimization is listed only as Candidate Milestone 3.2 under "Candidate Next Action After Audit".
- Confirmed the milestone convention is explicit:
  - Milestone 3.1: Experiment framework refactor.
  - Milestone 3.2: Dense / tangent-space normal optimization.
- Confirmed no experiment source, tests, runners, or metrics were intentionally changed.

Text checks run:

```bash
rg -n "Entry A: Continue current work|Entry B: Execute current milestone|Entry C: Small milestone audit|Entry D: Major-stage full audit|continue_current_work_prompt|milestone_implementation_prompt|short_audit_prompt|full_xhigh_audit_prompt" refmotion_gs_mvp/OPERATING_PROTOCOL.md
rg -n "Run the Phase 3 planning audit using PROMPTS/full_xhigh_audit_prompt.md|PLAN APPROVED|Candidate Next Action After Audit|Milestone 3.1: Experiment framework refactor|Milestone 3.2: Dense / tangent-space normal optimization|Candidate Milestone 3.2" refmotion_gs_mvp/NEXT_ACTION.md
rg -n "Candidate Milestone 3\\.1|dense.*Milestone 3\\.1|tangent.*Milestone 3\\.1|Milestone 3\\.1.*normal|normal.*Milestone 3\\.1" refmotion_gs_mvp/NEXT_ACTION.md refmotion_gs_mvp/OPERATING_PROTOCOL.md refmotion_gs_mvp/PROMPTS/continue_current_work_prompt.md
git diff --name-only -- refmotion_gs_mvp/src refmotion_gs_mvp/scripts refmotion_gs_mvp/tests
```

Observed:

- Required entry prompt lines are present in `OPERATING_PROTOCOL.md`.
- Required current-action, approval-gate, candidate-action, and milestone-numbering lines are present in `NEXT_ACTION.md`.
- No stale dense-normal-as-Milestone-3.1 reference was found by the stale-reference search.
- No tracked source, script, or test file diff was reported.

## Readiness

The persistent workflow is now ready for future Codex-only execution. A future session can start from Entry A, read `NEXT_ACTION.md`, run the Phase 3 planning audit using `PROMPTS/full_xhigh_audit_prompt.md`, and avoid implementation until the audit verdict allows it and all P0 fixes are resolved.
