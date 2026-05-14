# Phase 3 Milestone Summary

## Metadata

- milestone: 3.1
- purpose: experiment_framework_refactor
- implemented_dense_normal_optimization: false
- implemented_learned_near_field_reflection: false

## Decision Checks

- loss_correlated_near_gt: true
- normal_error_improves_10_percent: true
- routing_beats_all_pixels: true
- routing_beats_noisy_mask: true
- routing_beats_oracle_mask: false

## Oracle Mask Status

- routing_beats_oracle_mask: false
- oracle mask exclusion leakage: 0.18894842742715495
- normal refinement plus routing leakage: 0.19090032877604535
- inference: routing does not beat oracle mask exclusion on this leakage metric and must be interpreted against noisy-mask, albedo, UV seam, or normal-accuracy evidence.
