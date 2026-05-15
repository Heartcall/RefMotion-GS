# Phase 3 Milestone 3.2 Dense Normal Summary

## Dense Normal Optimization

- result status: lower-cost analytic smoke diagnostic, not full dense-normal validation
- reflective_error_improvement_percent: 11.305327524690204
- dense_normal_error_improves_10_percent: true
- dense_beats_no_cycle_ablation: true
- dense final reflective error: 5.0236136352350576
- no-cycle final reflective error: 5.663940679902162
- interpretation: dense reflective-region normal error clears the 10 percent gate by a narrow margin, so this is a positive but marginal signal.
- global rotation reference improvement percent: 67.41279022743005
- global rotation reference final reflective error: 1.8457202307536418
- interpretation: the favorable global-rotation reference remains much stronger than the dense tangent-space optimizer, as expected for this stricter diagnostic.

## Runner Configuration

- uv_height: 16
- uv_width: 32
- active_texels: 64
- dense_iterations: 8
- sample_count: 40
- seed: 53
- loss_seed: 59
- update_radius: 1
- local proposal policy: `update_radius = 1` applies a signed tangent-channel step to the selected texel and immediate valid sphere-UV neighbors. This is a local-neighborhood coordinate proposal, not strict single-texel coordinate search.
- sampling policy: `sample_count = 40` is the accepted Milestone 3.2 smoke-run configuration for repeatable Codex execution time. A stricter `sample_count = 250` rerun is deferred to a separate action if required.

## Texture And Mask Baselines

- routing_beats_all_pixels: true
- routing_beats_noisy_mask: true
- routing_beats_oracle_mask: false
- oracle mask exclusion leakage: 0.18623485108324137
- normal refinement plus routing leakage: 0.35270156748629633
- interpretation: normal refinement plus routing reduces leakage versus all-pixel and noisy-mask baselines, but oracle mask exclusion remains substantially stronger on leakage.
- measured continuation basis: the current evidence supports only continued diagnostic work from dense normal improvement and noisy-mask robustness, not oracle-mask superiority.

## Reviewer Risk Boundary

- Evidence remains synthetic analytic evidence, not a paper-level success claim.
- MaterialRefGS / photometric-variation risk is not fully closed by this milestone.
- TextureSplat / texture-only risk is addressed only through preserved texture and mask baselines.
- SpecTRe-GS and Ref-DGS overlap is avoided because no learned near-field reflection field or local reflection Gaussian is implemented.
- Mask-only threat remains binding; oracle mask exclusion is reported even when stronger.
