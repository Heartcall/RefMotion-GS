# Short Audit Prompt

Use this prompt after a small milestone.

## Role

You are Codex auditing a small RefMotion-GS milestone inside `/home/liuly/Surface_Reconstruction/Glossy/new_idea`.

Use GPT-5.5 high. Be skeptical and code-grounded.

## Required Reads

Read:

1. `refmotion_gs_mvp/ACTIVE_SCOPE.md`
2. `refmotion_gs_mvp/NEXT_ACTION.md`
3. `refmotion_gs_mvp/OPERATING_PROTOCOL.md`
4. files changed in the milestone,
5. tests changed in the milestone,
6. latest output metrics and result summary,
7. latest `IMPLEMENTATION_LOG.md` entry.

## Audit Questions

Answer these directly:

1. Did the milestone stay inside RefMotion-GS scope?
2. Did it avoid learned near-field reflection fields, inter-reflection residuals, full PBR, relighting, and material editing?
3. Are mesh, UV, PBR, or Gaussian components treated only as scaffolding?
4. Do tests cover the new behavior?
5. Did verification commands run, and what were the exact results?
6. Did the change preserve existing MVP baselines?
7. Did metrics improve, regress, or remain inconclusive?
8. Is the next action implementation, planning, full audit, pivot discussion, or stop?

## Output Format

Write a concise audit section to the relevant result file or `IMPLEMENTATION_LOG.md`:

```markdown
### Short Audit

Evidence:

- ...

Findings:

- PASS/REVISE/FAIL: ...

Decision:

- ...

Next action:

- ...
```

Then update `DECISION_LOG.md` and `NEXT_ACTION.md`.

