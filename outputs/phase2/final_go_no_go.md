# Final Go / No-Go

## Recommendation

**GO AFTER REVISION**

Do not proceed with the full RefTex-GS system. Proceed only with the reduced hypothesis:

"Reflection-induced multi-view motion can supervise reflective-region normals and prevent specular leakage during UV texture recovery."

## Basis

Novelty: **moderate after reduction, weak before reduction**. Mesh+GS+UV+PBR+near-field reflection is not a clean novelty claim because nearby work already covers most components.

Feasibility: **reasonable for the reduced MVP**. A feature-space reflection-cycle loss can be tested on synthetic data without implementing a learned reflection field.

Implementation cost: **two-week MVP is plausible** if PGSR/2DGS integration is optional and perturbed ground-truth mesh is allowed for the first signal test.

Evaluation clarity: **good for synthetic normal and texture leakage metrics**. Weak for real-data PBR claims, so those should be deferred.

Top-conference story strength: **conditional**. The story is strong only if the paper is about a new supervision signal for reflective reconstruction, not about a broad asset system.

## Exact First Implementation Milestone

Milestone 1:

Build one synthetic Blender/Cycles scene with a glossy curved object and nearby colored reflected objects. Render 40 calibrated views with ground-truth mesh, normals, albedo, roughness, and reflective mask. Implement feature-space reflection-cycle loss on a perturbed ground-truth mesh and verify:

1. the loss is lower for ground-truth normals than for 5 degree and 10 degree perturbed normals,
2. optimizing normals with the loss reduces reflective-region normal angular error,
3. UV texture baking with reflection-gated supervision reduces specular leakage versus all-pixel baking and mask-only baking.

Decision after Milestone 1:

- Continue if all three tests pass.
- Pivot if the loss is not correlated with normal correctness.
- Stop if mask-only baking matches the proposed method and normal error does not improve.

## Narrower Alternative if Pivoting

If the reflection-cycle loss fails, pivot to:

"A diagnostic benchmark and leakage metric for reflective Gaussian mesh and texture reconstruction."

This alternative is less ambitious but still useful: it would quantify where 2DGS, PGSR, SuGaR, GS-IR, GeoSplatting, MaterialRefGS, TextureSplat, SpecTRe-GS, and Ref-DGS fail on reflective-region normals and baked texture maps. It could support a workshop paper or become the evaluation backbone for a later method.
