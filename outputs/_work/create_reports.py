from __future__ import annotations

import csv
from pathlib import Path

OUT = Path("outputs")
OUT.mkdir(exist_ok=True)

COLS = [
    "Paper title",
    "Year",
    "Venue or preprint status",
    "Link",
    "Code / project page if available",
    "Core problem",
    "Input assumptions",
    "Representation used",
    "Whether it uses 3DGS / 2DGS / surface Gaussians / SDF / mesh / neural field / hybrid representation",
    "Whether it handles specular reflection",
    "Whether it handles mirror-like reflection",
    "Whether it handles near-field reflection",
    "Whether it handles inter-reflection",
    "Whether it outputs mesh",
    "Whether it outputs UV texture maps",
    "Whether it outputs PBR material maps",
    "Whether it supports relighting",
    "Whether it supports material editing",
    "Geometry supervision",
    "Normal estimation strategy",
    "Material decomposition strategy",
    "Rendering model",
    "Main loss functions",
    "Datasets",
    "Metrics",
    "Strengths",
    "Limitations explicitly stated by the authors",
    "Limitations inferred by you",
    "Key evidence: section / page / figure / equation reference",
]


def r(
    title,
    year,
    venue,
    link,
    code,
    problem,
    inputs,
    rep,
    kind,
    spec="No",
    mirror="No",
    near="No",
    inter="No",
    mesh="No",
    uv="No",
    pbr="No",
    relight="No",
    edit="No",
    geom="Photometric multiview supervision",
    normal="Not central or derived from geometry",
    mat="None",
    render="Differentiable image rendering",
    loss="RGB reconstruction plus regularization",
    datasets="Paper-specific benchmarks",
    metrics="PSNR/SSIM/LPIPS and/or geometry metrics",
    strengths="Relevant technical route for the target problem",
    author_lim="See paper limitation/discussion where available",
    infer_lim="Does not jointly solve reflective mesh reconstruction, UV texture baking, and PBR material mapping.",
    evidence="Local PDF first pages/abstract and method sections; web/project page when linked.",
):
    vals = [
        title,
        year,
        venue,
        link,
        code,
        problem,
        inputs,
        rep,
        kind,
        spec,
        mirror,
        near,
        inter,
        mesh,
        uv,
        pbr,
        relight,
        edit,
        geom,
        normal,
        mat,
        render,
        loss,
        datasets,
        metrics,
        strengths,
        author_lim,
        infer_lim,
        evidence,
    ]
    return dict(zip(COLS, vals))


rows = [
    r("2D Gaussian Splatting for Geometrically Accurate Radiance Fields", 2024, "SIGGRAPH / TOG", "https://arxiv.org/abs/2403.17888", "https://surfsplatting.github.io/", "Surface-accurate radiance fields and mesh extraction.", "Posed RGB; SfM initialization.", "Oriented 2D Gaussian disks.", "2DGS / surface Gaussians", "View-dependent color only", mesh="Yes, via depth fusion", geom="RGB plus depth distortion and normal consistency.", normal="Disk normals with depth-normal consistency.", render="Perspective-correct 2D Gaussian alpha compositing.", loss="RGB, depth distortion, normal consistency.", datasets="DTU, Tanks and Temples, Mip-NeRF360.", strengths="Turns volumetric splats into surface-like primitives.", author_lim="Motivated by 3DGS surface inaccuracy.", infer_lim="Specular highlights can still be absorbed into color and bias surface depth.", evidence="Local PDF abstract; Sec. 3 losses."),
    r("3D Gaussian Splatting with Self-Constrained Priors for High Fidelity Surface Reconstruction", 2025, "arXiv preprint", "local PDF", "", "Improve 3DGS surface quality.", "Posed RGB.", "3DGS with self-constrained geometry priors.", "3DGS", mesh="Yes", geom="Self constraints from rendered geometry.", normal="Gaussian/depth normals.", loss="RGB plus self-constrained geometry regularizers.", strengths="Reduces geometry noise without extra sensors.", infer_lim="Reflective surfaces remain underconstrained because reflection transport is not modeled.", evidence="Local PDF abstract/Sec. 1."),
    r("3DGSR: Implicit Surface Reconstruction with 3D Gaussian Splatting", 2024, "arXiv / ACM-linked", "https://arxiv.org/abs/2404.00409", "https://github.com/CVMI-Lab/3DGSR", "Joint 3DGS rendering and SDF surface reconstruction.", "Posed RGB.", "3D Gaussians plus neural SDF.", "Hybrid 3DGS + SDF", mesh="Yes, SDF mesh", geom="SDF-to-opacity and Gaussian/SDF consistency.", normal="SDF gradients aligned with rendered Gaussian normals.", render="Gaussian rasterization plus SDF-derived opacity.", loss="RGB, Eikonal/SDF, depth and normal consistency.", strengths="SDF improves coherent surface extraction.", infer_lim="Specular radiance is still baked unless reflection/material factors are explicit.", evidence="Local PDF abstract; Sec. 3."),
    r("Toward a Theory of Shape from Specular Flow", 2007, "Vision theory paper", "local PDF", "", "Theoretical relation between specular flow and shape.", "Known motion/environment assumptions.", "Differential specular geometry.", "Classical geometry", "Yes", "Yes", "Under assumptions", "No", geom="Specular-flow constraints.", normal="Differential surface constraints from reflection flow.", render="Analytic mirror reflection geometry.", loss="Specular-flow equations.", datasets="Synthetic/theoretical examples.", metrics="Qualitative/theoretical identifiability.", strengths="Shows reflections contain shape information.", author_lim="Requires strong assumptions on environment/motion.", infer_lim="Hard to use directly for uncontrolled posed RGB captures.", evidence="Local PDF Sec. theory pages."),
    r("Specular Flow and the Recovery of Surface Structure", 2006, "ECCV/IJCV-era vision paper", "local PDF", "", "Recover shape from specular image motion.", "Smooth specular surface and motion cues.", "Specular-flow field.", "Classical geometry", "Yes", "Yes", "Under assumptions", "No", geom="Specular-flow observations.", normal="Normals from flow constraints.", render="Geometric reflection model.", loss="Flow consistency.", strengths="Foundational specular shape prior.", author_lim="Strong calibration/environment assumptions.", infer_lim="Does not provide mesh/material pipeline for sparse multiview RGB.", evidence="Local PDF abstract; Sec. 2-4."),
    r("Deep Flow Rendering: View Synthesis via Layer-aware Reflection Flow", 2022, "Eurographics Symposium on Rendering", "local PDF", "", "View synthesis with reflection layers.", "Input views with reflection layers.", "Neural image-based rendering with reflection flow.", "Neural image-based hybrid", "Yes", "Partial", "Implicit", "No", render="Layer-aware neural rendering.", loss="Photometric and flow/rendering losses.", strengths="Models reflection motion better than single radiance field.", author_lim="NVS rather than reconstruction.", infer_lim="No mesh, UV, or PBR material recovery.", evidence="Local PDF abstract."),
    r("DN-Splatter: Depth and Normal Priors for Gaussian Splatting and Meshing", 2025, "WACV", "https://arxiv.org/abs/2403.17822", "https://maturk.github.io/dn-splatter/", "Regularize GS geometry and meshing with priors.", "Posed RGB plus depth/normal priors.", "3DGS with external priors.", "3DGS", mesh="Yes", geom="Monocular/depth priors and adaptive depth supervision.", normal="Monocular normal priors and local smoothness.", loss="RGB, depth, normal, smoothness losses.", datasets="Indoor reconstruction datasets.", strengths="Helpful for weak geometric signal.", author_lim="Prior quality matters.", infer_lim="Reflective surfaces may violate learned monocular priors.", evidence="Local PDF abstract; WACV abstract."),
    r("EnvGS: Modeling View-Dependent Appearance with Environment Gaussian", 2025, "arXiv preprint", "local PDF", "", "Model view-dependent appearance in GS.", "Posed RGB static scenes.", "3DGS plus environment Gaussian appearance.", "3DGS + appearance field", "Yes, appearance-level", "Partial", "No", "No", mat="Appearance factorization, not physical material.", render="Gaussian rasterization with environment appearance.", strengths="Efficient view-dependent rendering.", infer_lim="Near-field reflected objects and PBR maps are not explicit.", evidence="Local PDF abstract/Sec. 3."),
    r("SSR-GS: Separating Specular Reflection in Gaussian Splatting for Glossy Surface Reconstruction", 2026, "arXiv preprint", "https://arxiv.org/abs/2603.05152", "project linked from arXiv", "Separate direct and indirect specular reflection for glossy reconstruction.", "Posed RGB; visual geometry priors.", "3DGS plus mip-cubemap and anisotropic SG.", "3DGS + reflection model", "Yes", "Glossy partial", "Approximate", "Indirect specular component", mesh="Likely surface/depth", geom="Visual geometry priors and reflection-score weighting.", normal="Prior-transformed normal constraints.", mat="Direct/indirect specular separation.", render="Gaussian rasterization plus cubemap/SG reflection.", loss="RGB, reflection-score weighted geometry, depth, normal.", strengths="Explicit reflective-region treatment.", author_lim="Preprint; prior dependent.", infer_lim="No UV-ready PBR asset; priors can bias unusual reflections.", evidence="Local PDF; arXiv abstract."),
    r("Gaussian Opacity Fields: Efficient and Compact Surface Reconstruction in Unbounded Scenes", 2024, "arXiv / CVPR-related", "https://arxiv.org/abs/2404.10772", "", "Extract surfaces from Gaussian opacity fields.", "Trained/optimized 3DGS.", "Gaussian opacity field and marching tetrahedra.", "3DGS / opacity field / mesh", mesh="Yes", geom="Opacity and geometry regularization.", normal="Ray-Gaussian intersection-plane normals.", render="Ray-tracing/opacity level-set extraction.", strengths="Avoids Poisson/TSDF dependence.", infer_lim="Reflective radiance can create opacity artifacts.", evidence="Local PDF abstract."),
    r("Geometry Field Splatting with Gaussian Surfels", 2025, "CVPR", "https://openaccess.thecvf.com/content/CVPR2025/html/Jiang_Geometry_Field_Splatting_with_Gaussian_Surfels_CVPR_2025_paper.html", "", "Surface reconstruction with Gaussian surfels.", "Posed RGB; opaque-surface assumption.", "Gaussian surfels and geometry field.", "Surface Gaussians / surfels", "Targets specular via reflection-vector latent representation", "No", "No", "No", mesh="Yes", geom="RGB plus geometric consistency.", normal="Surfel normals and depth-normal consistency.", render="Surfel splatting with continuous color.", loss="RGB, depth distortion, depth-normal consistency.", datasets="DTU and surface benchmarks.", strengths="Strong surface representation.", author_lim="Assumes opaque surfaces; transparent/fuzzy objects limited.", infer_lim="Mirror-like radiance violates opaque local-surface color assumptions.", evidence="Local PDF; CVF abstract and limitation discussion."),
    r("GeoSplatting: Towards Geometry Guided Gaussian Splatting for Physically-based Inverse Rendering", 2025, "ICCV", "https://arxiv.org/abs/2410.24204", "https://pku-vcl-geometry.github.io/GeoSplatting/", "Geometry-guided GS inverse rendering.", "Posed RGB and optimizable mesh.", "Mesh-grounded 3DGS with BRDF and lighting.", "Hybrid mesh + 3DGS", "Yes", "No mirror-specific", "Occlusion-aware only", "Partial indirect/occlusion", "Yes/guided mesh", pbr="BRDF/material attributes", relight="Yes", edit="Yes", geom="Opaque mesh surface and ray-tracing guidance.", normal="Mesh normals replace noisy Gaussian normals.", mat="BRDF/environment decomposition.", render="Differentiable PBR with mesh-based ray tracing.", loss="RGB, BRDF, normal, light, smoothness.", strengths="Directly addresses normal and occlusion weakness.", author_lim="Depends on mesh quality and opaque surface.", infer_lim="Hard mirror/near-field reflections need explicit reflection-field constraints.", evidence="Local PDF abstract; project page."),
    r("GlossyGS: Inverse Rendering of Glossy Objects with 3D Gaussian Splatting", 2024, "arXiv preprint", "https://arxiv.org/abs/2410.13349", "", "Geometry/material reconstruction for glossy objects.", "Posed glossy object captures.", "Hybrid explicit/implicit GS with material priors.", "3DGS / hybrid", "Yes", "Glossy partial", "No explicit", "No explicit", mesh="Geometry output likely", pbr="Material attributes", relight="Yes", edit="Potential", geom="Material priors and microfacet segmentation prior.", normal="Normal-map prefiltering and GS normals.", mat="Microfacet/material priors.", render="3DGS inverse rendering.", loss="RGB, material prior, normal/geometric regularizers.", strengths="Directly targets glossy inverse rendering.", author_lim="Prior-dependent ambiguity reduction.", infer_lim="No near-field/inter-reflection or UV-ready asset guarantee.", evidence="Local PDF abstract; arXiv abstract."),
    r("GS-2DGS: Geometrically Supervised 2DGS for Reflective Object Reconstruction", 2025, "arXiv preprint", "local PDF", "", "Reflective object reconstruction using supervised 2DGS geometry.", "Posed RGB plus geometry supervision/priors.", "2DGS with geometric supervision.", "2DGS / surface Gaussians", "Yes", "Partial", "No explicit", "No explicit", mesh="Yes", geom="External or inferred geometric supervision.", normal="2D disk normals with depth/normal losses.", render="2DGS rasterization.", loss="RGB, geometry, normal/depth losses.", strengths="Combines reflective target with surface primitive.", author_lim="Requires reliable geometric supervision.", infer_lim="PBR/UV mapping and near-field reflection remain open.", evidence="Local PDF title/abstract."),
    r("GS-2M: Gaussian Splatting for Joint Mesh Reconstruction and Material Decomposition", 2026, "CGF / Eurographics-related preprint", "https://arxiv.org/abs/2509.22276", "", "Joint mesh reconstruction and material decomposition.", "Posed RGB object/scene captures.", "3DGS with material-aware mesh reconstruction.", "3DGS + mesh + material", "Yes", "Glossy partial", "No explicit", "No explicit", "Yes", "Unclear", "Material attributes/maps", "Potential", "Potential", geom="Material-aware geometry constraints.", normal="Surface/Gaussian normals.", mat="Roughness/albedo/material optimization.", render="Gaussian rendering with material model.", loss="RGB, material, geometry, smoothness.", strengths="Very close to desired joint mesh+material route.", author_lim="Roughness supervision is indirect.", infer_lim="Near-field/mirror inter-reflection and explicit UV output remain uncertain.", evidence="Local PDF; arXiv abstract."),
    r("GS2Mesh: Surface Reconstruction from Gaussian Splatting via Novel Stereo Views", 2024, "ECCV", "https://arxiv.org/abs/2404.01810", "https://gs2mesh.github.io/", "Recover mesh from 3DGS-rendered stereo.", "Trained 3DGS and pretrained stereo depth.", "3DGS plus stereo depth and TSDF.", "3DGS + external stereo + mesh", mesh="Yes", geom="Stereo depth from novel rendered pairs.", normal="Normals from fused depth/mesh.", render="Render stereo pairs, estimate depth, TSDF fuse.", loss="No direct material loss; stereo/depth fusion.", datasets="DTU, Tanks and Temples, in-the-wild.", strengths="Avoids direct noisy Gaussian geometry.", author_lim="Inherits stereo-model bias.", infer_lim="Specular correspondence violates stereo assumptions.", evidence="Local PDF; project abstract."),
    r("PolGS: Polarimetric Gaussian Splatting for Fast Reflective Surface Reconstruction", 2025, "ICCV / arXiv", "https://arxiv.org/abs/2509.19726", "", "Reflective surface reconstruction with polarization.", "Multi-view polarized images and poses.", "3DGS with polarimetric constraints.", "3DGS + polarization", "Yes", "Reflective partial", "No", "No", mesh="Surface/depth likely", geom="Polarization image formation and multiview constraints.", normal="Polarization-derived normals with ambiguity handling.", mat="Diffuse/specular separation cues, not PBR maps.", render="Gaussian rasterization with polarimetric supervision.", loss="RGB/polarization consistency, geometry/normal losses.", strengths="Adds physical signal for reflective surfaces.", author_lim="Requires polarization hardware/data.", infer_lim="Not RGB-only and not UV/PBR asset focused.", evidence="Local PDF; arXiv abstract."),
    r("PolGS++: Physically-Guided Polarimetric Gaussian Splatting for Fast Reflective Surface Reconstruction", 2026, "preprint / manuscript", "local PDF", "", "Physically guided polarimetric reflective reconstruction.", "Polarized multi-view images.", "3DGS plus physical polarimetric model.", "3DGS + polarization", "Yes", "Reflective partial", "No", "No", mesh="Surface/depth likely", geom="Physically guided polarization constraints.", normal="Polarization-derived normals.", mat="Diffuse/specular cues.", render="Gaussian rasterization and polarization model.", loss="RGB, polarization, normal losses.", strengths="Stronger physics than RGB-only.", author_lim="Specialized capture.", infer_lim="Cannot address ordinary RGB capture and UV baking alone.", evidence="Local PDF abstract."),
    r("IRGS: Inter-Reflective Gaussian Splatting with 2D Gaussian Ray Tracing", 2025, "arXiv preprint", "local PDF", "", "Inter-reflective GS with ray tracing.", "Posed RGB inter-reflective scenes.", "2D Gaussians with ray tracing.", "2DGS + ray tracing", "Yes", "Partial", "Yes if traced paths include local surfaces", "Yes", mesh="Possibly via 2DGS", pbr="Material attributes maybe", relight="Yes/limited", geom="2DGS surface and traced reflection constraints.", normal="2DGS normals.", mat="Material-aware reflection decomposition.", render="2D Gaussian ray tracing plus rasterization.", loss="RGB, reflection/ray consistency, geometry losses.", strengths="Directly targets inter-reflection.", author_lim="Ray tracing cost/approximations.", infer_lim="UV/PBR baking and stable optimization remain open.", evidence="Local PDF abstract/Sec. 3."),
    r("Neural Point Catacaustics for Novel-View Synthesis of Reflections", 2022, "SIGGRAPH Asia / TOG", "https://arxiv.org/abs/2301.01087", "https://repo-sam.inria.fr/fungraph/neural_catacaustics/", "NVS of curved reflections.", "Multiview images and reflector annotation/assumptions.", "Point cloud plus neural catacaustic/reflection flow.", "Neural point / reflection field", "Yes", "Yes for curved reflectors", "Yes", "No full multi-bounce", edit="Reflection editing/cloning", geom="Catacaustic/reflection-flow constraints.", normal="Reflection geometry, not full normal maps.", render="Neural point rendering with reflection flow.", loss="Photometric and flow consistency.", strengths="Models reflection paths instead of baking colors.", author_lim="Needs reflector annotation; not full material recovery.", infer_lim="No mesh/UV/PBR reconstruction.", evidence="Local PDF; project page."),
    r("MaterialRefGS: Reflective Gaussian Splatting with Multi-view Consistent Material Inference", 2025, "NeurIPS 2025 / preprint", "https://yushen-liu.github.io/main/pdf/LiuYS_NeurIPS25_MaterialRefGS.pdf", "", "Reflective GS with multi-view material inference.", "Posed RGB reflective scenes.", "GS with material attributes.", "GS + material", "Yes", "Glossy/mirror partial", "Potentially", "Limited", mesh="Not primary", pbr="PBR-related attributes", relight="Yes", edit="Yes", geom="Multi-view material consistency.", normal="Gaussian/surface normals.", mat="Multi-view consistent material inference.", render="PBR-inspired GS rendering.", loss="RGB, material consistency, normal/geometry.", strengths="Links reflective GS to material inference.", author_lim="Publication details should be checked from final PDF.", infer_lim="No UV material baking and limited near-field inter-reflection.", evidence="Local PDF and linked PDF."),
    r("MILo: Mesh-In-the-Loop Gaussian Splatting for Detailed and Efficient Surface Reconstruction", 2025, "TOG / SIGGRAPH Asia preprint", "https://arxiv.org/abs/2506.24096", "", "Differentiable mesh extraction during GS training.", "Posed RGB.", "3DGS plus per-iteration mesh.", "3DGS + mesh", mesh="Yes", geom="Bidirectional Gaussian-mesh consistency.", normal="Mesh normals and Gaussian geometry.", render="Gaussian rendering with mesh consistency.", loss="RGB, Gaussian-mesh consistency, SDF/geometry.", strengths="Produces lightweight complete meshes.", author_lim="Complex differentiable connectivity.", infer_lim="No reflective material separation.", evidence="Local PDF; arXiv abstract."),
    r("PGSR: Planar-based Gaussian Splatting for Efficient and High-Fidelity Surface Reconstruction", 2024, "TVCG / arXiv", "https://arxiv.org/abs/2406.06521", "https://zju3dv.github.io/pgsr/", "Planar GS for surface reconstruction.", "Posed RGB; exposure variations.", "Planar Gaussian splats.", "Surface Gaussians", mesh="Yes", geom="Single-view and multi-view geometric regularization.", normal="Unbiased depth and normal maps.", render="Planar Gaussian rasterization.", loss="Photometric, geometry consistency, exposure compensation.", strengths="Efficient high-fidelity surfaces.", author_lim="Not material/reflection-aware.", infer_lim="Reflection radiance remains entangled with geometry.", evidence="Local PDF; project abstract."),
    r("Reflective Gaussian Splatting", 2025, "ICLR", "https://arxiv.org/abs/2412.19282", "", "Reflective object reconstruction with inter-reflection.", "Posed RGB reflective objects.", "2DGS plus material-aware deferred PBR and inter-reflection.", "2DGS + PBR + reflection", "Yes", "Reflective/mirror partial", "Indirect near-field partial", "Yes", mesh="Surface possible", pbr="Material attributes", relight="Yes", edit="Yes", geom="2DGS/surface geometry and material constraints.", normal="Surface/2DGS normals.", mat="Pixel/material property inference.", render="Deferred PBR with split-sum and Gaussian-grounded inter-reflection.", loss="RGB, material, geometry, inter-reflection.", strengths="Closest reflective GS route.", author_lim="Approximate inter-reflection; depends on normals/materials.", infer_lim="Does not target mesh plus UV PBR texture baking as final asset.", evidence="Local PDF; arXiv abstract."),
    r("SOF: Sorted Opacity Fields for Fast Unbounded Surface Reconstruction", 2025, "TOG / preprint", "local PDF", "", "Fast surface reconstruction from sorted opacity fields.", "Optimized GS-like opacity field.", "Sorted opacity field.", "3DGS/opacity field/mesh", mesh="Yes", geom="Opacity sorting and geometry regularization.", normal="Opacity-field normals/depth.", render="Opacity-field rendering/extraction.", strengths="Fast unbounded reconstruction.", author_lim="Not inverse rendering/material-aware.", infer_lim="Reflective objects can induce wrong opacity surfaces.", evidence="Local PDF abstract."),
    r("SSD-GS: Scattering and Shadow Decomposition for Relightable 3D Gaussian Splatting", 2025, "ICLR / preprint", "local PDF", "", "Relightable GS via scattering/shadow decomposition.", "Posed RGB and lighting assumptions.", "3DGS with scattering/shadow factors.", "3DGS + relighting", "Partial", "No", "No", "Shadow/indirect effects", relight="Yes", edit="Maybe", mat="Scattering and shadow decomposition.", render="Relightable Gaussian rendering.", loss="RGB, decomposition, relighting consistency.", strengths="Addresses relighting factors.", infer_lim="No mirror/near-field reflection or mesh/UV output.", evidence="Local PDF abstract."),
    r("SuGaR: Surface-Aligned Gaussian Splatting for Efficient 3D Mesh Reconstruction and High-Quality Mesh Rendering", 2024, "CVPR", "https://openaccess.thecvf.com/content/CVPR2024/papers/Guedon_SuGaR_Surface-Aligned_Gaussian_Splatting_for_Efficient_3D_Mesh_Reconstruction_and_CVPR_2024_paper.pdf", "https://anttwo.github.io/sugar/", "Efficient mesh extraction from 3DGS.", "Posed RGB or trained 3DGS.", "Surface-aligned Gaussians and mesh.", "3DGS + mesh", mesh="Yes", relight="Limited by mesh-bound Gaussians", edit="Yes, geometric/animation editing", geom="Surface-alignment regularization.", normal="Shortest-axis/surface-aligned normals.", render="3DGS and mesh-bound rendering.", loss="Photometric plus density/surface regularization.", datasets="Mip-NeRF360, Tanks and Temples, DTU-like.", strengths="Seminal GS-to-mesh route.", author_lim="Mesh tied to Gaussian alignment.", infer_lim="Reflective color blobs can align to apparent reflected content.", evidence="Local PDF; CVPR Fig. 2-3."),
    r("SpecTRe-GS: Modeling Highly Specular Surfaces with Reflected Nearby Objects by Tracing Rays in 3D Gaussian Splatting", 2026, "arXiv preprint", "local PDF", "", "Highly specular surfaces with reflected nearby objects.", "Posed RGB with local reflected objects.", "3DGS with traced reflection rays.", "3DGS + ray tracing", "Yes", "Mirror-like/specular", "Yes", "Single-bounce likely", mesh="Geometry/depth likely", relight="Maybe", geom="Ray-traced reflection constraints.", normal="Normals for reflection rays.", mat="Reflection separation rather than UV PBR.", render="3DGS plus traced reflection rendering.", loss="RGB, reflection ray consistency, geometry losses.", strengths="Directly targets near-field reflected objects.", author_lim="Ray tracing cost and normal dependence.", infer_lim="No full UV/PBR asset or multi-bounce guarantee.", evidence="Local PDF title/abstract."),
    r("RefGaussian: Disentangling Reflections from 3D Gaussian Splatting for Realistic Rendering", 2024, "arXiv preprint", "local PDF", "", "Disentangle reflections in 3DGS rendering.", "Posed RGB reflective scenes.", "3DGS with reflection separation branch.", "3DGS", "Yes", "Partial", "No explicit", "No", mat="Reflection-separated appearance.", render="3DGS rasterization with reflection branch.", loss="RGB and disentanglement losses.", strengths="Addresses reflection entanglement for rendering.", author_lim="Preprint details need exact arXiv verification.", infer_lim="No mesh/UV/PBR output.", evidence="Local PDF."),
    r("Ref-GS: Directional Factorization for 2D Gaussian Splatting", 2025, "arXiv preprint", "local PDF", "", "Directional factorization for 2DGS view dependence.", "Posed RGB.", "2DGS with directional appearance factorization.", "2DGS", "Yes appearance-level", "Partial", "No", "No", mesh="Surface possible", mat="Directional radiance factorization.", render="2DGS rasterization.", loss="RGB, directional, geometry losses.", strengths="Improves view-dependent effects on surface splats.", infer_lim="Directional appearance alone cannot infer PBR maps or near-field reflection.", evidence="Local PDF abstract."),
    r("MGSR: 2D/3D Mutual-boosted Gaussian Splatting for High-fidelity Surface Reconstruction under Various Light Conditions", 2025, "arXiv preprint", "local PDF", "", "Surface reconstruction under varied lighting.", "Posed RGB under light variation.", "Mutual-boosted 2D and 3D Gaussians.", "Hybrid 2DGS + 3DGS", "Lighting variation, not specular-specific", mesh="Yes", geom="2D/3D mutual geometric constraints.", normal="2DGS/surface normals.", render="Hybrid Gaussian rendering.", loss="RGB and mutual geometry/normal regularizers.", strengths="Combines 2D surface accuracy and 3D appearance.", infer_lim="Reflective variation can still be mistaken for geometry/material.", evidence="Local PDF abstract."),
    r("3D Gaussian Splatting for Real-Time Radiance Field Rendering", 2023, "SIGGRAPH / TOG", "https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/", "https://github.com/graphdeco-inria/gaussian-splatting", "Real-time radiance-field rendering.", "Posed RGB and SfM points.", "Anisotropic 3D Gaussians with SH color.", "3DGS", "Only view-dependent color", geom="Photometric densification/pruning.", normal="No explicit surface normals.", render="Tile-based differentiable Gaussian rasterization.", loss="L1/SSIM photometric.", datasets="Mip-NeRF360, Tanks and Temples, Deep Blending.", strengths="Speed/quality baseline.", author_lim="Not designed for accurate surface/material recovery.", infer_lim="Geometry and view-dependent appearance are entangled.", evidence="Original paper Sec. 3; project page."),
    r("Ref-NeRF: Structured View-Dependent Appearance for Neural Radiance Fields", 2022, "CVPR", "https://openaccess.thecvf.com/content/CVPR2022/html/Verbin_Ref-NeRF_Structured_View-Dependent_Appearance_for_Neural_Radiance_Fields_CVPR_2022_paper.html", "https://dorverbin.github.io/refnerf/", "Glossy NeRF view synthesis.", "Posed RGB.", "NeRF with reflection-direction encoding.", "Neural field", "Yes", "Glossy, not mirror reconstruction", geom="Volumetric photometric training.", normal="Density-field normals with orientation regularization.", render="Volumetric rendering with reflected-direction parameterization.", loss="Photometric and normal/orientation regularizers.", datasets="Shiny Blender and real captures.", strengths="Reflection direction is an effective view-dependence coordinate.", author_lim="NeRF is slow and not an asset/PBR output.", infer_lim="No mesh/UV/PBR final asset.", evidence="CVPR Sec. 3; Fig. 2."),
    r("NeRO: Neural Geometry and BRDF Reconstruction of Reflective Objects from Multiview Images", 2023, "SIGGRAPH / TOG", "https://arxiv.org/abs/2305.17398", "https://liuyuan-pal.github.io/NeRO/", "Reflective object geometry and BRDF recovery.", "Posed RGB object images.", "Neural SDF with BRDF and environment light.", "SDF / neural field", "Yes", "Reflective/mirror partial", "Indirect lighting considered", "Approximate", "Yes via SDF", pbr="BRDF fields", relight="Yes", edit="Yes", geom="SDF photometric/geometric constraints.", normal="SDF gradients.", mat="BRDF and environment recovery.", render="Split-sum approximation with direct/indirect light.", loss="Photometric, Eikonal, BRDF/light regularization.", strengths="Strong non-GS reflective inverse-rendering baseline.", author_lim="Two-stage/slower neural pipeline.", infer_lim="No fast GS or UV baking emphasis.", evidence="SIGGRAPH abstract; project pipeline."),
    r("GS-IR: 3D Gaussian Splatting for Inverse Rendering", 2024, "CVPR", "https://arxiv.org/abs/2311.16473", "https://github.com/lzhnb/GS-IR", "3DGS inverse rendering and relighting.", "Posed RGB.", "3DGS with normals, material, environment, baked occlusion.", "3DGS + PBR", "Yes", "No mirror-specific", "No", "Approximate occlusion/indirect", pbr="PBR-like attributes", relight="Yes", edit="Yes", geom="Depth-derived normal and occlusion regularization.", normal="Depth-derived normals.", mat="BRDF/material and environment estimation.", render="Forward splatting with PBR and baked occlusion.", loss="RGB, material smoothness, normal, illumination.", datasets="TensoIR Synthetic, Mip-NeRF360.", strengths="Seminal GS inverse-rendering baseline.", author_lim="Normals and occlusion are approximations.", infer_lim="Highly reflective geometry remains fragile because normals are not true surface normals.", evidence="CVPR abstract; Sec. 3.2-3.3."),
    r("GaussianShader: 3D Gaussian Splatting with Shading Functions for Reflective Surfaces", 2024, "CVPR", "https://openaccess.thecvf.com/content/CVPR2024/html/Jiang_GaussianShader_3D_Gaussian_Splatting_with_Shading_Functions_for_Reflective_Surfaces_CVPR_2024_paper.html", "https://github.com/Asparagus15/GaussianShader", "Reflective-surface rendering in 3DGS.", "Posed RGB.", "3DGS with normals and simplified shading.", "3DGS + shading", "Yes", "Glossy", "No", "No", geom="Normal/geometry regularization.", normal="Shortest-axis Gaussian normals.", mat="Simplified shading, not full PBR.", render="Gaussian rasterization plus shading function.", loss="RGB, normal consistency, shading losses.", strengths="Explicit reflective 3DGS rendering.", author_lim="No mesh/material output.", infer_lim="Rendering quality can improve while asset reconstruction remains unresolved.", evidence="CVPR abstract; Sec. 3."),
    r("Spec-Gaussian: Anisotropic View-Dependent Appearance for 3D Gaussian Splatting", 2024, "NeurIPS", "https://arxiv.org/abs/2402.15870", "", "High-frequency anisotropic view-dependent appearance.", "Posed RGB.", "3DGS with anisotropic spherical Gaussian appearance.", "3DGS", "Yes appearance-level", "Glossy", "No", "No", mat="None; appearance field.", render="Gaussian rasterization with ASG appearance.", loss="RGB and appearance regularizers.", strengths="Captures specular appearance better than SH.", author_lim="Appearance-focused.", infer_lim="Can hide geometry errors behind expressive view dependence.", evidence="arXiv abstract; NeurIPS paper."),
    r("MirrorGaussian: Reflecting 3D Gaussians for Reconstructing Mirror Reflections", 2024, "ECCV", "https://arxiv.org/abs/2405.11921", "https://mirror-gaussian.github.io", "Mirror-scene reconstruction and editing.", "Posed RGB with planar mirror.", "Real-space and reflected virtual Gaussians.", "3DGS + mirror transform", "Yes", "Yes planar", "Yes via virtual objects", "Single-bounce mirror", edit="Yes", geom="Mirror plane and dual-space constraints.", normal="Mirror plane geometry.", render="Dual rendering of real and mirrored Gaussian spaces.", loss="Photometric plus mirror consistency.", strengths="Strong planar mirror treatment.", author_lim="Assumes planar mirror symmetry.", infer_lim="Not for curved reflective object material maps.", evidence="ECCV abstract; project Fig. 2."),
    r("GS-ROR²: Bidirectional-guided 3DGS and SDF for Reflective Object Relighting and Reconstruction", 2024, "arXiv preprint", "https://arxiv.org/abs/2406.18544", "", "Reflective object relighting and reconstruction.", "Posed RGB reflective objects.", "Coupled 3DGS and SDF.", "Hybrid 3DGS + SDF", "Yes", "Reflective/glossy", "Limited", "No full multi-bounce", "Yes via SDF", pbr="Material/relighting attributes", relight="Yes", edit="Potential", geom="Bidirectional depth/normal guidance.", normal="SDF and Gaussian normals supervise each other.", mat="Deferred shading/material estimation.", render="Gaussian splatting plus SDF-aware deferred shading.", loss="RGB, depth/normal, SDF consistency, shading.", strengths="Close reflective mesh+relighting route.", author_lim="Extra SDF cost/complexity.", infer_lim="No UV/PBR texture-map export.", evidence="arXiv abstract."),
    r("NeRSP: Neural 3D Reconstruction for Reflective Objects with Sparse Polarized Images", 2024, "CVPR", "https://arxiv.org/abs/2406.07111", "", "Sparse reflective reconstruction with polarization.", "Sparse polarized images and poses.", "Neural implicit surface plus polarization.", "SDF / neural field + polarization", "Yes", "Reflective partial", mesh="Yes via implicit surface", geom="Polarization image formation and multiview azimuth consistency.", normal="Polarization-derived normals.", render="Neural surface rendering with polarization.", loss="Photometric, Eikonal, polarization/azimuth.", strengths="Strong physical signal under sparse views.", author_lim="Requires polarization capture.", infer_lim="Not RGB-only GS or UV baking.", evidence="CVPR abstract; Sec. 3."),
    r("GUS-IR: Gaussian Splatting with Unified Shading for Inverse Rendering", 2024, "arXiv preprint", "https://arxiv.org/abs/2411.07478", "", "Unified shading for GS inverse rendering.", "Posed RGB.", "3DGS with unified forward/deferred shading.", "3DGS + PBR", "Yes", "No mirror-specific", "No", "Approximate indirect/occlusion", pbr="PBR-like attributes", relight="Yes", edit="Yes", geom="Normal and AO regularization.", normal="Shortest-axis plus depth-regularized normals.", mat="BRDF/material and illumination.", render="Unified shading and AO baking.", loss="RGB, material, normal, AO.", strengths="Improves shading consistency.", author_lim="Approximate indirect illumination.", infer_lim="No mesh/UV or near-field reflection model.", evidence="arXiv abstract."),
    r("Relightable 3D Gaussians: Realistic Point Cloud Relighting with BRDF Decomposition and Ray Tracing", 2024, "ECCV", "https://eccv.ecva.net/virtual/2024/poster/2401", "", "Relightable Gaussian/point-cloud assets.", "Posed images/point cloud.", "Gaussians/points with normals, BRDF, incident light.", "3DGS / point PBR", "Yes", "No mirror-specific", "Visibility/shadows", "Secondary visibility", pbr="BRDF parameters", relight="Yes", edit="Yes", geom="Normals and ray tracing visibility.", normal="Estimated primitive normals.", mat="BRDF decomposition.", render="Point-based PBR with BVH ray tracing.", loss="Photometric, BRDF, light, visibility.", strengths="Ray tracing gives stronger visibility.", author_lim="Visibility precompute/complexity.", infer_lim="Not UV mesh focused.", evidence="ECCV abstract/poster."),
    r("GIR: 3D Gaussian Inverse Rendering for Relightable Scene Factorization", 2025, "TPAMI", "https://3dgir.github.io/", "https://3dgir.github.io/", "Relightable scene factorization.", "Posed RGB.", "3DGS with geometry/material/illumination.", "3DGS + inverse rendering", "Yes", "No mirror-specific", "No", "Simulated indirect", pbr="Material attributes", relight="Yes", edit="Yes", geom="Self-regularized normals and illumination.", normal="Self-regularized normals.", mat="Material/illumination estimation.", render="Gaussian inverse rendering with indirect approximation.", loss="RGB, normal/material/light regularizers.", strengths="Mature relightable GS factorization.", author_lim="Normals approximated.", infer_lim="No mesh/UV/PBR asset.", evidence="Project page."),
    r("SVG-IR: Spatially-Varying Gaussian Splatting for Inverse Rendering", 2025, "CVPR", "https://openaccess.thecvf.com/content/CVPR2025/html/Sun_SVG-IR_Spatially-Varying_Gaussian_Splatting_for_Inverse_Rendering_CVPR_2025_paper.html", "", "Spatially varying GS inverse rendering.", "Posed RGB.", "Spatially varying Gaussian attributes.", "3DGS + inverse rendering", "Yes", "No mirror-specific", "No", "Indirect lighting approximate", pbr="Spatially varying BRDF attributes", relight="Yes", edit="Yes", geom="Physically based indirect lighting/material supervision.", normal="Spatially varying normal/material per Gaussian.", mat="BRDF parameter fields.", render="SVG splatting with PBR indirect lighting.", loss="RGB, material/normal smoothness, relighting.", strengths="Fixes constant-per-Gaussian limitation.", author_lim="Not UV-baked mesh asset.", infer_lim="Hard mirror/near-field reflections not targeted.", evidence="CVPR abstract."),
    r("TexGaussian: Generating High-quality PBR Material via Octree-based 3D Gaussian Splatting", 2025, "CVPR", "https://3d-aigc.github.io/TexGaussian/", "https://3d-aigc.github.io/TexGaussian/", "Generate PBR material textures for meshes.", "Input mesh and generative conditioning.", "Octree-aligned 3DGS over mesh with UV baking.", "Mesh + 3DGS texture generation", "PBR specular output", "No reconstruction", "No", "No", "Input mesh", "Yes", "Yes", "Yes through PBR", "Yes", geom="Mesh geometry given.", normal="Mesh normals.", mat="Albedo/roughness/metallic prediction and baking.", render="Multiview PBR rendering and texture baking.", loss="PBR multiview and texture consistency.", strengths="Important UV/PBR baking reference.", author_lim="Generation, not inverse capture.", infer_lim="Baking stage useful but reconstruction signal absent.", evidence="Project page."),
    r("NeRD: Neural Reflectance Decomposition from Image Collections", 2021, "ICCV", "https://arxiv.org/abs/2012.03918", "https://markboss.me/publication/2021-nerd/", "Recover relightable textured mesh.", "Image collections under varying illumination.", "Neural reflectance volume convertible to mesh.", "Neural field + mesh output", "Yes", "No mirror-specific", "No", "No", "Yes", "Textured mesh", "BRDF/material maps", "Yes", "Yes", geom="Multiview plus varying illumination constraints.", normal="Learned geometry normals.", mat="Neural BRDF decomposition.", render="Physically based rendering.", loss="Photometric, geometry, material, light.", strengths="Asset-oriented inverse-rendering precedent.", author_lim="Pre-3DGS and slower.", infer_lim="Useful output target but not fast reflective GS.", evidence="ICCV abstract."),
    r("PhySG: Inverse Rendering with Spherical Gaussians for Physics-based Material Editing and Relighting", 2021, "CVPR", "https://kai-46.github.io/PhySG-website/", "https://kai-46.github.io/PhySG-website/", "Joint geometry/material/light recovery.", "Posed RGB object images.", "SDF with spherical-Gaussian BRDF/light.", "SDF / neural field", "Yes", "Glossy not pure mirror", "No", "Approximate visibility", "Yes via SDF", pbr="BRDF fields", relight="Yes", edit="Yes", geom="SDF photometric/Eikonal.", normal="SDF gradients.", mat="SG BRDF and illumination.", render="Closed-form SG approximation to rendering equation.", loss="Photometric, Eikonal, material/light.", strengths="Strong physical decomposition baseline.", author_lim="Approximate SG lighting.", infer_lim="No GS speed or UV baking.", evidence="CVPR project/paper."),
    r("NeRFactor: Neural Factorization of Shape and Reflectance Under an Unknown Illumination", 2021, "SIGGRAPH Asia / TOG", "https://arxiv.org/abs/2106.01970", "https://xiuming.info/projects/nerfactor/", "Factor shape, reflectance, visibility, illumination.", "Posed RGB under unknown illumination; pretrained NeRF.", "Neural fields distilled from NeRF.", "Neural field", "Yes", "No mirror-specific", "No", "Visibility only", mesh="Possible, not primary", pbr="BRDF fields", relight="Yes", edit="Yes", geom="Distilled geometry/visibility priors.", normal="Density/surface normals.", mat="Albedo, BRDF, environment with priors.", render="Visibility-aware rendering equation.", loss="Photometric, BRDF prior, smoothness.", strengths="Classic prior-driven inverse rendering.", author_lim="Underconstrained and prior-dependent.", infer_lim="No GS or mesh/UV asset pipeline.", evidence="TOG abstract."),
    r("TensoIR: Tensorial Inverse Rendering", 2023, "CVPR", "https://arxiv.org/abs/2304.12461", "https://haian-jin.github.io/TensoIR/", "Efficient neural inverse rendering with secondary effects.", "Posed RGB.", "Tensor-factorized neural field.", "Neural field", "Yes", "No mirror-specific", "No", "Secondary effects approximate", mesh="Possible", pbr="BRDF fields", relight="Yes", edit="Yes", geom="Volumetric/surface constraints.", normal="Geometry-field normals.", mat="Reflectance and illumination tensors.", render="Physically based rendering with secondary effects.", loss="Photometric, material, light, geometry.", strengths="Efficient neural inverse rendering baseline.", author_lim="Not mesh/UV-native.", infer_lim="Not target asset format or mirror-focused.", evidence="CVPR abstract."),
    r("nvdiffrec: Extracting Triangular 3D Models, Materials, and Lighting From Images", 2022, "CVPR oral", "https://nvlabs.github.io/nvdiffrec/", "https://github.com/NVlabs/nvdiffrec", "Extract graphics-ready mesh/material/light.", "Posed images, masks, object-centric capture.", "Triangle mesh with PBR textures.", "Mesh + PBR", "Yes", "Moderate specular", "No", "No", "Yes", "Yes", "Yes", "Yes", "Yes", geom="Differentiable rasterization and masks.", normal="Mesh normals.", mat="SVBRDF/PBR texture optimization.", render="Rasterized PBR with split-sum environment lighting.", loss="Photometric, mask, regularization.", strengths="Strong target-output precedent.", author_lim="Needs good masks/capture; reflective ambiguity remains.", infer_lim="Hard reflective surfaces need additional reflection constraints.", evidence="CVPR project."),
    r("Stanford-ORB: A Real-World 3D Object Inverse Rendering Benchmark", 2023, "NeurIPS Datasets and Benchmarks", "https://stanfordorb.github.io/", "https://stanfordorb.github.io/", "Benchmark inverse rendering and relighting.", "Captured HDR object dataset.", "Dataset with images, meshes, lights.", "Dataset", "Contains specular materials", "Some shiny objects", "Captured light-box/HDR", "Physical but not isolated", "Provides meshes", "Reference assets", "Reference materials", "Evaluation", "No method", geom="Ground truth capture.", normal="GT/reference normals and meshes.", mat="Benchmark references.", render="Evaluation renderer.", loss="N/A", datasets="14 objects, HDR images, HDR env maps.", metrics="Depth, normal, shape, PSNR-H/L, SSIM, LPIPS.", strengths="Real benchmark for material/relighting.", author_lim="Limited object count.", infer_lim="May not stress near-field mirror objects enough.", evidence="Project page counts/metrics."),
    r("OpenIllumination: A Multi-Illumination Dataset for Inverse Rendering Evaluation on Real Objects", 2023, "NeurIPS Datasets and Benchmarks", "https://openreview.net/forum?id=pRnrg2bWr0", "https://oppo-us-research.github.io/OpenIllumination/", "Controlled multi-view multi-light benchmark.", "64 real objects with many views/lights.", "Dataset.", "Dataset", "Includes varied materials", "Some glossy/specular", "Controlled lighting", "Physical but not isolated", "Provides cameras/masks/lights", "No method", "Evaluation references", "Evaluation", "No method", geom="GT cameras/lights/masks.", normal="N/A.", mat="Benchmark setting.", render="Benchmark rendering/evaluation.", loss="N/A", datasets="108K+ images, 64 objects, 72 views, many illuminations.", metrics="Relighting/material/geometry metrics.", strengths="Strong controlled evaluation source.", author_lim="Controlled rig.", infer_lim="Not uncontrolled near-field mirror setting.", evidence="OpenReview abstract."),
    r("RAGS: Roughness-Aware Gaussian Splatting for Reflective Objects Surface Reconstruction", 2026, "Knowledge-Based Systems", "https://www.sciencedirect.com/science/article/pii/S0950705126005812", "", "Reflective object reconstruction with roughness-aware BRDF.", "Posed RGB reflective objects.", "3DGS with Ward BRDF and roughness.", "3DGS + BRDF", "Yes", "Glossy partial", "No explicit", "No", mesh="Surface likely", pbr="Roughness/material attributes", relight="Potential", edit="Potential", geom="Physically based geometry optimization.", normal="Gaussian/surface normals.", mat="Ward BRDF roughness prediction.", render="Differentiable rendering equation.", loss="RGB, roughness/material, geometry.", strengths="Recent explicit roughness-aware reflective GS.", author_lim="Full details require paper access.", infer_lim="Near-field/inter-reflection and UV baking not central.", evidence="ScienceDirect abstract snippet."),
    r("GIP-GS: Glossy Image Prior-guided Gaussian Splatting for Reflective Surface Reconstruction", 2026, "Neural Networks", "https://www.sciencedirect.com/science/article/pii/S0893608026001152", "", "Decouple geometry and appearance for glossy surfaces.", "Posed RGB; glossy-image prior.", "Two-stage PGSR-derived GS.", "3DGS/planar GS + prior", "Yes", "Glossy", "No explicit", "No", "Yes", geom="Glossy image prior and staged geometry/appearance separation.", normal="Geometry prior normals/depth.", mat="Appearance decoupling, not PBR maps.", render="Gaussian rasterization.", loss="RGB and prior-guided geometry/appearance.", strengths="Directly attacks entanglement.", author_lim="Full details require paper access.", infer_lim="No PBR UV asset; priors can fail on unusual reflections.", evidence="ScienceDirect abstract snippet."),
    r("RTR-GS: 3D Gaussian Splatting for Inverse Rendering with Radiance Transfer and Reflection", 2025, "ACM Multimedia", "https://arxiv.org/abs/2507.07733", "https://fanglue.github.io/papers/RTR_GS_MM.pdf", "Radiance-transfer and reflection-aware GS inverse rendering.", "Posed RGB.", "3DGS with radiance transfer, BRDF, lighting.", "3DGS + inverse rendering", "Yes", "No mirror-specific", "Unclear", "Secondary effects via radiance transfer", pbr="BRDF attributes", relight="Yes", edit="Yes", geom="Radiance-transfer constraints.", normal="Regularized Gaussian normals.", mat="BRDF and lighting decomposition.", render="Rasterization/ray-tracing hybrid radiance transfer.", loss="RGB, BRDF/light/radiance-transfer.", strengths="Stronger light transport than split-sum only.", author_lim="Not UV mesh-focused.", infer_lim="Near-field mirror geometry remains open.", evidence="arXiv abstract; ACM MM PDF."),
    r("Ref-DGS: Reflective Dual Gaussian Splatting", 2026, "arXiv preprint", "https://arxiv.org/abs/2603.07664", "project linked from arXiv", "Efficient near-field reflective rendering.", "Posed RGB reflective scenes.", "Geometry Gaussians plus local reflection Gaussians.", "Dual 3DGS", "Yes", "Reflective/glossy", "Yes", "No full multi-bounce", mesh="Surface reconstruction supported", geom="Decoupled surface/reflection representations.", normal="Geometry normals for reflection direction.", mat="Adaptive mixing shader, not PBR maps.", render="Rasterized dual GS with local/global reflection mixing.", loss="RGB, reflection mixing, geometry.", strengths="Near-field reflection without expensive ray tracing.", author_lim="Preprint; approximation depends on mixing.", infer_lim="No UV/PBR mesh asset or inter-reflection.", evidence="arXiv abstract."),
    r("RT-GS: Gaussian Splatting with Reflection and Transmittance Primitives", 2026, "arXiv preprint", "https://arxiv.org/abs/2604.00509", "", "Joint reflection and transmittance effects.", "Posed RGB with reflective/transparent effects.", "Separate reflection/transmittance primitives with ray tracing.", "3DGS + ray tracing + material", "Yes", "Specular partial", "Ray-traced", "Partial paths", mesh="Geometry possible", pbr="Microfacet attributes", relight="Potential", edit="Potential", geom="Ray-traced primitive constraints.", normal="Surface normals for microfacet reflection.", mat="Microfacet material model.", render="Ray tracing plus Gaussian primitives.", loss="RGB, primitive separation, material/geometry.", strengths="Explicit reflective and transparent transport.", author_lim="Higher cost and broader scope.", infer_lim="UV mesh/material baking absent.", evidence="arXiv abstract."),
    r("MSGS: Multi-space Gaussian Splatting for Mirror Reflections", 2026, "Computers and Graphics", "https://www.sciencedirect.com/science/article/abs/pii/S0097849326000555", "", "Mirror reflection view inconsistency in GS.", "Posed RGB mirror scenes.", "Multi-space GS with anisotropic features.", "3DGS + mirror/multi-space", "Yes", "Yes", "Mirror virtual objects", "Single-bounce mirror", edit="Maybe", geom="Mirror-space consistency.", normal="Mirror plane/space geometry.", render="Multi-space Gaussian rendering.", loss="Photometric and multi-space consistency.", strengths="Addresses virtual-object inconsistency.", author_lim="Mirror-scene assumptions.", infer_lim="Not curved reflective object material mapping.", evidence="ScienceDirect abstract snippet."),
    r("2D-SuGaR: 2D Gaussian Splatting for Surface-Aligned Mesh Extraction", 2025, "arXiv / project", "https://arxiv.org/search/?query=2D-SuGaR", "", "Mesh extraction with 2DGS/SuGaR ideas.", "Posed RGB/trained GS.", "2D surface splats plus mesh extraction.", "2DGS + mesh", mesh="Yes", geom="Surface alignment/depth fusion.", normal="2D disk/mesh normals.", render="2DGS rendering and mesh extraction.", loss="RGB, depth/normal, alignment.", strengths="Natural 2DGS mesh-extraction route.", author_lim="Exact paper details need verification.", infer_lim="Reflective material and UV/PBR outputs not addressed.", evidence="Web search follow-up; lower-confidence adjacent work."),
    r("Quadratic Gaussian Splatting: High Quality Surface Reconstruction with Second-order Geometric Prior", 2025, "ICCV", "https://openaccess.thecvf.com/content/ICCV2025/papers/Zhang_Quadratic_Gaussian_Splatting_High_Quality_Surface_Reconstruction_with_Second-order_Geometric_ICCV_2025_paper.pdf", "", "High-quality surface reconstruction with curvature prior.", "Posed RGB.", "Quadratic Gaussian local surface model.", "Surface Gaussians / second-order geometry", mesh="Yes", geom="Second-order geometry prior.", normal="Quadratic surface normals.", render="Gaussian rendering with local quadratic surface model.", loss="RGB and second-order geometry losses.", strengths="Improves local curvature beyond planar splats.", author_lim="Not material/reflection-aware.", infer_lim="Specular highlights remain unmodeled.", evidence="ICCV 2025 CVF PDF."),
]

with (OUT / "literature_matrix.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=COLS)
    writer.writeheader()
    writer.writerows(rows)

technical_review = """# Technical Review

## Local Paper Inventory

I inspected 31 local PDFs in `papers/`. The local set covers: surface reconstruction from Gaussian Splatting (2DGS, SuGaR, PGSR, GOF, SOF, 3DGSR, GS2Mesh, DN-Splatter, MILo, MGSR, geometry-field surfels), reflective/specular Gaussian Splatting (Reflective Gaussian Splatting, RefGaussian, Ref-GS, MaterialRefGS, PolGS, PolGS++, SSR-GS, SpecTRe-GS, GS-2DGS, IRGS, EnvGS, GlossyGS), inverse rendering/material routes (GeoSplatting, GS-2M, SSD-GS), and classical reflection theory (Specular Flow, Shape from Specular Flow, Neural Point Catacaustics, Deep Flow Rendering). Extracted abstracts and term-level snippets are cached at `outputs/_work/local_pdf_extracts.json`.

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
"""

gap_analysis = """# Research Gap Analysis

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
"""

proposed_method = """# Proposed Method: RefTex-GS

## A. Core Thesis

[HYPOTHESIS]: Highly reflective object reconstruction becomes better conditioned if the model does not ask one representation to explain both the reflector surface and the reflected world. RefTex-GS therefore optimizes a mesh-bound surface Gaussian representation, a UV-domain PBR material atlas, and a decomposed reflection field with explicit far-field, near-field, and residual inter-reflection terms.

## B. Problem Formulation

Inputs are calibrated images {I_i}, camera intrinsics K_i, camera poses T_i, and optional object masks M_i. The object is static, opaque, and may contain diffuse, glossy, and mirror-like regions. Unknowns are geometry G, surface normals n, UV atlas U, material maps A/R/M/N for albedo, roughness, metallic/specular, and normal detail, far-field illumination L_env, near-field reflection field F_nf, and residual inter-reflection field F_ir. Desired outputs are a triangle mesh, UV texture maps, PBR material maps, relightable renderer, and editable material parameters.

## C. Representation

Surface representation: a triangle mesh plus surface-bound 2D Gaussian surfels. Free 3D Gaussians are rejected because they can float toward reflected content. Pure SDF is rejected as the only representation because it is slower and less direct for UV baking.

Appearance representation: each Gaussian stores a pointer to mesh triangle barycentric coordinates and UV coordinates. Its diffuse color and PBR parameters are sampled from UV atlases. View-dependent residual color is allowed only through the reflection field, not through arbitrary SH color.

BRDF/PBR representation: Cook-Torrance microfacet BRDF with albedo a(u), roughness rho(u), metallic/specular m(u), and normal detail n_t(u). This addresses the lack of graphics-ready outputs in most GS inverse-rendering papers.

Reflection representation: L_env(w) handles far-field lighting; F_nf(x, w) stores local reflected radiance conditioned on surface position and reflection direction; F_ir(x, w) is a low-rank residual for multi-bounce effects. The near-field term is necessary because environment maps cannot explain reflected-object parallax.

## D. Full Pipeline

1. Data preprocessing: estimate masks, COLMAP poses if needed, coarse reflective-region scores from view-dependent residuals, and monocular/depth priors only as soft cues. Failure case: priors may misread mirror regions.

2. Initialization: train a conservative 2DGS/PGSR-style surface model, extract a coarse mesh, unwrap UVs, and initialize material maps from view-consistent diffuse observations. Failure case: mirror-only regions may lack diffuse observations.

3. Geometry estimation: optimize mesh vertices and surface-bound Gaussians using RGB, silhouette, depth-normal, and reflection-aware losses. The key is that reflective pixels are not forced to match diffuse texture.

4. Normal estimation: combine mesh normals, tangent-space normal atlas, Gaussian surfel normals, and reflection consistency. This reduces the normal-light ambiguity in low-roughness regions.

5. Reflective-region reasoning: estimate p_ref(u) from high view-dependent residual, polarization if available, and learned uncertainty. Reflective regions weight reflection losses upward and diffuse texture losses downward.

6. Material decomposition: optimize albedo/roughness/metallic maps with spatial smoothness and cross-view UV consistency. Roughness controls whether radiance should be explained by BRDF blur or reflection field.

7. Reflection modeling: render far-field specular from L_env, near-field from F_nf by reflected-ray queries, and inter-reflection residual from F_ir with low rank and energy penalties.

8. Mesh extraction/refinement: use the live mesh as the final surface; refine vertices under normal, silhouette, and reflection-motion constraints rather than extracting a mesh only after training.

9. UV texture/material baking: bake diffuse and PBR maps by minimizing consistency between Gaussian samples and UV texels under held-out views. Seam consistency is enforced across duplicated UV islands.

10. Relighting/material editing: replace L_env and optionally edit UV material maps; keep F_nf disabled for pure relighting or re-estimate it for captured local environments.

11. Inference-time rendering: rasterize mesh/surface Gaussians for visibility and evaluate PBR shading plus optional reflection-field residual.

## E. Mathematical Formulation

Camera ray: r_i(p,t)=o_i+t d_i(p), with d_i(p)=R_i K_i^{-1}[p_x,p_y,1]^T.

Surface intersection: x=s(r_i)=argmin_x d(x,G)=0 along the ray, approximated by rasterized mesh/surface-Gaussian visibility.

Surface normal: n(x)=normalize(n_mesh(x)+T(u)n_t(u)), where u=UV(x).

Reflection direction: omega_r=2(n dot omega_o)n-omega_o, with omega_o=-d_i(p).

PBR rendering: C_pbr=integral f_r(a,rho,m,n,omega_i,omega_o)L(omega_i)V(x,omega_i)(n dot omega_i)_+ d omega_i.

Gaussian component: C_g(p)=sum_k alpha_k(p) prod_{j<k}(1-alpha_j(p)) C_k, where C_k is sampled from UV material and reflection terms rather than arbitrary SH color.

Reflection decomposition: L(x,omega_r)=L_env(omega_r)+F_nf(x,omega_r)+F_ir(x,omega_r).

Reflection consistency loss: L_ref=sum_{i,p} p_ref(u)||I_i(p)-R(G,U,L_env,F_nf,F_ir)_i(p)||_1 + lambda_flow ||Pi_j(x')-p'_j||_1. The second term checks that a reflected ray predicted from view i lands at a consistent image location in nearby views. It uses poses, normals, and a local reflection-field proxy. It reduces the ambiguity between moving highlights and static texture. Failure case: unobserved reflected content gives weak correspondence.

Geometry regularization: L_geo=lambda_lap||Delta V||^2 + lambda_sil L_sil + lambda_dn||n_mesh-n_gauss||_1. It stabilizes the mesh and keeps Gaussians surface-bound. Failure case: over-smoothing sharp metal edges.

Normal consistency loss: L_n=sum||n_mesh(x_k)-n_gauss,k||_1 + p_ref||omega_r(n_mesh)-omega_r(n_tex)||_1. It directly penalizes inconsistent reflection directions.

Material consistency loss: L_mat=sum_{views of u} w_diff||a(u)-a_i^obs(u)||_1 + lambda_tv TV(a,rho,m). It uses only low-reflection observations for diffuse color. It reduces texture/specular leakage. Failure case: regions visible only as mirror reflection.

UV baking loss: L_uv=sum_k||theta_k - theta(UV(x_k))||_1 + lambda_seam||theta(u_a)-theta(u_b)||_1 for duplicated seam texels. It transfers Gaussian material estimates into texture maps.

Full objective: L=L_rgb+L_ref+L_geo+L_n+L_mat+L_uv+L_light+L_sparse, optimizing mesh vertices V, Gaussian surfel parameters, UV material maps, L_env, F_nf, F_ir, and reflective-region logits.

## F. Novelty Analysis

Compared with GS-IR, our method differs in: surface-bound Gaussians instead of free material Gaussians; explicit near-field reflection field; final UV PBR baking. This matters because GS-IR approximates normals/occlusion but does not output mesh-bound texture assets.

Compared with GeoSplatting, our method differs in: reflection-region reasoning, near-field reflection field, and UV atlas consistency during optimization. This matters because mesh-guided PBR alone still assumes reflected illumination can be represented mostly by environment/visibility.

Compared with Reflective Gaussian Splatting, our method differs in: a live mesh+UV asset representation, explicit texture baking losses, and separated far-field/near-field/residual reflection terms. This matters because rendering/editing outputs are not the same as a graphics-ready PBR asset.

Compared with GS-2M, our method differs in: reflective-region gating and near-field/inter-reflection consistency objectives, not only joint mesh/material decomposition. This matters because material roughness alone cannot explain reflected-object parallax.

Compared with SpecTRe-GS or Ref-DGS, our method differs in: reflection modeling is tied to UV PBR material extraction rather than primarily novel-view rendering, and the reflection residual is regularized not to become arbitrary view-dependent color. This matters because the final output must remain editable.

Closest prior works: GS-IR, GeoSplatting, Reflective Gaussian Splatting, GS-2M, SpecTRe-GS, Ref-DGS, PolGS/NeRSP, nvdiffrec.

Potential overlap: recent 2026 reflective GS papers may contain partial near-field reflection fields or roughness-aware geometry losses.

Actual difference: RefTex-GS makes the mesh+UV PBR atlas a first-class optimization variable and uses reflection consistency to decide which pixels supervise texture versus reflection field.

Remaining novelty risk: if a concurrent reflective-GS paper already optimizes UV PBR maps with near-field reflection decomposition, the claim narrows to the specific reflection-consistency and baking formulation.

## G. Why This Can Work

[HYPOTHESIS]: The added constraint is that reflected radiance must move according to a normal-induced reflection direction, while diffuse texture must remain fixed in UV space. Under static-object and calibrated-camera assumptions, this separates two different motion models. The optimization is expected to be more stable than free view-dependent color because low-roughness regions are routed to reflection losses and diffuse UV losses are downweighted there. When assumptions are violated, such as moving reflected objects or unmodeled transparent layers, the residual field may absorb errors and should be flagged by high uncertainty.

## H. Expected Contributions

1. A mesh-bound Gaussian inverse-rendering representation that jointly optimizes surface geometry, UV-domain PBR maps, and decomposed reflection fields for highly reflective objects.

2. A reflection-consistency objective that uses predicted normals and multiview reflected-ray motion to reduce geometry-texture-reflection ambiguity.

3. A reflective-region-aware UV baking strategy that prevents specular and mirror-like content from leaking into diffuse texture maps.

4. An evaluation protocol that reports mesh, normal, material, UV texture, relighting, and reflective-region metrics separately.
"""

experiments = """# Experiments

## Datasets

Synthetic: Blender/Cycles scenes with chrome, brushed metal, glossy ceramic, black plastic, planar mirrors, curved mirrors, and nearby colored objects. Render ground-truth mesh, normals, albedo, roughness, metallic/specular, HDR lighting, reflection-region masks, and inter-reflection masks.

Real controlled: Stanford-ORB and OpenIllumination for relighting/material evaluation; add a small captured set with turntable objects, chrome spheres, metal utensils, phone backs, watch cases, and glossy ceramic objects. Capture HDR environment probes and optional cross-polarized references for analysis.

Real in-the-wild: reflective tabletop objects with COLMAP poses and masks, used for qualitative and robustness evaluation.

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
"""

paper_story = """# Paper Story

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
"""

terminology = """# Terminology Checklist

Reflective surface: A surface whose observed radiance contains a significant view-dependent reflected component. Use as the umbrella term; do not use it interchangeably with mirror-like.

Specular reflection: Directional reflection described by a BRDF lobe. Use for both glossy and sharp components; do not equate it with perfect mirror reflection.

Mirror-like reflection: Very low-roughness reflection with sharp reflected structure. Use only for near-delta specular behavior.

Glossy reflection: Specular reflection with finite roughness and blurred reflected structure. Do not use it for perfect mirrors.

View-dependent appearance: Any appearance changing with viewing direction. This includes specular reflection but can also be non-physical learned color; do not treat it as material decomposition.

Material decomposition: Estimating surface material parameters such as albedo, roughness, metallic/specular, and normal detail. Do not use it for arbitrary latent appearance splitting.

Texture mapping: Assigning surface properties to a 2D UV atlas on a mesh. Do not use it for per-Gaussian color storage.

PBR material: A physically based rendering parameter set, here albedo, roughness, metallic/specular, and normal map. Do not call SH color a PBR material.

UV texture map: A 2D image indexed by mesh UV coordinates. Do not use it interchangeably with neural texture or per-point color.

Surface-bound Gaussian: A Gaussian primitive constrained to a mesh point or surface parameterization. Do not use it for free-floating 3D Gaussians.

Reflection field: A function returning reflected radiance conditioned on position and direction. Do not use it for generic view-dependent color unless the reflection-direction relationship is enforced.

Near-field reflection: Reflection of nearby scene content whose appearance depends on reflector position, not only direction. Do not model it only as an environment map.

Inter-reflection: Light reflected between surfaces one or more additional times. Do not use it for single-bounce mirror reflection.

Mesh reconstruction: Recovering a triangle surface with accurate geometry and normals. Do not equate it with high PSNR novel-view rendering.

Relighting: Rendering the recovered asset under changed illumination. Do not call view synthesis relighting unless lighting changes.
"""

(OUT / "technical_review.md").write_text(technical_review, encoding="utf-8")
(OUT / "research_gap_analysis.md").write_text(gap_analysis, encoding="utf-8")
(OUT / "proposed_method.md").write_text(proposed_method, encoding="utf-8")
(OUT / "experiments.md").write_text(experiments, encoding="utf-8")
(OUT / "paper_story.md").write_text(paper_story, encoding="utf-8")
(OUT / "terminology_checklist.md").write_text(terminology, encoding="utf-8")

print(f"wrote {len(rows)} literature rows and 6 markdown reports")
