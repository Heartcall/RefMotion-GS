# Full GPT-5.5 xhigh Go/No-Go Audit Prompt

Use this prompt for major stages, phase transitions, claim changes, or any go/no-go decision.

## Role

You are Codex performing a full RefMotion-GS audit inside `/home/liuly/Surface_Reconstruction/Glossy/new_idea`.

Use **GPT-5.5 xhigh**. Be adversarial, code-grounded, and evidence-bound. Do not give a continue decision unless the files, commands, and metrics support it.

## Required Reads

Read all of:

1. `refmotion_gs_mvp/ACTIVE_SCOPE.md`
2. `refmotion_gs_mvp/NEXT_ACTION.md`
3. `refmotion_gs_mvp/OPERATING_PROTOCOL.md`
4. `refmotion_gs_mvp/PROJECT_PLAN.md`
5. `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`
6. `refmotion_gs_mvp/MVP_RESULTS.md`
7. `refmotion_gs_mvp/DECISION_LOG.md`
8. all relevant `outputs/phase2/*.md`
9. current source under `refmotion_gs_mvp/src/`
10. current scripts under `refmotion_gs_mvp/scripts/`
11. current tests under `refmotion_gs_mvp/tests/`
12. latest result metrics and plots under `refmotion_gs_mvp/outputs/`

## Scope Guard

Reject the stage if it depends on:

- learned near-field reflection fields,
- inter-reflection residuals,
- full PBR optimization,
- relighting,
- material editing,
- novelty claims around mesh, UV, PBR, or Gaussian representation.

The only allowed novelty frame is reflection-induced multi-view motion as supervision for normals and texture-leakage control.

## Audit Checklist

Evaluate:

1. **Scope:** Is this still RefMotion-GS?
2. **Formulation:** Is Formulation A still explicit and reproducible?
3. **Gradient/evidence path:** Does the implemented signal actually affect normals or routing rather than only post-hoc filtering?
4. **Baselines:** Are all-pixel, oracle mask, noisy mask, reflection-confidence routing, and normal-refinement routing present?
5. **Mask-only threat:** Does the method add evidence beyond simple reflective-pixel exclusion?
6. **Normal evidence:** Does reflective-region normal angular error improve under a less favorable optimizer than global rotation?
7. **Texture evidence:** Does specular leakage decrease versus all-pixel and noisy-mask baselines, and how does it compare to oracle mask?
8. **Renderer validity:** Is the synthetic setup strong enough for the claimed decision?
9. **Tests:** Do unit and diagnostic tests cover the new stage?
10. **Reproducibility:** Can another Codex session rerun the commands and get the same result files?
11. **Reviewer risks:** Address MaterialRefGS, SpecTRe-GS, Ref-DGS, TextureSplat, and mask-only objections.
12. **Claim discipline:** Are relighting, material editing, full PBR, and representation novelty absent from claims?

## Required Output

Write a full audit markdown file under an appropriate output directory, for example:

`refmotion_gs_mvp/outputs/phase3/full_go_no_go.md`

Use this structure:

```markdown
# RefMotion-GS Full Go/No-Go Audit

## Verdict

GO / GO AFTER REVISION / PIVOT / STOP

## Evidence Reviewed

- ...

## Pass/Fail Table

| Criterion | Status | Evidence |
|---|---|---|
| Scope discipline | PASS/FAIL | ... |

## Major Findings

1. ...

## Required Revisions

- ...

## Decision

- ...

## Next Action

- ...
```

Then update:

- `refmotion_gs_mvp/DECISION_LOG.md`
- `refmotion_gs_mvp/NEXT_ACTION.md`
- `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`

Stop if the verdict is pivot or stop, or if revisions need user input.

