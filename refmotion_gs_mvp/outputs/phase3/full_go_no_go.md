# RefMotion-GS Phase 3 Planning Audit

## Verdict

**PLAN APPROVED WITH REQUIRED FIXES**

The Phase 3 direction is inside RefMotion-GS scope and should continue, but implementation must not start yet. The current "plan" exists only as `NEXT_ACTION.md` plus earlier MVP notes; no dedicated `PHASE3_PLAN.md` or equivalent Phase 3 plan file is present. That is a P0 planning gap because Milestone 3.1 is supposed to be an experiment framework refactor, while dense / tangent-space normal optimization is only Candidate Milestone 3.2.

## Evidence Reviewed

- `refmotion_gs_mvp/ACTIVE_SCOPE.md`
- `refmotion_gs_mvp/NEXT_ACTION.md`
- `refmotion_gs_mvp/OPERATING_PROTOCOL.md`
- `refmotion_gs_mvp/PROJECT_PLAN.md`
- `refmotion_gs_mvp/IMPLEMENTATION_LOG.md`
- `refmotion_gs_mvp/MVP_RESULTS.md`
- `refmotion_gs_mvp/DECISION_LOG.md`
- `outputs/phase2/final_go_no_go.md`
- `outputs/phase2/theory_rewrite.md`
- `outputs/phase2/reviewer_attack.md`
- `outputs/phase2/core_contribution_reduction.md`
- `outputs/phase2/anti_cheating_constraints.md`
- `outputs/phase2/mvp_implementation_plan.md`
- `outputs/phase2/novelty_audit.md`
- Current source under `refmotion_gs_mvp/src/`
- Current script `refmotion_gs_mvp/scripts/run_mvp_diagnostics.py`
- Current tests under `refmotion_gs_mvp/tests/`
- Latest metrics in `refmotion_gs_mvp/outputs/run_latest/metrics.json`

No dedicated Phase 3 plan file was found by searching for `PHASE3_PLAN.md`, `*phase3*plan*.md`, or `refmotion_gs_mvp/outputs/phase3/*` before this audit report was created.

## Pass/Fail Table

| Criterion | Status | Evidence |
|---|---|---|
| Scope discipline | PASS | `ACTIVE_SCOPE.md`, `PROJECT_PLAN.md`, and `NEXT_ACTION.md` keep the project as RefMotion-GS and exclude learned near-field fields, inter-reflections, full PBR, relighting, material editing, and representation-novelty claims. |
| Formulation A clarity | PASS FOR MVP, P0 FOR PHASE 3 PLAN | `theory_rewrite.md` defines reflected-ray correspondence and the current `losses.py` implements RGB feature-space reflected-ray matching, but the Phase 3 plan has not yet specified how Milestone 3.1 will preserve or expose this formulation in a reusable framework. |
| Gradient / evidence path | REVISE | Current normal improvement comes from `optimize_global_normal_rotation`, a favorable global coordinate search. This validates signal presence but not dense or tangent-space optimization. |
| Baselines | PASS FOR MVP, P0 FOR PHASE 3 PLAN | MVP includes all-pixel, oracle mask exclusion, noisy mask only, reflection-confidence routing, and normal-refinement plus routing. Phase 3 still needs a plan that preserves these baselines in the refactored runner. |
| Mask-only threat | REVISE | Sphere-UV leakage is `0.19090032877604535` for normal-refinement plus routing versus better oracle mask leakage `0.18894842742715495`; evidence beyond simple exclusion is currently strongest under noisy masks and albedo RMSE, not oracle leakage. |
| Normal evidence | REVISE | Reflective normal error improved from `5.7091979244066104` to `0.3569152456956942` degrees, but only under global rotation. Phase 3 must test less favorable normal degrees of freedom. |
| Texture evidence | REVISE | Routing beats all-pixel and noisy-mask leakage, but does not beat oracle mask leakage. Phase 3 must explicitly measure whether added normal/reflection evidence improves beyond exclusion under stricter setups. |
| Renderer validity | REVISE | The analytic renderer uses fixed reflected-color lobes, not Blender/Cycles or explicit near-object geometry. This is acceptable for MVP continuation, not for strong method claims. |
| Tests | PASS FOR MVP, P0 FOR PHASE 3 PLAN | Current tests cover cameras, reflection geometry, loss ordering, global normal optimization, metrics, and sphere UV baking. Phase 3 must specify new tests before new experiment code. |
| Reproducibility | PASS FOR MVP, P0 FOR PHASE 3 PLAN | `run_mvp_diagnostics.py` writes deterministic metrics and plots. Phase 3 needs dedicated output directories and summaries before implementation. |
| Reviewer risks | REVISE | The reduced scope addresses SpecTRe-GS / Ref-DGS overlap by avoiding learned near-field fields, but Phase 3 still needs explicit plan coverage for MaterialRefGS / photometric-variation and TextureSplat-style texture-only threats. |
| Claim discipline | PASS | Current docs do not claim relighting, material editing, full PBR, or mesh/UV/Gaussian representation novelty. |

## Major Findings

1. **No dedicated Phase 3 plan exists yet.** The current action asks for a Phase 3 planning audit, but the only concrete Phase 3 planning content is in `NEXT_ACTION.md` and post-MVP notes. This is insufficient for implementation.

2. **The Phase 3 direction is correct but under-specified.** The project should continue with stricter validation, but the next executable step should be a planning repair, not experiment code.

3. **Milestone numbering must be preserved.** Unless a future `PHASE3_PLAN.md` explicitly overrides it, Milestone 3.1 is experiment framework refactor and Milestone 3.2 is dense / tangent-space normal optimization. Dense normal optimization must not be implemented as Milestone 3.1.

4. **The mask-only objection is still the central risk.** Current routing beats all-pixel and noisy-mask baselines but does not beat oracle mask exclusion on leakage. Phase 3 must make this threat a first-class gate, not a secondary note.

5. **The current normal optimization evidence is favorable.** The global rotation optimizer is a useful signal diagnostic but not a strong optimization claim. Dense/tangent-space optimization belongs after a framework refactor and test plan.

## Required Revisions

### P0: Required Before Any Milestone 3.1 Implementation

- Create a dedicated Phase 3 plan file, preferably `refmotion_gs_mvp/PHASE3_PLAN.md`, that defines:
  - Milestone 3.1 as experiment framework refactor only.
  - Milestone 3.2 as dense / tangent-space normal optimization only after 3.1 passes.
  - Exact files to create or modify for Milestone 3.1.
  - Exact output directories and result-summary filenames.
  - Exact tests to add or update before implementation.
  - Exact verification commands.
  - The required baseline suite: all-pixel, oracle mask exclusion, noisy mask only, reflection-confidence routing, normal-refinement plus routing.
  - Explicit gates for `routing_beats_all_pixels`, `routing_beats_noisy_mask`, and comparison against `routing_beats_oracle_mask`.
  - A statement that no learned near-field reflection field, inter-reflection residual, full PBR optimization, relighting, material editing, or representation-novelty claim is allowed.

- Add a Phase 3 plan section that directly answers how the next milestones address:
  - the oracle-mask leakage threat,
  - the favorable global-rotation optimizer limitation,
  - analytic renderer limitations,
  - MaterialRefGS / photometric-variation and TextureSplat / texture-only objections.

### P1: Required Before Milestone 3.2 Approval

- Define a dense or tangent-space normal optimizer diagnostic that is less favorable than global rotation but still small enough for analytic smoke tests.
- Define a result schema that records reflective and non-reflective normal error, loss history, leakage, albedo RMSE, and all decision checks.
- Define a stricter scene or renderer upgrade path, either Blender/Cycles if available or a more explicit analytic near-object reflection scene.

## Decision

The Phase 3 concept is approved with required fixes. The project should not pivot or stop because the MVP signal has not been falsified. However, implementation remains blocked until the P0 planning fixes are complete and reviewed.

## Next Action

Resolve the P0 planning fixes by creating a dedicated Phase 3 plan file. Do not implement Milestone 3.1 experiment code until the plan explicitly passes the P0 requirements above.

