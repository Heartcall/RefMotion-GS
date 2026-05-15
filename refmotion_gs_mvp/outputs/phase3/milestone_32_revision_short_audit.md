# Milestone 3.2 Revision Short Audit

### Short Audit

Evidence:

- Read `ACTIVE_SCOPE.md`, `NEXT_ACTION.md`, `OPERATING_PROTOCOL.md`, latest `IMPLEMENTATION_LOG.md`, latest `DECISION_LOG.md`, `MVP_RESULTS.md`, `PHASE3_PLAN.md`, `outputs/phase3/milestone_32_post_result_audit.md`, `outputs/phase3/milestone_32_dense_normals/metrics.json`, `outputs/phase3/milestone_32_dense_normals/summary.md`, `src/dense_normal_optimization.py`, `scripts/run_phase3_milestone32.py`, and `tests/test_phase3_milestone32_runner.py`.
- `PHASE3_PLAN.md` now distinguishes the accepted Milestone 3.2 smoke configuration from stricter deferred settings:
  - accepted smoke `sample_count`: `40`.
  - stricter deferred `sample_count`: `250`.
  - accepted smoke `update_radius`: `1`.
  - strict single-texel `update_radius`: `0`.
- `PHASE3_PLAN.md` now states that `update_radius = 1` is a local-neighborhood coordinate proposal and must not be described as strict single-texel coordinate search.
- `summary.md` now reports:
  - lower-cost analytic smoke diagnostic status.
  - exact runner configuration: `uv_height = 16`, `uv_width = 32`, `active_texels = 64`, `dense_iterations = 8`, `sample_count = 40`, `seed = 53`, `loss_seed = 59`, `update_radius = 1`.
  - dense reflective-region normal improvement is marginal: `11.305327524690204` percent.
  - global-rotation reference remains much stronger: `67.41279022743005` percent improvement and `1.8457202307536418` deg final reflective error.
  - oracle mask exclusion remains substantially stronger on leakage: `0.18623485108324137` versus normal-refinement-plus-routing `0.35270156748629633`.
- Current metrics preserve required decision checks:
  - `dense_normal_error_improves_10_percent`: true.
  - `dense_beats_no_cycle_ablation`: true.
  - `routing_beats_all_pixels`: true.
  - `routing_beats_noisy_mask`: true.
  - `routing_beats_oracle_mask`: false.
- Phase 3 scope flags remain false for forbidden components:
  - `implemented_learned_near_field_reflection`: false.
  - `implemented_inter_reflection_residual`: false.
  - `implemented_full_pbr_optimization`: false.
  - `claimed_relighting_or_editing`: false.
- Verification commands run during this audit:

```bash
pytest refmotion_gs_mvp/tests/test_phase3_milestone32_runner.py -q
python -m py_compile refmotion_gs_mvp/src/dense_normal_optimization.py refmotion_gs_mvp/scripts/run_phase3_milestone32.py
jq empty refmotion_gs_mvp/outputs/phase3/milestone_32_dense_normals/metrics.json
git diff --name-only refmotion_gs_mvp/src refmotion_gs_mvp/scripts refmotion_gs_mvp/tests
```

Observed:

- Runner schema test: `1 passed in 7.69s`.
- Python compilation: exit code 0.
- `metrics.json` JSON validation: exit code 0.
- Source/script/test tracked diff check: no paths printed.

Findings:

- PASS: The revision stayed inside RefMotion-GS scope and did not introduce learned near-field reflection fields, inter-reflection residuals, full PBR optimization, relighting, material editing, or representation-novelty claims.
- PASS: Mesh, UV, and texture-baking components remain scaffolding for normal and leakage evaluation.
- PASS: The post-result audit P0 mismatch is resolved by documenting the existing result as a lower-cost analytic smoke diagnostic rather than claiming it used the stricter planned setting.
- PASS: The plan and summary no longer conflict with the executed `sample_count = 40` and `update_radius = 1` run.
- PASS WITH CAUTION: The Milestone 3.2 result remains positive but narrow. Dense normal improvement barely clears the 10 percent gate, global-rotation reference is much stronger, and oracle mask exclusion remains substantially better on leakage.
- PASS: Existing runner schema and scope-flag tests still cover the relevant output structure and forbidden-component flags.
- INCONCLUSIVE FOR FULL CLAIMS: Metrics remain synthetic analytic evidence and do not justify a paper-level success claim.

Decision:

- Short audit verdict: `PASS`.
- The Milestone 3.2 revision state is accepted as a documented smoke-result state.
- Do not begin Milestone 3.3 implementation without a GPT-5.5 xhigh pre-implementation authorization audit.

Next action:

- Run a GPT-5.5 xhigh pre-implementation authorization audit for Milestone 3.3 stricter scene or renderer validation using `PROMPTS/pre_major_milestone_audit_prompt.md`.
