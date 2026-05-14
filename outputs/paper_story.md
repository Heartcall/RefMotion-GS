# Paper Story

One-sentence core message: Reflective object reconstruction needs to separate the surface that reflects from the world being reflected, and that separation should be optimized directly in the mesh and UV material domain.

## Abstract Draft

Gaussian Splatting has made high-quality view synthesis and fast surface reconstruction practical, but highly reflective objects remain difficult because RGB photometric consistency entangles surface geometry, material, and reflected scene content. We propose RefTex-GS, a mesh-bound Gaussian inverse-rendering method for reflective object reconstruction and texture/material mapping. RefTex-GS represents the object with surface-bound Gaussians attached to a live triangle mesh and UV atlas, while decomposing appearance into PBR material maps, far-field illumination, a near-field reflection field, and a compact inter-reflection residual. A reflective-region reasoning module decides which observations should supervise diffuse UV texture and which should supervise reflection transport. A multiview reflection-consistency objective constrains normals by the motion of reflected radiance, reducing texture-reflection leakage in mirror-like regions. The method outputs a clean mesh, UV albedo/roughness/metallic/normal maps, and a relightable/editable renderer. Experiments will evaluate geometry, normals, material maps, UV texture quality, relighting, and reflective-region reconstruction on synthetic and real reflective objects.

## Introduction Outline

1. 3DGS and 2DGS have improved radiance-field speed and surface reconstruction.
2. Reflective objects violate the diffuse/mild-view-dependence assumptions behind photometric geometry.
3. Existing routes solve only parts of the problem: mesh extraction without material decomposition, inverse rendering without UV mesh assets, or reflection rendering without graphics-ready material maps.
4. The key observation is that diffuse texture is fixed in UV space, while reflected radiance moves according to normal-induced reflection geometry.
5. RefTex-GS uses this distinction to jointly optimize surface-bound Gaussians, mesh geometry, UV PBR maps, and decomposed reflection fields.

## Motivation Figure

Show the same chrome/glossy object reconstructed by 2DGS/SuGaR, GS-IR/GeoSplatting, and RefTex-GS. Highlight three failure modes: floating reflected content in geometry, specular leakage into albedo, and relighting inconsistency when a nearby reflected object moves.

## Main Method Figure

Left: input posed images and masks. Middle: surface-bound Gaussians attached to mesh/UV, reflective-region map, far-field environment, near-field reflection field, and residual inter-reflection field. Right: final mesh, UV PBR maps, relighting, and material editing.

## Contribution Paragraph

The paper contributes a surface-bound Gaussian representation for reflective mesh and UV material recovery, a reflection-consistency objective that constrains normals through reflected-ray motion, and a reflective-region-aware texture baking strategy that reduces specular leakage into PBR maps. It also proposes an evaluation protocol that isolates reflective-region geometry, normal, material, UV, and relighting errors.

## Related Work Positioning

Against surface GS methods, the paper adds physically motivated reflection decomposition and UV/PBR outputs. Against GS inverse-rendering methods, it adds mesh-bound UV optimization and near-field reflection modeling. Against reflective GS methods, it makes graphics-ready mesh and material maps the target output rather than only novel-view rendering or relighting. Against nvdiffrec-style asset extraction, it adds Gaussian efficiency and reflection-specific constraints.

## Why Reviewers Should Care

Reflective objects are common in product digitization, robotics, AR/VR asset capture, and e-commerce. Current methods can look visually plausible while producing unusable geometry or texture maps. The proposal targets a measurable asset-quality gap.

## Potential Reviewer Criticisms

1. The method may appear to combine many components.
2. Near-field reflection fields could absorb errors like arbitrary view-dependent color.
3. UV PBR maps may be hard to evaluate on real data.
4. Concurrent reflective GS papers may overlap.

## Rebuttal Strategy

Emphasize the causal constraint: UV texture is view-stationary, reflection is normal-induced and view-dependent. Show ablations proving each component is necessary. Use synthetic ground truth plus real relighting benchmarks. Include novelty table against GS-IR, GeoSplatting, Reflective Gaussian Splatting, GS-2M, SpecTRe-GS, Ref-DGS, and nvdiffrec.
