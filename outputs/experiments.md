# Experiments

## Datasets

Synthetic: Blender/Cycles scenes with chrome, brushed metal, glossy ceramic, black plastic, planar mirrors, curved mirrors, and nearby colored objects. Render ground-truth mesh, normals, albedo, roughness, metallic/specular, HDR lighting, reflection-region masks, and inter-reflection masks.

Real controlled: Stanford-ORB and OpenIllumination for relighting/material evaluation; add a small captured set with turntable objects, chrome spheres, metal utensils, phone backs, watch cases, and glossy ceramic objects. Capture HDR environment probes and optional cross-polarized references for analysis.

Real in-the-wild: reflective tabletop objects with COLMAP poses and masks, used for qualitative stress tests under uncontrolled backgrounds, imperfect masks, and calibration noise.

## Baselines

Surface/mesh: 3DGS, 2DGS, SuGaR, PGSR, GS2Mesh, GOF, Geometry Field Splatting, MILo.

Inverse rendering/relighting: nvdiffrec, PhySG, NeRO, GS-IR, GUS-IR, GIR, SVG-IR, GeoSplatting, Relightable 3D Gaussians, GS-2M.

Reflective-specific: GaussianShader, Reflective Gaussian Splatting, PolGS when polarization is available, GS-ROR2, SSR-GS, SpecTRe-GS, Ref-DGS, MirrorGaussian for planar-mirror scenes.

## Metrics

Mesh quality: Chamfer-L1, F-score at multiple thresholds, normal consistency, edge Chamfer for sharp reflective silhouettes.

Normal quality: mean/median angular error overall and separately in low-roughness reflective regions.

Material quality: albedo RMSE/SSIM, roughness MAE, metallic/specular classification accuracy, scale-invariant albedo error.

UV texture quality: held-out UV reprojection error, seam inconsistency, specular-leakage score measured by correlation between baked albedo and view-dependent residual.

Relighting: PSNR/SSIM/LPIPS under held-out environment maps and held-out local near-field probes.

Reflective-region reconstruction: metrics restricted to reflective masks; reflected-object parallax error; inter-reflection residual error on synthetic scenes.

Runtime/memory: training time, peak VRAM, primitive count, mesh vertex/face count, rendering FPS, UV atlas resolution.

## Ablations

Without reflection-consistency loss: tests whether normals and reflective geometry degrade.

Without near-field reflection field: tests far-field-only failure on local reflected objects.

Without inter-reflection residual: tests multi-bounce and concave metal/glossy cases.

Without reflective-region reasoning: tests whether specular content leaks into albedo/UV maps.

Free 3D Gaussians vs surface-bound Gaussians: tests floating reflection artifacts and mesh quality.

RGB loss vs feature-space/reflection-aware loss: tests sensitivity to high-frequency reflected texture.

With and without external priors: monocular normals/depth/VGGT/polarization when available.

Without UV consistency and seam loss: tests texture-map usability.

## Failure-case Analysis

Report failures for moving reflected objects, transparent coatings, extremely sparse views, black mirror surfaces with little diffuse signal, inaccurate masks, calibration errors, and concave objects with strong multi-bounce reflections.
