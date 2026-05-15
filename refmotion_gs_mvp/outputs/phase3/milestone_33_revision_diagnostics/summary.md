# Phase 3 Milestone 3.3 Revision Diagnostics Summary

## Evidence

- reflector_hit_fraction: 0.15492957746478872
- active_texel_count: 64
- active_texel_hit_fraction_mean: 0.17395833333333333
- active_texels_without_finite_hits: 34
- accepted_update_count: 8
- worsened_reflective_update_count: 5
- objective_reflective_error_correlation: 0.29366840127375765
- final_reflective_improvement_percent: 0.7685068728508346
- normal_refinement_improves_over_reflection_confidence: false
- normal_refinement_beats_noisy_mask: true
- normal_refinement_beats_oracle_mask: false

## Reflector Primitive Reconciliation

- The implemented Milestone 3.3 radii are treated as the recorded diagnostic scene for this revision.
- Larger radii were used to obtain a minimum finite-reflector hit fraction in the low-resolution smoke scene.
- The hit fraction is barely above the gate, so it is not a strong realism claim.
- reflector 0: center=[1.75, 0.1, 1.15], radius=0.765, color=[0.95, 0.1, 0.08]
- reflector 1: center=[-1.55, 0.35, 1.35], radius=0.68, color=[0.08, 0.85, 0.18]
- reflector 2: center=[0.15, 1.45, -1.55], radius=0.85, color=[0.12, 0.22, 0.95]

## Routing Diagnostics

- all-pixel leakage: 0.9658763096531678
- noisy-mask leakage: 0.5556875799054598
- reflection-confidence routing leakage: 0.4632458373229172
- normal-refinement-plus-routing leakage: 0.4714538905111631
- oracle mask exclusion leakage: 0.17595366303189766
- oracle mask exclusion remains an honest comparator and is still reported even when stronger.

## Inference

- The diagnostic output measures whether objective descent aligns with reflective-region normal correctness.
- Normal-refinement-plus-routing is explicitly compared with reflection-confidence routing, noisy-mask-only, and oracle mask exclusion.
- The revision remains controlled synthetic evidence and does not support paper-level claims by itself.

## Decision

- recommendation: revise: dense trajectory diagnostics explain the failed 10 percent normal gate

## Next Action

- Run a short audit before treating this revision state as accepted.
