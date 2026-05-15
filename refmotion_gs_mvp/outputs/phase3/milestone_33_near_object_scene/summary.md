# Phase 3 Milestone 3.3 Near-Object Scene Summary

## Scene Path

- renderer_path: analytic_near_object_fallback
- reason: Blender/Cycles is unavailable on PATH, so the audited analytic fallback is the current implementation path.
- reflector_hit_fraction: 0.15492957746478872
- reflector_hit_fraction_sufficient: true

## Loss Landscape

- 0deg: 0.01518530465164876
- 5deg: 0.015862829735769086
- 10deg: 0.01802097308944506
- loss_correlated_near_gt: true

## Dense Reflection-Cycle Optimizer

- method_name: dense_reflection_cycle_optimizer
- reflective_error_improvement_percent: 0.7685068728508346
- dense_normal_error_improves_10_percent: false
- dense_beats_no_cycle_ablation: true
- dense final reflective error: 5.666570971472453
- no-cycle final reflective error: 5.710456219994247

## Texture And Mask Baselines

- routing_beats_all_pixels: true
- routing_beats_noisy_mask: true
- routing_beats_oracle_mask: false
- oracle mask exclusion leakage: 0.17595366303189766
- normal refinement plus routing leakage: 0.4714538905111631

## Scope Flags

- used_blender_cycles: false
- implements_learned_near_field_reflection_field: false
- implements_inter_reflection_residual: false
- implements_full_pbr_optimization: false
- claims_relighting_or_material_editing: false
- claims_representation_novelty: false

## Recommendation

- revise: dense normal improvement is positive but below the 10 percent gate

## Reviewer Risk Boundary

- Evidence remains controlled synthetic analytic evidence, not a paper-level success claim.
- MaterialRefGS / photometric-variation risk is not fully closed because this is not a MaterialRefGS baseline.
- TextureSplat / texture-only risk is addressed only through retained texture-only, mask-only, and routing baselines.
- SpecTRe-GS and Ref-DGS overlap is avoided because no learned near-field reflection field or local reflection Gaussian is implemented.
- Mask-only threat remains binding; oracle mask exclusion is reported even when stronger.
