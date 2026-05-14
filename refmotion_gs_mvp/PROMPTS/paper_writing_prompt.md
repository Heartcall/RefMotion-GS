# Paper Writing Prompt

Use this prompt when RefMotion-GS needs a paper section, advisor-facing report, or claim rewrite.

## Role

You are Codex writing from evidence inside `/home/liuly/Surface_Reconstruction/Glossy/new_idea`. The active project is `refmotion_gs_mvp`, named RefMotion-GS.

Use GPT-5.5 high for normal writing. Use GPT-5.5 xhigh if the writing changes the central claim or go/no-go decision.

## Required Reads

Read:

1. `refmotion_gs_mvp/ACTIVE_SCOPE.md`
2. `refmotion_gs_mvp/PROJECT_PLAN.md`
3. `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`
4. `refmotion_gs_mvp/MVP_RESULTS.md`
5. `refmotion_gs_mvp/DECISION_LOG.md`
6. latest relevant output metrics and summaries,
7. `outputs/phase2/novelty_audit.md`
8. `outputs/phase2/core_contribution_reduction.md`
9. `outputs/phase2/reviewer_attack.md`
10. `outputs/phase2/theory_rewrite.md`

## Claim Boundaries

Allowed wording:

- "reflection-induced multi-view motion"
- "reflective-region normal supervision"
- "feature-space reflection-cycle consistency"
- "specular leakage in texture baking"
- "synthetic controlled evidence"
- "continue with caution" when evidence is preliminary

Disallowed wording unless a future full audit explicitly approves it:

- "full RefTex-GS"
- "learned near-field reflection field"
- "inter-reflection residual"
- "full PBR optimization"
- "relighting"
- "material editing"
- "mesh/UV/PBR/Gaussian representation is the novelty"
- "solves reflective object reconstruction"
- "state of the art" without direct comparative evidence.

## Required Writing Discipline

Separate:

- hypothesis,
- method,
- evidence,
- inference,
- limitations,
- next validation.

When evidence is preliminary, say so. Do not convert analytic MVP results into real-world claims.

## Suggested Abstract Claim

RefMotion-GS studies whether reflection-induced multi-view motion can serve as a geometric supervision signal for reflective-region normals and reduce specular leakage during texture recovery. Instead of introducing a learned near-field reflection field, the current formulation uses reflected-ray geometry and frozen feature correspondences to test whether reflection motion provides information beyond photometric texture stationarity and mask-only exclusion.

## Required Output

Write the requested paper/report file in the project or output directory. Then update `IMPLEMENTATION_LOG.md` with:

- file written,
- evidence sources used,
- claim boundary,
- remaining limitations.

If the writing changes a project decision, also update `DECISION_LOG.md` and `NEXT_ACTION.md`.

