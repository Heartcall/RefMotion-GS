# Novelty Audit

## Audit Position

Verdict on the full Phase 1 RefTex-GS proposal: **over-combined as written**.

The defensible part is narrower: use reflection-induced motion or reflected-ray correspondence to decide whether a multi-view observation should supervise surface texture, surface normal, or reflected radiance. The mesh+UV+PBR+near-field+inter-reflection package is not one clean contribution. Several pieces are already present in nearby work:

- Surface-like Gaussian primitives: 2DGS, PGSR, SuGaR, MILo.
- Mesh or mesh-guided GS: SuGaR, PGSR, MILo, GeoSplatting, GS-2M.
- PBR/inverse-rendering GS: GS-IR, GeoSplatting, MaterialRefGS, SVG-IR, RTR-GS.
- Near-field or ray-traced reflection: SpecTRe-GS, Ref-DGS, IRGS.
- Texture maps on reflective Gaussian primitives: TextureSplat is an extra overlap risk beyond the requested list.

Sources used: Phase 1 files, local PDFs, [MaterialRefGS project](https://wen-yuan-zhang.github.io/MaterialRefGS/), [SpecTRe-GS project](https://spectre-gs.github.io/), [TextureSplat OpenReview PDF](https://openreview.net/pdf?id=aRMIlILPm9), [Ref-DGS arXiv](https://arxiv.org/abs/2603.07664), [nvdiffrec project](https://nvlabs.github.io/nvdiffrec/), [SuGaR CVPR](https://openaccess.thecvf.com/content/CVPR2024/papers/Guedon_SuGaR_Surface-Aligned_Gaussian_Splatting_for_Efficient_3D_Mesh_Reconstruction_and_CVPR_2024_paper.pdf), and [2DGS arXiv](https://arxiv.org/abs/2403.17888).

## Verdict Table

### GS-IR

A. It estimates geometry, material, illumination, normals, and occlusion for inverse rendering with 3DGS.

B. Surface-bound Gaussians: No. It is still free 3DGS with normal/occlusion regularization.

C. Mesh extraction: No primary mesh output.

D. UV-domain material maps: No. Material is associated with Gaussian/inverse-rendering attributes.

E. Near-field reflection: No. It relies on environment/occlusion approximations.

F. Inter-reflection: Approximate indirect/occlusion, not explicit near-field inter-reflection.

G. Reflection motion / reflected-ray correspondence: No.

H. Observation routing between texture and reflected radiance: No explicit gate.

I. Remaining RefTex-GS difference: reflection-motion supervision plus UV texture supervision on a mesh.

J. Strength: **PARTIALLY NOVEL** if the paper is about reflection-motion supervision. Weak if framed as general GS inverse rendering.

### GeoSplatting

A. It uses geometry-guided GS and mesh normals for physically based inverse rendering and occlusion-aware light transport.

B. Surface-bound Gaussians: Partly. It is mesh-grounded, but not the same as a UV-first surface-bound texture formulation.

C. Mesh extraction: Yes, mesh-guided geometry is central.

D. UV-domain material maps: No clear UV-map output in the Phase 1 matrix.

E. Near-field reflection: No explicit local reflected-object model; it focuses on mesh normals and occlusion-aware transport.

F. Inter-reflection: Partial indirect/occlusion, not explicit multi-bounce reflective-object modeling.

G. Reflection motion / reflected-ray correspondence: No clear evidence.

H. Observation routing: No explicit texture-versus-reflection gate.

I. Remaining RefTex-GS difference: the proposed normal/texture supervision from reflection-induced motion.

J. Strength: **PARTIALLY NOVEL**. The mesh+inverse-rendering part overlaps heavily.

### Reflective Gaussian Splatting / RefGaussian

A. Reflective Gaussian Splatting uses 2D Gaussian primitives, material-aware deferred PBR, split-sum rendering, and Gaussian-grounded inter-reflection. RefGaussian/related works disentangle reflections from 3DGS for realistic rendering.

B. Surface-bound Gaussians: Reflective GS uses 2DGS-like surface primitives. RefGaussian is more appearance/disentanglement oriented.

C. Mesh extraction: Surface/geometry may be possible, but a clean mesh+UV asset is not the central output.

D. UV-domain material maps: No evidence of mesh UV PBR texture maps.

E. Near-field reflection: Partial. Reflective GS models inter-reflection; near-field handling depends on its Gaussian-grounded reflection formulation.

F. Inter-reflection: Yes for Reflective GS.

G. Reflection motion / reflected-ray correspondence: Not as a stated normal/texture-supervision signal in the Phase 1 evidence.

H. Observation routing: Material/reflection decomposition exists, but not clearly a hard supervision decision for UV texture versus reflection field.

I. Remaining RefTex-GS difference: UV texture supervision and using reflected motion as a disambiguating training signal.

J. Strength: **PARTIALLY NOVEL**. Strong overlap on reflective rendering; defend only the supervision signal and UV texture leakage metric.

### GS-2M

A. It targets joint mesh reconstruction and material decomposition with Gaussian Splatting.

B. Surface-bound Gaussians: Unclear from available evidence; it is material-aware GS with mesh reconstruction.

C. Mesh extraction: Yes.

D. UV-domain material maps: Unclear. Phase 1 evidence lists material attributes/maps but not confirmed UV-domain atlas output.

E. Near-field reflection: No explicit evidence.

F. Inter-reflection: No explicit evidence.

G. Reflection motion / reflected-ray correspondence: No evidence.

H. Observation routing: No evidence of an explicit reflective observation gate.

I. Remaining RefTex-GS difference: reflection-motion supervision in reflective regions.

J. Strength: **UNCERTAIN, NEEDS MORE SEARCH**. If GS-2M has UV material maps, RefTex-GS loses much of its asset-output novelty.

### SpecTRe-GS

A. It models highly specular surfaces reflecting nearby objects by tracing reflected rays in 3DGS. The project page states it separates highly specular and rough reflections, uses efficient ray tracing for secondary rays, and enhances geometry with normal prior guidance and numerical gradients from ray-traced incident radiance.

B. Surface-bound Gaussians: No. It uses a Gaussian point cloud with depth/normal/shading attributes.

C. Mesh extraction: Not central.

D. UV-domain material maps: No.

E. Near-field reflection: Yes. This is its main target.

F. Inter-reflection: Yes, for highly specular inter-reflections.

G. Reflection motion / reflected-ray correspondence: It uses reflected rays and incident radiance gradients for geometry, but not clearly a multi-view reflection-flow correspondence used to supervise UV texture versus reflection.

H. Observation routing: It separates rough and specular rendering paths, but not a UV texture supervision gate.

I. Remaining RefTex-GS difference: texture-leakage prevention and UV-domain supervision, not near-field reflection itself.

J. Strength: **WEAK NOVELTY** for near-field reflection. **PARTIALLY NOVEL** only if narrowed to reflection-motion-gated UV baking.

### Ref-DGS

A. It introduces geometry Gaussians plus local reflection Gaussians for near-field specular interactions, and a global environment reflection field for far-field specular reflection.

B. Surface-bound Gaussians: It has geometry Gaussians, but the local reflection Gaussians are not a mesh-UV material representation.

C. Mesh extraction: Surface reconstruction is reported, but mesh/UV output is not the main evidence.

D. UV-domain material maps: No.

E. Near-field reflection: Yes.

F. Inter-reflection: No full multi-bounce claim from the Phase 1 evidence.

G. Reflection motion / reflected-ray correspondence: No evidence of using cross-view reflection flow as direct supervision.

H. Observation routing: It separates geometry and local reflection representations, but not explicitly texture-supervision routing.

I. Remaining RefTex-GS difference: the training signal, not the near-field reflection representation.

J. Strength: **WEAK NOVELTY** if RefTex-GS claims local reflection fields. **PARTIALLY NOVEL** if the paper proves reflection-motion supervision improves normals and texture baking.

### MaterialRefGS

A. It performs reflective GS with multi-view material consistency and a reflection strength prior. The project page says it enforces consistency across projected multi-view material maps and uses photometric variation along camera trajectories as an explicit target for reflection strength.

B. Surface-bound Gaussians: Not clearly surface-bound in a mesh/UV sense.

C. Mesh extraction: Not primary.

D. UV-domain material maps: It discusses material maps from views/Gaussians, but not final mesh UV atlases.

E. Near-field reflection: Not clearly explicit.

F. Inter-reflection: Limited or not central.

G. Reflection motion / reflected-ray correspondence: It uses multi-view photometric variation and warping for reflection strength, but not a physically reflected-ray correspondence.

H. Observation routing: Close. Reflection-strength prior affects material inference and identifies reflective behavior.

I. Remaining RefTex-GS difference: physically defined reflection-direction correspondence and UV texture leakage prevention.

J. Strength: **PARTIALLY NOVEL TO WEAK NOVELTY**. This is a serious overlap for reflection-aware material consistency.

### IRGS

A. It models inter-reflective Gaussian Splatting with 2D Gaussian ray tracing.

B. Surface-bound Gaussians: Yes, via 2DGS-like primitives.

C. Mesh extraction: Possibly, but not the central asset output.

D. UV-domain material maps: No evidence.

E. Near-field reflection: Yes if traced paths include local surfaces.

F. Inter-reflection: Yes.

G. Reflection motion / reflected-ray correspondence: It uses ray tracing, but no evidence that multi-view reflection flow is used to supervise UV texture.

H. Observation routing: Material/reflection decomposition likely exists, but not UV-supervision routing.

I. Remaining RefTex-GS difference: UV texture disambiguation and a minimal reflection-motion normal loss.

J. Strength: **WEAK NOVELTY** for reflection transport; **PARTIALLY NOVEL** for texture-supervision routing.

### PolGS / PolGS++

A. They use polarization to reconstruct reflective surfaces with 3DGS.

B. Surface-bound Gaussians: Not necessarily. They are 3DGS plus polarimetric constraints.

C. Mesh extraction: Surface/depth likely, but not UV asset central.

D. UV-domain material maps: No.

E. Near-field reflection: No.

F. Inter-reflection: No.

G. Reflection motion / reflected-ray correspondence: No. They use polarization physics.

H. Observation routing: They separate reflective cues physically, but not texture-versus-reflection supervision in RGB.

I. Remaining RefTex-GS difference: RGB-only reflection-motion supervision and UV texture outcome.

J. Strength: **CLEARLY NOVEL** relative to PolGS only if the setting is RGB-only. If polarization is allowed, PolGS may be more physically defensible.

### nvdiffrec

A. It optimizes triangle mesh, PBR textures, and environment lighting from posed images using differentiable rasterization.

B. Surface-bound Gaussians: No.

C. Mesh extraction: Yes, central.

D. UV-domain material maps: Yes.

E. Near-field reflection: No explicit local reflected-object model.

F. Inter-reflection: No.

G. Reflection motion / reflected-ray correspondence: No.

H. Observation routing: No explicit reflective observation gate.

I. Remaining RefTex-GS difference: reflection-motion disambiguation for reflective objects and Gaussian initialization/efficiency.

J. Strength: **PARTIALLY NOVEL**. Asset output overlaps; reflective supervision is the difference.

### TexGaussian

A. It generates or reconstructs PBR material via octree-based 3DGS and bakes multiview renders to UV space on an input mesh.

B. Surface-bound Gaussians: Yes, aligned to an input mesh.

C. Mesh extraction: Input mesh, not reconstructed.

D. UV-domain material maps: Yes.

E. Near-field reflection: No inverse-capture near-field model.

F. Inter-reflection: No.

G. Reflection motion / reflected-ray correspondence: No.

H. Observation routing: No reflective capture supervision gate.

I. Remaining RefTex-GS difference: reconstruction from reflective images and reflection-motion signal.

J. Strength: **PARTIALLY NOVEL**. UV/PBR output is not novel by itself.

### SuGaR

A. It extracts meshes from surface-aligned 3DGS and supports mesh-bound Gaussian rendering/editing.

B. Surface-bound Gaussians: Yes, surface-aligned/bound in refinement.

C. Mesh extraction: Yes, central.

D. UV-domain material maps: No.

E. Near-field reflection: No.

F. Inter-reflection: No.

G. Reflection motion / reflected-ray correspondence: No.

H. Observation routing: No.

I. Remaining RefTex-GS difference: reflective normal/texture supervision and UV material output.

J. Strength: **PARTIALLY NOVEL**. Mesh-bound Gaussians are not enough.

### 2DGS

A. It replaces volumetric Gaussians with oriented 2D disks, improves geometry, and supports depth/normal consistency.

B. Surface-bound Gaussians: Yes, surface-like 2D disks.

C. Mesh extraction: Yes, via depth fusion.

D. UV-domain material maps: No.

E. Near-field reflection: No.

F. Inter-reflection: No.

G. Reflection motion / reflected-ray correspondence: No.

H. Observation routing: No.

I. Remaining RefTex-GS difference: reflection-motion supervision and texture-leakage prevention.

J. Strength: **PARTIALLY NOVEL**. The primitive is not novel.

### PGSR

A. It uses planar Gaussian splats, unbiased depth/normal maps, and geometric regularization for surface reconstruction.

B. Surface-bound Gaussians: Yes, planar surface-oriented Gaussians.

C. Mesh extraction: Yes.

D. UV-domain material maps: No.

E. Near-field reflection: No.

F. Inter-reflection: No.

G. Reflection motion / reflected-ray correspondence: No.

H. Observation routing: No.

I. Remaining RefTex-GS difference: reflective-region supervision and UV texture recovery.

J. Strength: **PARTIALLY NOVEL**. PGSR is a likely MVP initialization, not a novelty baseline to claim over broadly.

### MILo

A. It puts mesh extraction inside the GS training loop, producing a lightweight mesh during optimization.

B. Surface-bound Gaussians: Mesh-in-the-loop coupling, but not necessarily UV-material surface-bound Gaussians.

C. Mesh extraction: Yes, central.

D. UV-domain material maps: No.

E. Near-field reflection: No.

F. Inter-reflection: No.

G. Reflection motion / reflected-ray correspondence: No.

H. Observation routing: No.

I. Remaining RefTex-GS difference: reflective supervision and texture disambiguation.

J. Strength: **PARTIALLY NOVEL** only for reflection-motion supervision. Mesh-in-the-loop alone is not new.

## Extra Overlap Risk: TextureSplat

TextureSplat is not in the requested audit list, but it is highly relevant. Its OpenReview PDF describes per-primitive texture maps for material properties and normals within 2DGS-based PBR rendering for highly reflective scenes, plus unified material texture atlases for hardware acceleration. This directly overlaps with the Phase 1 claim that surface-bound Gaussians plus texture/material maps are new.

Consequence: RefTex-GS should not claim novelty for "texture maps on reflective Gaussian primitives." It can only claim novelty for a specific reflection-induced motion supervision signal, if that signal is demonstrably absent from TextureSplat and MaterialRefGS.

## Conservative Overall Verdict

Full RefTex-GS: **WEAK NOVELTY / over-combined**.

Reduced RefTex-GS: **PARTIALLY NOVEL** if framed as:

"Reflection-induced motion provides a training signal for normal estimation and texture-supervision routing in reflective object mesh and UV texture recovery."

The top-tier case requires experiments showing that this signal improves reflective-region normals and reduces specular leakage into baked texture. Without that evidence, the proposal reads as component stacking.
