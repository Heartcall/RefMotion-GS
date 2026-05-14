# RefMotion-GS Active Scope

## Project Identity

Active project: **RefMotion-GS**.

RefMotion-GS is a reduced, falsifiable project about reflection-induced multi-view motion as a supervision signal for reflective-region normals and texture leakage control.

It is not the full RefTex-GS system.

## Core Hypothesis

Reflection-induced multi-view motion provides useful supervision for reflective-region normals and helps prevent specular leakage during texture recovery.

## Allowed First-Order Contributions

- Feature-space reflection-cycle consistency.
- Reflected-ray geometric correspondence.
- Reflective-region normal supervision.
- Texture-routing or baking diagnostics that measure specular leakage.
- Synthetic controlled evaluation with known normals, albedo, reflective masks, and reflected content.
- Baselines that test whether the signal adds value beyond all-pixel baking, oracle mask exclusion, noisy mask exclusion, and texture-only routing.

## Allowed Scaffolding

These are implementation or evaluation supports only, not novelty claims:

- analytic synthetic renderer,
- Blender/Cycles synthetic renderer if available,
- mesh or analytic surface,
- fixed UV or sphere UV atlas,
- 2DGS/PGSR initialization in later phases,
- Gaussian-related representation only if needed for an implementation baseline.

## Explicitly Out Of Scope

Do not implement:

- learned near-field reflection fields,
- inter-reflection residuals,
- full PBR optimization,
- relighting systems,
- material editing systems,
- high-capacity view-dependent reflection memorization,
- broad real-world reconstruction claims without direct evaluation.

Do not claim novelty for:

- mesh representation,
- UV representation,
- PBR representation,
- Gaussian representation,
- asset editing,
- relighting.

## Current Evidence Boundary

The current MVP evidence is analytic and preliminary:

- reflection-cycle loss is correlated with normal correctness on the analytic scene,
- constrained global normal-offset optimization improves reflective-region normal error,
- routing reduces leakage versus all-pixel and noisy-mask baking,
- routing does not beat oracle reflective-mask exclusion on leakage,
- albedo RMSE improves strongly in the current proxy evaluation.

Therefore the status is **continue with caution**, not solved.

## Active Frontier

Phase 3 should test whether the signal survives stricter conditions:

1. replace global normal-offset search with per-surface or tangent-space normal-map optimization,
2. improve synthetic reflection realism through Blender/Cycles or a more explicit near-object analytic reflection scene,
3. preserve all baselines from the MVP,
4. re-run go/no-go with evidence beyond simple mask exclusion.

