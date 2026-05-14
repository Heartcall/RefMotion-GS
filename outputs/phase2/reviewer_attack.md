# Reviewer Attack

## 1. The method is component stacking

Why serious: The full proposal includes mesh, 2DGS, UV PBR, reflective gates, environment lighting, near-field fields, inter-reflection, UV baking, relighting, and editing. This reads like many known modules assembled.

Evidence needed: A reduced method with one central mechanism and ablations showing that mechanism is necessary.

Required experiment: reflection-motion loss only versus PGSR/2DGS, mask-only baking, and UV baking baselines.

Current plan answers it: Partly after Phase 2 reduction, not in Phase 1.

## 2. Novelty overlaps with SpecTRe-GS and Ref-DGS

Why serious: SpecTRe-GS already traces reflected rays for nearby reflected objects. Ref-DGS already uses local reflection Gaussians plus global environment reflection.

Evidence needed: Show that the paper is not about near-field reflection rendering, but about using reflection-induced motion as supervision for normals and texture routing.

Required experiment: normal and UV leakage metrics, not only novel-view PSNR.

Current plan answers it: Only if near-field F_nf is removed from the first paper.

## 3. Novelty overlaps with MaterialRefGS

Why serious: MaterialRefGS already uses multi-view material consistency and a reflection-strength prior based on photometric variation along camera trajectories.

Evidence needed: Compare against MaterialRefGS and show that reflected-ray geometry gives better normal/texture supervision than photometric variation alone.

Required experiment: reflective mask/gate quality, roughness or reflection-strength estimation, normal error, texture leakage.

Current plan answers it: Not yet. Must include MaterialRefGS in baselines or analysis.

## 4. Texture mapping novelty is weakened by TextureSplat

Why serious: TextureSplat already introduces per-primitive texture maps for material and normal properties in 2DGS-based PBR rendering for highly reflective scenes.

Evidence needed: Remove "texture maps on Gaussians" from the novelty claim. Show the contribution is the reflection-motion supervision signal.

Required experiment: compare against per-primitive texture mapping without reflection-motion loss.

Current plan answers it: Partly. The MVP should include a texture-only baseline.

## 5. Learned reflection fields can absorb all errors

Why serious: A high-capacity F_nf can fit arbitrary view-dependent color, leaving geometry and UV material wrong.

Evidence needed: Either remove F_nf or provide low-capacity constraints and held-out diagnostics.

Required experiment: normal perturbation test, held-out reflected-object position test, F_nf capacity ablation.

Current plan answers it: Yes only if F_nf is not in the first implementation.

## 6. The reflection-consistency loss was underdefined

Why serious: Without precise definitions of x, reflected point, p'_j, correspondences, and gradient paths, the theory is not reproducible.

Evidence needed: A rigorous formulation with stop-gradient choices and variables.

Required experiment: controlled synthetic test showing the loss minimum aligns with ground-truth normals.

Current plan answers it: Phase 2 theory rewrite addresses it conceptually. Implementation still required.

## 7. Real-data evaluation lacks ground truth

Why serious: Reflective object normals, albedo, roughness, and UV texture quality are difficult to measure on real captures.

Evidence needed: synthetic ground truth plus controlled real benchmarks with proxies, not unsupported real-only claims.

Required experiment: Blender/Cycles ground truth, Stanford-ORB/OpenIllumination where applicable, and real qualitative cases clearly labeled.

Current plan answers it: Yes for MVP if synthetic comes first.

## 8. UV/PBR evaluation may be ill-posed

Why serious: Many texture maps can render the same training views. Without ground-truth material, claimed material quality is weak.

Evidence needed: focus on diffuse albedo leakage and normal accuracy first; defer full PBR claims.

Required experiment: specular leakage metric and albedo RMSE on synthetic scenes.

Current plan answers it: Yes if full PBR is deferred.

## 9. Relighting and editing claims are overclaimed

Why serious: If near-field reflected content is captured in a residual field, relighting/editing may not be physically correct.

Evidence needed: remove relighting/editing from first-paper claims or evaluate with held-out lights and edited local reflectors.

Required experiment: optional sanity relighting only, not headline.

Current plan answers it: Yes after reduction, no in Phase 1.

## 10. The proposed signal may be unnecessary

Why serious: Masking out reflective pixels during texture baking may already prevent specular leakage; monocular normals or polarization may solve normal errors more directly.

Evidence needed: show improvement over mask-only, monocular normal prior, and ground-truth reflective-mask baking baselines.

Required experiment: mask-only bake, oracle mask bake, monocular normal prior, proposed reflection-cycle loss.

Current plan answers it: Partly. The MVP includes mask-only, but must add oracle-mask and normal-prior baselines.

## Bottom Line From Hostile Review

I would reject the full Phase 1 paper for lack of focus. I might support the reduced paper if it proves, with clean synthetic evidence and strong ablations, that reflection-induced motion is a useful normal and texture-supervision signal not captured by MaterialRefGS, SpecTRe-GS, Ref-DGS, TextureSplat, or mask-only baking.
