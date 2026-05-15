# Pre-Implementation Authorization Audit

## Verdict

APPROVED WITH REQUIRED FIXES

Milestone 3.3 is authorized for implementation. The repaired `PHASE3_PLAN.md` now specifies the analytic near-object fallback path at an implementation-ready level and resolves the previous P0 blockers. Remaining fixes are P1 implementation-time clarifications, not blockers.

## Evidence Reviewed

- `refmotion_gs_mvp/AGENTS.md`
- `refmotion_gs_mvp/ACTIVE_SCOPE.md`
- `refmotion_gs_mvp/OPERATING_PROTOCOL.md`
- `refmotion_gs_mvp/NEXT_ACTION.md`
- `refmotion_gs_mvp/PROMPTS/continue_current_work_prompt.md`
- `refmotion_gs_mvp/PROMPTS/pre_major_milestone_audit_prompt.md`
- `refmotion_gs_mvp/PROJECT_PLAN.md`
- `refmotion_gs_mvp/PHASE3_PLAN.md`
- `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`
- `refmotion_gs_mvp/MVP_RESULTS.md`
- `refmotion_gs_mvp/DECISION_LOG.md`
- `refmotion_gs_mvp/outputs/phase3/milestone_32_revision_short_audit.md`
- `refmotion_gs_mvp/outputs/phase3/milestone_32_dense_normals/metrics.json`
- `refmotion_gs_mvp/outputs/phase3/milestone_32_dense_normals/summary.md`
- `outputs/phase2/theory_rewrite.md`
- `outputs/phase2/reviewer_attack.md`
- `outputs/phase2/core_contribution_reduction.md`
- `outputs/phase2/anti_cheating_constraints.md`
- Context-only source and tests:
  - `refmotion_gs_mvp/src/synthetic_scene.py`
  - `refmotion_gs_mvp/src/losses.py`
  - `refmotion_gs_mvp/src/dense_normal_optimization.py`
  - `refmotion_gs_mvp/src/decision_checks.py`
  - `refmotion_gs_mvp/scripts/run_phase3_milestone32.py`
  - `refmotion_gs_mvp/tests/test_phase3_milestone32_runner.py`

Additional checks:

```bash
which blender
git diff --name-only refmotion_gs_mvp/src refmotion_gs_mvp/scripts refmotion_gs_mvp/tests
jq '.decision_checks, .phase3, .dense_normal_optimization | . ' refmotion_gs_mvp/outputs/phase3/milestone_32_dense_normals/metrics.json
rg -n "8\\.[0-9]|Milestone 3\\.3|analytic near-object|near_object_scene|run_phase3_milestone33|test_near_object_scene|metrics\\.json|Decision Gates|Scope Lock|Formulation" refmotion_gs_mvp/PHASE3_PLAN.md
rg -n "learned near-field|inter-reflection|full PBR|relighting|material editing|representation novelty|oracle mask|noisy mask|TextureSplat|MaterialRefGS|SpecTRe-GS|Ref-DGS" refmotion_gs_mvp/PHASE3_PLAN.md refmotion_gs_mvp/ACTIVE_SCOPE.md outputs/phase2/*.md
```

Observed:

- `which blender`: exit code `1`, no executable found on `PATH`.
- Source/script/test tracked diff check: no paths printed.
- Milestone 3.2 remains accepted only as a lower-cost analytic smoke diagnostic:
  - `dense_normal_error_improves_10_percent`: true.
  - `dense_beats_no_cycle_ablation`: true.
  - `routing_beats_all_pixels`: true.
  - `routing_beats_noisy_mask`: true.
  - `routing_beats_oracle_mask`: false.
  - forbidden-component flags remain false.
- The repaired Milestone 3.3 plan now defines scene design, fallback path, public API, tests, output schema, verification commands, baselines, and decision gates.

## Pass/Fail Table

| Criterion | Status | Evidence |
|---|---|---|
| Scope compliance | PASS | Section 8.2 forbids learned near-field reflection fields, inter-reflection residuals, full PBR optimization, relighting/material editing, and representation-novelty claims. |
| Formulation compliance | PASS | Section 8.4 requires reuse of Formulation A, `reflection_cycle_loss`, dense tangent-space normal optimization, and no-cycle ablation. |
| Implementation readiness | PASS | Sections 8.3-8.6 define the analytic near-object scene, camera split, reflector primitives, observation rule, files, and public API. |
| Test readiness | PASS WITH P1 FIXES | Section 8.7 defines test files and assertions. One test should be implemented through explicit runner scope flags or explicit scene metadata rather than an undefined metadata claim. |
| Baseline preservation | PASS | Section 8.9 preserves all-pixel, oracle mask exclusion, noisy mask-only, reflection-confidence routing, normal-refinement-plus-routing, global rotation reference, dense no-cycle ablation, and dense reflection-cycle optimizer. |
| Metric and output readiness | PASS WITH P1 FIXES | Section 8.8 defines the output directory, required files, schema, plots, and summary requirements. Implementation should consistently alias `dense_normal_optimization` as the dense reflection-cycle optimizer in summary text and checks. |
| Decision gates | PASS | Section 8.11 defines pass, revise, pivot, stop, and post-result audit gates, including reflector hit fraction, normal improvement, no-cycle comparison, routing checks, and forbidden-component flags. |
| Reviewer-risk coverage | PASS | Sections 8.12 and 9 cover MaterialRefGS, TextureSplat, SpecTRe-GS, Ref-DGS, mask-only, and analytic-fallback limitations. |
| Environment readiness | PASS | Blender is unavailable, and section 8.1 correctly defines analytic near-object fallback as the current implementation path. |
| Code-change safety | PASS | This audit did not implement Milestone 3.3 code and did not modify source, scripts, or tests. |

## Findings

1. The previous P0 blockers are resolved. The plan no longer leaves the future implementation session to invent the scene, files, tests, output schema, metrics, verification commands, baseline mapping, fallback trigger, or decision gates.

2. The analytic near-object fallback is in scope. The planned finite colored reflector primitives are deterministic synthetic data-generation components, not learned near-field reflection fields or a renderer novelty claim.

3. The plan preserves Formulation A. Dense normal changes affect reflected-ray geometry through `reflection_cycle_loss`, and the proposed dense optimizer is still compared against a no-cycle dense ablation and the global-rotation reference.

4. The baseline suite is preserved and the oracle-mask threat remains binding. The plan explicitly requires reporting all-pixel, noisy-mask, oracle-mask, routing, normal-refinement-plus-routing, dense no-cycle, and dense reflection-cycle results.

5. The output and audit chain are clear. The implementation must write `metrics.json`, `summary.md`, plots, logs, and then set `NEXT_ACTION.md` to a post-result GPT-5.5 xhigh audit rather than continuing automatically.

6. Two implementation-time details need tightening, but neither requires another planning cycle:
   - the `trace_reflector_color` return order should be explicit in code/tests as `(colors, hit_mask, reflector_id)`;
   - scope flags should be tested through explicit runner `phase3` fields or explicit scene metadata, not by relying on absent metadata.

## Required Fixes

- P0: None.
- P1: During implementation, make the `trace_reflector_color` return order explicit and test it.
- P1: During implementation, ensure scope-guard tests inspect explicit `phase3` runner flags or explicit scene metadata.
- P1: During implementation, use consistent naming for the proposed dense method: schema may use `dense_normal_optimization`, but summaries and checks should state that it is the dense reflection-cycle optimizer.

## Authorization Decision

- Milestone 3.3 is authorized for implementation.
- Verdict: `APPROVED WITH REQUIRED FIXES`.
- The required fixes are P1 and can be resolved during implementation.
- Implementation must use GPT-5.5 high and execute only Milestone 3.3.
- After implementation and verification, Milestone 3.3 must receive a GPT-5.5 xhigh post-result full go/no-go audit before acceptance.

## Next Action

- Implement Milestone 3.3 analytic near-object fallback validation using `PROMPTS/milestone_implementation_prompt.md`.
- Do not implement learned near-field reflection fields, inter-reflection residuals, full PBR optimization, relighting, material editing, or representation-novelty claims.
