# Technical Review

## Local Paper Inventory

I inspected 31 local PDFs in `papers/`. The local set covers: surface reconstruction from Gaussian Splatting (2DGS, SuGaR, PGSR, GOF, SOF, 3DGSR, GS2Mesh, DN-Splatter, MILo, MGSR, geometry-field surfels), reflective/specular Gaussian Splatting (Reflective Gaussian Splatting, RefGaussian, Ref-GS, MaterialRefGS, PolGS, PolGS++, SSR-GS, SpecTRe-GS, GS-2DGS, IRGS, EnvGS, GlossyGS), inverse rendering/material routes (GeoSplatting, GS-2M, SSD-GS), and classical reflection theory (Specular Flow, Shape from Specular Flow, Neural Point Catacaustics, Deep Flow Rendering). Extracted abstracts and term-level snippets are cached at `outputs/_work/local_pdf_extracts.json`; the per-PDF inventory is in `outputs/local_paper_inventory.md`.

## Taxonomy

### 1. Appearance-centric 3DGS for view-dependent effects

[AUTHOR CLAIM | Paper: 3D Gaussian Splatting, Sec. 3]: 3DGS represents scenes with anisotropic Gaussians and spherical-harmonic view-dependent color, optimized by differentiable rasterization.

[MY SYNTHESIS | Evidence: 3D Gaussian Splatting, Spec-Gaussian, EnvGS, Ref-GS]: Appearance-centric methods improve novel-view rendering by increasing the expressiveness of view-dependent color, directional factors, or environment-conditioned appearance.

[MY INFERENCE | Based on: Spec-Gaussian abstract and EnvGS local PDF]: These methods can render specular highlights more faithfully because the appearance basis can vary strongly with view direction. They do not force the highlight to be explained by a surface normal, BRDF roughness, or a reflected environment; therefore the same image evidence can be explained by wrong geometry plus a flexible appearance field.

Failure mode for the target problem: mesh reconstruction and UV/PBR material baking require view-independent geometry and surface-bound material. Appearance-centric splats can reproduce images while storing reflections as view-dependent color, so the exported mesh and texture are not physically meaningful.

### 2. Surface Gaussian and mesh-extraction methods

[AUTHOR CLAIM | Paper: 2D Gaussian Splatting, Sec. 3]: Replacing volumetric 3D ellipsoids with oriented 2D disks makes Gaussian primitives more surface-like and permits depth and normal consistency losses.

[AUTHOR CLAIM | Paper: SuGaR, Sec. 3 / Fig. 2]: Surface-aligned Gaussian regularization allows efficient mesh extraction from 3DGS.

[AUTHOR CLAIM | Paper: GS2Mesh, Abstract]: Rendering stereo views from a trained 3DGS and fusing stereo depth can recover a mesh without relying directly on noisy Gaussian centers.

[MY SYNTHESIS | Evidence: 2DGS, SuGaR, PGSR, GOF, SOF, MILo, Geometry Field Splatting]: This route succeeds when multiview photometric consistency is mostly Lambertian or mildly view-dependent, because depth/normal/alignment losses make the optimized primitive support coincide with the real surface.

[MY INFERENCE | Based on: 2DGS losses, GS2Mesh stereo assumption, SuGaR surface alignment]: For highly reflective objects, the same surface point may show unrelated reflected content across views. Photometric gradients then pull disks or opacity toward reflected objects, not only toward the reflector surface. Stereo-based extraction is also vulnerable because specular reflection breaks brightness constancy.

Failure mode for the target problem: these methods often output meshes, but not UV texture maps or PBR material maps. They do not explain near-field reflected content, inter-reflection, or mirror-like appearance as light transport.

### 3. SDF-Gaussian and mesh-guided hybrids

[AUTHOR CLAIM | Paper: 3DGSR, Sec. 3]: A neural SDF can be jointly optimized with 3DGS by converting SDF values to opacity and enforcing depth/normal consistency.

[AUTHOR CLAIM | Paper: GeoSplatting, Abstract]: Mesh normals and mesh-based ray tracing can improve physically based inverse rendering because raw Gaussian normals and occlusion are unreliable.

[AUTHOR CLAIM | Paper: GS-ROR2, Abstract]: Bidirectional 3DGS-SDF guidance improves reflective-object relighting and reconstruction at additional training cost.

[MY SYNTHESIS | Evidence: 3DGSR, GeoSplatting, GS-ROR2, MILo]: Hybrids succeed because the implicit or explicit surface supplies coherent normals and visibility, while Gaussians preserve efficient differentiable image formation.

[MY INFERENCE | Based on: GeoSplatting and GS-ROR2 assumptions]: If the mesh/SDF is initialized from reflection-contaminated images, the hybrid can stabilize the wrong geometry. Mesh guidance improves normals only after the surface is already close enough for reflection constraints to be meaningful.

Failure mode for the target problem: hybrids address mesh and inverse rendering separately, but few provide a surface-bound representation that simultaneously models near-field reflected radiance, outputs UV PBR maps, and remains editable after Gaussian optimization.

### 4. Gaussian Splatting inverse rendering and relighting

[AUTHOR CLAIM | Paper: GS-IR, Sec. 3.2-3.3]: GS-IR adds normal regularization and baked occlusion so 3DGS can estimate material and environment illumination for physically based rendering.

[AUTHOR CLAIM | Paper: SVG-IR, Abstract]: Spatially varying Gaussian parameters address the limitation of assigning constant normal/material values to an entire Gaussian.

[AUTHOR CLAIM | Paper: Relightable 3D Gaussians, ECCV abstract]: Point-based ray tracing estimates visibility for BRDF decomposition and relighting.

[MY SYNTHESIS | Evidence: GS-IR, GUS-IR, GIR, SVG-IR, RTR-GS, Relightable 3D Gaussians]: Inverse-rendering GS methods succeed when geometry normals are reliable and reflected illumination can be approximated as environment lighting plus visibility/occlusion.

[MY INFERENCE | Based on: GS-IR normal approximation and GeoSplatting critique]: Highly reflective objects are a worst case because material, normal, and lighting are coupled. A wrong normal can be compensated by a different environment map or roughness, and the RGB loss alone may not distinguish these explanations.

Failure mode for the target problem: current methods usually store material per Gaussian or in neural fields, not as UV texture maps on a clean mesh. They usually approximate far-field illumination; near-field reflected objects and inter-reflections need explicit geometric consistency.

### 5. Reflective, mirror, near-field, and inter-reflection methods

[AUTHOR CLAIM | Paper: MirrorGaussian, Sec. 3]: Planar mirror scenes can be modeled by rendering real Gaussians and their reflected virtual counterparts.

[AUTHOR CLAIM | Paper: Neural Point Catacaustics, Sec. 3]: Reflection flow and catacaustic geometry can model curved-reflector view synthesis.

[AUTHOR CLAIM | Paper: Reflective Gaussian Splatting, Abstract]: A material-aware deferred renderer with Gaussian-grounded inter-reflection targets reflective-object rendering, relighting, and editing.

[AUTHOR CLAIM | Paper: PolGS, Abstract]: Polarization provides physical cues for fast reflective surface reconstruction.

[MY SYNTHESIS | Evidence: MirrorGaussian, Neural Point Catacaustics, Reflective Gaussian Splatting, IRGS, SpecTRe-GS, Ref-DGS, SSR-GS, PolGS]: Reflection-aware methods introduce extra signals: mirror symmetry, reflection rays, inter-reflection tracing, local reflection fields, or polarization. These are exactly the kinds of constraints missing from pure photometric surface reconstruction.

[MY INFERENCE | Based on: comparison of outputs in the literature matrix]: Most of these methods optimize rendering quality or geometry, but stop short of producing a clean mesh with baked UV albedo/roughness/metallic/normal maps. Conversely, asset-oriented inverse-rendering methods such as nvdiffrec output UV/PBR maps but do not model 3DGS near-field reflection ambiguity.

### 6. Asset-oriented mesh and UV/PBR methods

[AUTHOR CLAIM | Paper: nvdiffrec, CVPR project]: nvdiffrec optimizes triangle mesh, spatially varying 2D textures, and HDR environment lighting using differentiable rasterization.

[AUTHOR CLAIM | Paper: TexGaussian, Project page]: TexGaussian uses octree-aligned Gaussians and bakes PBR material to UV space.

[MY SYNTHESIS | Evidence: nvdiffrec, TexGaussian, NeRD, PhySG, NeRFactor]: Asset-oriented methods define the desired output format more clearly than most GS methods: triangle mesh plus texture-space material maps.

[MY INFERENCE | Based on: nvdiffrec assumptions and reflective GS papers]: These methods are not sufficient for highly reflective objects because their rendering models typically assume environment illumination and do not introduce a reflection-field or near-field correspondence constraint strong enough to disambiguate reflected objects from reflector geometry.
