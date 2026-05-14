# Research Gap Analysis

## Pain Point 1: Reflection-contaminated photometric geometry

What it is: RGB photometric loss treats a reflected highlight or reflected object as color attached to a surface sample, although its image motion follows reflection geometry rather than material texture.

Why it matters: Mesh reconstruction from 3DGS, 2DGS, opacity fields, or stereo fusion depends on consistent cross-view evidence. Mirror-like and glossy objects break this assumption because the observed color changes with view and with reflected scene structure.

Attempts: 2DGS, PGSR, SuGaR, GS2Mesh, Geometry Field Splatting, GS-2DGS, SSR-GS, SpecTRe-GS, Ref-DGS, PolGS.

Why insufficient: surface-GS methods improve surface support but do not explain reflection transport; stereo methods inherit brightness-constancy failures; reflection-aware methods often improve rendering or geometry but do not bake an editable UV/PBR mesh.

Limitation type: representational and optimization-related.

Potential remedy: a surface-bound representation with an explicit residual reflection field, plus a loss that constrains reflection motion using predicted normals and local reflected geometry.

Evidence: [MY SYNTHESIS | Evidence: 2DGS, SuGaR, GS2Mesh, SpecTRe-GS, Ref-DGS, PolGS].

## Pain Point 2: No stable normal signal in mirror-like regions

What it is: Normals are both the output needed for mesh/material mapping and the variable that determines reflection direction.

Why it matters: In PBR rendering, small normal errors cause large changes in reflected radiance for low roughness materials. Therefore RGB gradients in mirror-like regions are poorly conditioned.

Attempts: GS-IR uses depth-derived normals; GaussianShader uses shortest-axis normals; 2DGS/PGSR use depth-normal consistency; GeoSplatting uses mesh normals; PolGS uses polarization; NeRSP uses polarized sparse views.

Why insufficient: shortest-axis normals are unreliable when Gaussians are not true surface elements; mesh normals help only after mesh quality is adequate; polarization helps but requires specialized hardware.

Limitation type: theoretical and optimization-related.

Potential remedy: combine surface-bound Gaussians, mesh-normal refinement, and a reflection-consistency objective that supervises normals by checking where reflected rays land in a learned reflection field or proxy scene.

Evidence: [AUTHOR CLAIM | Paper: GS-IR, Sec. 3.2]: missing normals are a core inverse-rendering issue. [MY SYNTHESIS | Evidence: GS-IR, GaussianShader, GeoSplatting, PolGS].

## Pain Point 3: Far-field lighting assumptions ignore near-field reflected objects

What it is: Many inverse-rendering methods represent incoming illumination as an environment map. Near-field reflected objects do not obey a direction-only far-field model because their appearance changes with reflector position.

Why it matters: Highly reflective desktop objects, metal tools, phones, and household items often reflect nearby cameras, hands, lights, and adjacent objects. A far-field environment map can fit images but cannot explain correct parallax or produce stable material maps.

Attempts: Neural Point Catacaustics, MirrorGaussian, Reflective Gaussian Splatting, IRGS, SpecTRe-GS, Ref-DGS, RT-GS.

Why insufficient: mirror-specific methods assume planar mirrors; catacaustic methods are NVS-focused and need annotation; recent GS methods model local reflection for rendering but not UV-baked material assets.

Limitation type: representational and evaluation-related.

Potential remedy: a decomposed appearance model with a low-dimensional far-field environment plus a surface-aware near-field reflection atlas/field tied to reflected-ray intersections.

Evidence: [MY SYNTHESIS | Evidence: Neural Point Catacaustics, SpecTRe-GS, Ref-DGS, Reflective Gaussian Splatting].

## Pain Point 4: Material maps are not tied to a final mesh/UV domain

What it is: Many GS inverse-rendering methods optimize material attributes per Gaussian or in neural fields. Downstream graphics workflows require UV albedo, roughness, metallic/specular, and normal maps on a triangle mesh.

Why it matters: Texture/material mapping is part of the requested problem, not an optional export. Per-Gaussian material cannot be directly edited in standard DCC/game pipelines.

Attempts: GS-IR, GeoSplatting, SVG-IR, GS-2M, nvdiffrec, TexGaussian, NeRD.

Why insufficient: GS inverse-rendering methods rarely bake UV maps; nvdiffrec/TexGaussian have asset outputs but do not solve reflective GS reconstruction and near-field reflection ambiguity from capture images.

Limitation type: representational and pipeline-related.

Potential remedy: optimize surface-bound Gaussians for differentiable rendering, but maintain a live mesh+UV texture domain and enforce Gaussian-to-UV material consistency during training and baking.

Evidence: [AUTHOR CLAIM | Paper: nvdiffrec project]: mesh plus 2D textures are the target output. [MY SYNTHESIS | Evidence: GS-IR, SVG-IR, TexGaussian, GS-2M].

## Pain Point 5: Existing benchmarks under-test reflective-region reconstruction

What it is: Standard metrics report whole-image PSNR/SSIM/LPIPS or global Chamfer, often dominated by diffuse regions.

Why it matters: A method can improve average rendering while still failing where reflection dominates the geometry/material ambiguity.

Attempts: Stanford-ORB and OpenIllumination provide stronger inverse-rendering evaluation; PolGS/NeRSP provide specialized reflective setups; reflective GS papers use method-specific datasets.

Why insufficient: few benchmarks isolate mirror-like, glossy, near-field reflection, inter-reflection, UV texture quality, and relighting consistency in the same protocol.

Limitation type: evaluation-related.

Potential remedy: reflective-region masks, normal error in low-roughness regions, UV seam/temporal consistency, relighting under held-out local probes, and geometry metrics separated by reflective/diffuse material labels.

Evidence: [MY SYNTHESIS | Evidence: Stanford-ORB, OpenIllumination, Reflective Gaussian Splatting, PolGS].
