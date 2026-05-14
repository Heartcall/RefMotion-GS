# Local Paper Inventory

This appendix records the 31 PDFs inspected from `papers/`. Abstracts are extracted from the local PDFs when available; method summaries and key claims are normalized against `outputs/literature_matrix.csv`.

## 1. Ref-GS: Directional Factorization for 2D Gaussian Splatting

- File: `2D Gaussian Splatting for Geometrically Accurate Radiance Fields.pdf`
- Year: 2025
- Venue/status: arXiv preprint
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: 2D Gaussian Splatting for Geometrically Accurate Radiance Fields BINBIN HUANG, ShanghaiTech University, China ZEHAO YU, University of Tübingen Tübingen AI Center, Germany ANPEI CHEN, University of Tübingen Tübingen AI Center, Germany ANDREAS GEIGER, University of Tübingen Tübingen AI Center, Germany SHENGHUA GAO, ShanghaiTech University, China https://surfsplatting.github.io Mesh Radiance fieldDisk (color) Disk (normal)Surface normal (a) 2D disks as surface elements(b) 2D Gaussian splatting(c) Meshing Fig. 1. Our method, 2DGS, (a) optimizes a set of 2D oriented disks to represent and reconstruct a complex real-world scene from multi-view RGB images. These optimized 2D disks are tightly aligned to the surfaces. (b) With 2D Gaussian splatting, we allow real-time rendering of high quality novel view images with view consistent normals and depth maps. (c) Finally, our method provides detaile
- Method summary: 2DGS with directional appearance factorization.; 2DGS rasterization.
- Key claim / relevance: Improves view-dependent effects on surface splats. Limitation: Directional appearance alone cannot infer PBR maps or near-field reflection.

## 2. 3D Gaussian Splatting with Self-Constrained Priors for High Fidelity Surface Reconstruction

- File: `3D Gaussian Splatting with Self-Constrained Priors for High Fidelity Surface Reconstruction.pdf`
- Year: 2025
- Venue/status: arXiv preprint
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: Rendering 3D surfaces has been revolutionized within the modeling of radiance fields through either 3DGS or NeRF . Although 3DGS has shown advantages over NeRF in terms of rendering quality or speed, there is still room for im- provement in recovering high fidelity surfaces through 3DGS. To resolve this issue, we propose a self-constrained prior to constrain the learning of 3D Gaussians, aiming for more accurate depth rendering. Our self-constrained prior is derived from a TSDF grid that is obtained by fusing the depth maps rendered with current 3D Gaussians. The prior measures a distance field around the estimated sur- face, offering a band centered at the surface for imposing more specific constraints on 3D Gaussians, such as remov- ing Gaussians outside the band, moving Gaussians closer to the surface, and encouraging larger or smaller opac- ity in a geometry-aware manner. More import
- Method summary: 3DGS with self-constrained geometry priors.; Differentiable image rendering
- Key claim / relevance: Reduces geometry noise without extra sensors. Limitation: Reflective surfaces remain underconstrained because reflection transport is not modeled.

## 3. 3D Gaussian Splatting with Self-Constrained Priors for High Fidelity Surface Reconstruction

- File: `3DGSR Implicit Surface Reconstruction with 3D Gaussian Splatting.pdf`
- Year: 2025
- Venue/status: arXiv preprint
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: 3DGSR: Implicit Surface Reconstruction with 3D Gaussian Splatting XIAOYANG LYU,The University of Hong Kong, Hong Kong YANG-TIAN SUN,The University of Hong Kong, Hong Kong YI-HUA HUANG, The University of Hong Kong, Hong Kong XIUZHE WU, The University of Hong Kong, Hong Kong ZIYI YANG, The University of Hong Kong, Hong Kong YILUN CHEN, Shanghai AI Lab, China JIANGMIAO PANG, Shanghai AI Lab, China XIAOJUAN QI∗, The University of Hong Kong, Hong Kong Rendered Image Rendered Normal Ours 2DGS Relightable-GS Rendered Depth Fig. 1. Our method, called 3DGSR, achieves accurate 3D surface reconstruction with rich details while maintaining the efficiency and high-quality rendering of 3DGS. The left part shows the capability of our method to achieve high-quality reconstruction and rendering results simultaneously. 2DGS [Huang et al. 2024] is the state-of-the-art Gaussian-based reconstruction method.
- Method summary: 3DGS with self-constrained geometry priors.; Differentiable image rendering
- Key claim / relevance: Reduces geometry noise without extra sensors. Limitation: Reflective surfaces remain underconstrained because reflection transport is not modeled.

## 4. Toward a Theory of Shape from Specular Flow

- File: `Adato 等 - 2007 - Toward a Theory of Shape from Specular Flow.pdf`
- Year: 2007
- Venue/status: Vision theory paper
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: The image of a curved, specular (mirror-like) surface is a distorted re ﬂection of the environment. The goal of our work is to develop a framework for recovering general shape from such distortions when the environment is nei- ther calibrated nor known. T o achieve this goal we con- sider far- ﬁeld illumination, where the object-environment distance is relatively large, and we examine the dense spec- ular ﬂow that is induced on the image plane through rela- tive object-environment motion. W e show that under these very practical conditions the observed specular ﬂow can be related to surface shape through a pair of coupled non- linear partial differential equations. Importantly, this rela- tionship depends only on the environment’s relative motion and not its content. W e examine the qualitative properties of these equations, present analytic methods for recovery of the shape in several s
- Method summary: Differential specular geometry.; Analytic mirror reflection geometry.
- Key claim / relevance: Shows reflections contain shape information. Limitation: Hard to use directly for uncontrolled posed RGB captures.

## 5. Eurographics Symposium on Rendering 2022 A. Ghosh and L.-Y . Wei (Guest Editors) Volume 41 (2022), Number 4

- File: `Dai和Xie - 2022 - Deep Flow Rendering View Synthesis via Layer-aware Reflection Flow.pdf`
- Year: 2022
- Venue/status: Unknown / local PDF
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: Novel view synthesis (NVS) generates images from unseen viewpoints based on a set of input images. It is a challenge because of inaccurate lighting optimization and geometry inference. Although current neural rendering methods have made significant progress, they still struggle to reconstruct global illumination effects like reflections and exhibit ambiguous blurs in highly view- dependent areas. This work addresses high-quality view synthesis to emphasize reflection on non-concave surfaces. We propose Deep Flow Rendering that optimizes direct and indirect lighting separately, leveraging texture mapping, appearance flow, and neural rendering. A learnable texture is used to predict view-independent features, meanwhile enabling efficient reflection extraction. To accurately fit view-dependent effects, we adopt a constrained neural flow to transfer image-space features from nearby views to 
- Method summary: See local PDF; 
- Key claim / relevance: Relevant local reference Limitation: Requires manual reading for details.

## 6. DN-Splatter: Depth and Normal Priors for Gaussian Splatting and Meshing Matias Turkulainen∗1 Xuqian Ren∗2 Iaroslav Melekhov3 Otto Seiskari4 Esa Rahtu2 Juho Kannala3,4

- File: `DN-Splatter - Depth and Normal Priors for Gaussian Splatting and Meshing.pdf`
- Year: Unknown
- Venue/status: Unknown / local PDF
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: High-fidelity 3D reconstruction of common indoor scenes is crucial for VR and AR applications. 3D Gaussian splat- ting, a novel differentiable rendering technique, has achieved state-of-the-art novel view synthesis results with high ren- dering speeds and relatively low training times. However, its performance on scenes commonly seen in indoor datasets is poor due to the lack of geometric constraints during op- timization. In this work, we explore the use of readily ac- cessible geometric cues to enhance Gaussian splatting op- timization in challenging, ill-posed, and textureless scenes. We extend 3D Gaussian splatting with depth and normal cues to tackle challenging indoor datasets and showcase techniques for efficient mesh extraction. Specifically, we regularize the optimization procedure with depth informa- tion, enforce local smoothness of nearby Gaussians, and use off-the-shelf mono
- Method summary: See local PDF; 
- Key claim / relevance: Relevant local reference Limitation: Requires manual reading for details.

## 7. EnvGS: Modeling View-Dependent Appearance with Environment Gaussian

- File: `EnvGS Modeling View-Dependent Appearance with Environment Gaussian.pdf`
- Year: 2025
- Venue/status: arXiv preprint
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: Reconstructing complex reflections in real-world scenes from 2D images is essential for achieving photorealistic novel view synthesis. Existing methods that utilize environ- ment maps to model reflections from distant lighting often struggle with high-frequency reflection details and fail to account for near-field reflections. In this work, we introduce EnvGS, a novel approach that employs a set of Gaussian primitives as an explicit 3D representation for capturing reflections of environments. These environment Gaussian primitives are incorporated with base Gaussian primitives to model the appearance of the whole scene. To efficiently render these environment Gaussian primitives, we devel- oped a ray-tracing-based renderer that leverages the GPU’s RT core for fast rendering. This allows us to jointly optimize our model for high-quality reconstruction while maintain- * Equal Contribution. 
- Method summary: 3DGS plus environment Gaussian appearance.; Gaussian rasterization with environment appearance.
- Key claim / relevance: Efficient view-dependent rendering. Limitation: Near-field reflected objects and PBR maps are not explicit.

## 8. SSR-GS: Separating Specular Reflection in Gaussian Splatting for Glossy Surface Reconstruction Ningjing Fan1 and Yiqun Wang1∗

- File: `Fan和Wang - 2026 - SSR-GS Separating Specular Reflection in Gaussian Splatting for Glossy Surface Reconstruction.pdf`
- Year: 2026
- Venue/status: Unknown / local PDF
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: .In recent years, 3D Gaussian splatting (3DGS) has achieved remarkable progress in novel view synthesis. However, accurately recon- structingglossysurfacesundercomplexilluminationremainschallenging, particularly in scenes with strong specular reflections and multi-surface interreflections. To address this issue, we propose SSR-GS, a specular reflection modeling framework for glossy surface reconstruction. Specif- ically, we introduce a prefiltered Mip-Cubemap to model direct spec- ular reflections efficiently, and propose an IndiASG module to capture indirect specular reflections. Furthermore, we design Visual Geometry Priors (VGP) that couple a reflection-aware visual prior via a reflection score (RS) to downweight the photometric loss contribution of reflection- dominated regions, with geometry priors derived from VGGT, including progressively decayed depth supervision and transformed 
- Method summary: See local PDF; 
- Key claim / relevance: Relevant local reference Limitation: Requires manual reading for details.

## 9. Gaussian Opacity Fields: Efficient Adaptive Surface Reconstruction in Unbounded Scenes Fig. 1. Applying TSDF fusion with rendered depth maps from the state-of-the-art Mip-Splatting [Yu et al. 2024a] models results in noisy and incomplete

- File: `Gaussian Opacity Fields Efficient and Compact Surface Reconstruction in Unbounded Scenes.pdf`
- Year: Unknown
- Venue/status: Unknown / local PDF
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: Gaussian Opacity Fields: Efficient Adaptive Surface Reconstruction in Unbounded Scenes ZEHAO YU, University of Tübingen, Tübingen AI Center, Germany TORSTEN SATTLER, Czech Technical University in Prague, Czech Republic ANDREAS GEIGER, University of Tübingen, Tübingen AI Center, Germany https://niujinshuchong.github.io/gaussian-opacity-fields Fig. 1. Applying TSDF fusion with rendered depth maps from the state-of-the-art Mip-Splatting [Yu et al. 2024a] models results in noisy and incomplete meshes, while meshes extracted with our method are complete, smooth, and detailed. This is achieved by establishing Gaussian opacity fields from 3D Gaussians, which enables geometry extraction by directly identifying its level-set. Moreover, we generate tetrahedral meshes from 3D Gaussians and utilize Marching Tetrahedra to extract adaptive and compact meshes. Recently, 3D Gaussian Splatting (3DGS) has
- Method summary: See local PDF; 
- Key claim / relevance: Relevant local reference Limitation: Requires manual reading for details.

## 10. Geometry Field Splatting with Gaussian Surfels Kaiwen Jiang1 Venkataram Sivaram1 Cheng Peng2 Ravi Ramamoorthi1

- File: `Geometry Field Splatting with Gaussian Surfels.pdf`
- Year: Unknown
- Venue/status: Unknown / local PDF
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: Geometric reconstruction of opaque surfaces from im- ages is a longstanding challenge in computer vision, with renewed interest from volumetric view synthesis algorithms using radiance fields. We leverage the geometry field pro- posed in recent work for stochastic opaque surfaces, which can then be converted to volume densities. We adapt Gaus- sian kernels or surfels to splat the geometry field rather than the volume, enabling precise reconstruction of opaque solids. Our first contribution is to derive an efficient and almost exact differentiable rendering algorithm for geometry fields parameterized by Gaussian surfels, while removing current approximations involving Taylor series and no self- attenuation. Next, we address the discontinuous loss land- scape when surfels cluster near geometry, showing how to guarantee that the rendered color is a continuous function of the colors of the k
- Method summary: See local PDF; 
- Key claim / relevance: Relevant local reference Limitation: Requires manual reading for details.

## 11. GeoSplatting: Towards Geometry Guided Gaussian Splatting for Physically-based Inverse Rendering Kai Ye1,∗, Chong Gao 2,∗, Guanbin Li 2, Wenzheng Chen 3,4,†, Baoquan Chen 1,5,† Multi-view Inputs

- File: `GeoSplatting Towards Geometry Guided Gaussian Splatting for Physically-based Inverse Rendering.pdf`
- Year: Unknown
- Venue/status: Unknown / local PDF
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: Recent 3D Gaussian Splatting (3DGS) representations [22] have demonstrated remarkable performance in novel view synthesis; further, material-lighting disentanglement on 3DGS warrants relighting capabilities and its adaptability to broader applications. While the general approach to the latter operation lies in integrating differentiable physically- based rendering (PBR) techniques to jointly recover BRDF materials and environment lighting, achieving a precise dis- entanglement remains an inherently difficult task due to the challenge of accurately modeling light transport. Ex- isting approaches typically approximate Gaussian points’ *Equal contribution. †Equal advisory. normals, which constitute an implicit geometric constraint. However, they usually suffer from inaccuracies in normal estimation that subsequently degrade light transport, re- sulting in noisy material decomposition and fl
- Method summary: See local PDF; 
- Key claim / relevance: Relevant local reference Limitation: Requires manual reading for details.

## 12. 3D Gaussian Splatting with Self-Constrained Priors for High Fidelity Surface Reconstruction

- File: `GlossyGS Inverse Rendering of Glossy Objects.pdf`
- Year: 2025
- Venue/status: arXiv preprint
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: —Reconstructing objects from posed images is a crucial and complex task in computer graphics and computer vision. While NeRF-based neural reconstruction methods have exhibited impressive reconstruction ability, they tend to be time-comsuming. Recent strategies have adopted 3D Gaussian Splatting (3D-GS) for inverse rendering, which have led to quick and effective outcomes. However, these techniques generally have difficulty in producing believable geometries and materials for glossy objects, a challenge that stems from the inherent ambigui- ties of inverse rendering. To address this, we introduce GlossyGS, an innovative 3D-GS-based inverse rendering framework that aims to precisely reconstruct the geometry and materials of glossy objects by integrating material priors. The key idea is the use of micro-facet geometry segmentation prior, which helps to reduce the intrinsic ambiguities and i
- Method summary: 3DGS with self-constrained geometry priors.; Differentiable image rendering
- Key claim / relevance: Reduces geometry noise without extra sensors. Limitation: Reflective surfaces remain underconstrained because reflection transport is not modeled.

## 13. GS-2DGS: Geometrically Supervised 2DGS for Reflective Object Reconstruction

- File: `GS-2DGS Geometrically Supervised 2DGS for Reflective Object Reconstruction.pdf`
- Year: 2025
- Venue/status: arXiv preprint
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: 3D modeling of highly reflective objects remains chal- lenging due to strong view-dependent appearances. While previous SDF-based methods can recover high-quality meshes, they are often time-consuming and tend to produce over-smoothed surfaces. In contrast, 3D Gaussian Splat- ting (3DGS) offers the advantage of high speed and de- tailed real-time rendering, but extracting surfaces from the Gaussians can be noisy due to the lack of geometric con- straints. To bridge the gap between these approaches, we propose a novel reconstruction method called GS-2DGS for reflective objects based on 2D Gaussian Splatting (2DGS). Our approach combines the rapid rendering capabilities of Gaussian Splatting with additional geometric information from foundation models. Experimental results on synthetic and real datasets demonstrate that our method significantly outperforms Gaussian-based techniques in term
- Method summary: 2DGS with geometric supervision.; 2DGS rasterization.
- Key claim / relevance: Combines reflective target with surface primitive. Limitation: PBR/UV mapping and near-field reflection remain open.

## 14. GS-2M: Gaussian Splatting for Joint Mesh Reconstruction and Material Decomposition D. M. Nguyen1 , M. Avenhaus2

- File: `GS-2M Gaussian Splatting for Joint.pdf`
- Year: Unknown
- Venue/status: Unknown / local PDF
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: We propose a unified solution for mesh reconstruction and material decomposition from multi-view images based on 3D Gaus- sian Splatting, referred to as GS-2M. Previous works handle these tasks separately and struggle to reconstruct highly reflective surfaces, often relying on priors from external models to enhance the decomposition results. Conversely, our method addresses these two problems by jointly optimizing attributes relevant to the quality of rendered depth and normals, maintaining geometric details while being resilient to reflective surfaces. Although contemporary works effectively solve these tasks together, they often employ sophisticated neural components to learn scene properties, which hinders their performance at scale. To further elimi- nate these neural components, we propose a novel roughness supervision strategy based on multi-view photometric variation. When combine
- Method summary: See local PDF; 
- Key claim / relevance: Relevant local reference Limitation: Requires manual reading for details.

## 15. GS2Mesh: Surface Reconstruction from Gaussian Splatting via Novel Stereo Views Yaniv Wolf∗, Amit Bracha∗, and Ron Kimmel SuGaR (2H)

- File: `GS2Mesh Surface Reconstruction from Gaussian.pdf`
- Year: Unknown
- Venue/status: Unknown / local PDF
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: . Recently, 3D Gaussian Splatting (3DGS) has emerged as an efficient approach for accurately representing scenes. However, despite its superior novel view synthesis capabilities, extracting the geometry of the scene directly from the Gaussian properties remains a challenge, as those are optimized based on a photometric loss. While some concur- rent models have tried adding geometric constraints during the Gaussian optimization process, they still produce noisy, unrealistic surfaces. We propose a novel approach for bridging the gap between the noisy 3DGS representation and the smooth 3D mesh representation, by inject- ing real-world knowledge into the depth extraction process. Instead of ex- tracting the geometry of the scene directly from the Gaussian properties, we instead extract the geometry through a pre-trained stereo-matching model. We render stereo-aligned pairs of images correspo
- Method summary: See local PDF; 
- Key claim / relevance: Relevant local reference Limitation: Requires manual reading for details.

## 16. PolGS: Polarimetric Gaussian Splatting for Fast Reflective Surface Reconstruction Yufei Han1, Bowen Tie1, Heng Guo1,2∗, Youwei Lyu1, Si Li1∗, Boxin Shi3,4, Yunpeng Jia1, Zhanyu Ma1 0.2 0.4 1 2 4 8 10

- File: `Han 等 - 2025 - PolGS Polarimetric Gaussian Splatting for Fast Reflective Surface Reconstruction.pdf`
- Year: 2025
- Venue/status: Unknown / local PDF
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: Efficient shape reconstruction for surfaces with complex reflectance properties is crucial for real-time virtual re- ality. While 3D Gaussian Splatting (3DGS)-based meth- ods offer fast novel view rendering by leveraging their ex- plicit surface representation, their reconstruction quality lags behind that of implicit neural representations, partic- ularly in the case of recovering surfaces with complex re- flective reflectance. To address these problems, we propose PolGS, a Polarimetric Gaussian Splatting model allowing fast reflective surface reconstruction in 10 minutes. By inte- grating polarimetric constraints into the 3DGS framework, PolGS effectively separates specular and diffuse compo- nents, enhancing reconstruction quality for challenging re- flective materials. Experimental results on the synthetic and real-world dataset validate the effectiveness of our method. Project page:
- Method summary: See local PDF; 
- Key claim / relevance: Relevant local reference Limitation: Requires manual reading for details.

## 17. PolGS++: Physically-Guided Polarimetric Gaussian Splatting for Fast Reflective Surface Reconstruction

- File: `Han 等 - 2026 - PolGS++ Physically-Guided Polarimetric Gaussian Splatting for Fast Reflective Surface Reconstructio.pdf`
- Year: 2026
- Venue/status: preprint / manuscript
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: Accurate reconstruction of reflective surfaces re- mains a fundamental challenge in computer vision, with broad applications in real-time virtual reality and digital content creation. Although 3D Gaussian Splatting (3DGS) enables efficient novel-view rendering with explicit repre- sentations, its performance on reflective surfaces still lags behind implicit neural methods, especially in recovering fine geometry and surface normals. To address this gap, we pro- pose PolGS++, a physically-guided polarimetric Gaussian Splatting framework for fast reflective surface reconstruction. Specifically, we integrate a polarized BRDF (pBRDF) model into 3DGS to explicitly decouple diffuse and specular com- ponents, providing physically grounded reflectance modeling and stronger geometric cues for reflective surface recovery. Furthermore, we introduce adepth-guided visibility mask Corresponding author:
- Method summary: 3DGS plus physical polarimetric model.; Gaussian rasterization and polarization model.
- Key claim / relevance: Stronger physics than RGB-only. Limitation: Cannot address ordinary RGB capture and UV baking alone.

## 18. IRGS: Inter-Reflective Gaussian Splatting with 2D Gaussian Ray Tracing

- File: `IRGS Inter-Reflective Gaussian Splatting with 2D Gaussian Ray Tracing.pdf`
- Year: 2025
- Venue/status: arXiv preprint
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: In inverse rendering, accurately modeling visibility and indirect radiance for incident light is essential for cap- turing secondary effects. Due to the absence of a pow- erful Gaussian ray tracer, previous 3DGS-based methods have either adopted a simplified rendering equation or used learnable parameters to approximate incident light, result- ing in inaccurate material and lighting estimations. To this end, we introduce inter-reflective Gaussian splatting (IRGS) for inverse rendering. To capture inter-reflection, we apply the full rendering equation without simplification and compute incident radiance on the fly using the pro- posed differentiable 2D Gaussian ray tracing . Addition- ally, we present an efficient optimization scheme to handle the computational demands of Monte Carlo sampling for rendering equation evaluation. Furthermore, we introduce a novel strategy for querying the in
- Method summary: 2D Gaussians with ray tracing.; 2D Gaussian ray tracing plus rasterization.
- Key claim / relevance: Directly targets inter-reflection. Limitation: UV/PBR baking and stable optimization remain open.

## 19. Neural Point Catacaustics for Novel-View Synthesis of Reflections GEORGIOS KOPANAS, Inria & Université Côte d’Azur, France THOMAS LEIMKÜHLER, Max-Planck-Institut für Informatik, Germany

- File: `Kopanas 等 - 2022 - Neural Point Catacaustics for Novel-View Synthesis of Reflections.pdf`
- Year: 2022
- Venue/status: Unknown / local PDF
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: Neural Point Catacaustics for Novel-View Synthesis of Reflections GEORGIOS KOPANAS, Inria & Université Côte d’Azur, France THOMAS LEIMKÜHLER, Max-Planck-Institut für Informatik, Germany GILLES RAINER, Inria & Université Côte d’Azur, France CLÉMENT JAMBON, Inria & Université Côte d’Azur and Ecole Polytechnique, France GEORGE DRETTAKIS, Inria & Université Côte d’Azur, France Primary Point Cloud Reflection Point Cloud Point Rasterization & Neural Rendering Point-based Representation and Rendering Image Novel-view Synthesis Ours Ground Truth Mip-NeRF Neural Warp Field Applications Reflection Edits Refl. Tracking Stereo Comfort Object Cloning Fig. 1. We propose a method to perform novel-view synthesis of curved reflectors. We employ a dynamic point-based scene representation that allows to model catacaustic trajectories of reflections for accurate reflection flow estimation. Our approach outp
- Method summary: See local PDF; 
- Key claim / relevance: Relevant local reference Limitation: Requires manual reading for details.

## 20. MaterialRefGS: Reflective Gaussian Splatting with Multi-view Consistent Material Inference Wenyuan Zhang1∗ Jimin Tang1∗ Weiqi Zhang1 Yi Fang2 Yu-Shen Liu1† Zhizhong Han3

- File: `MaterialRefGS Reflective Gaussian Splatting with.pdf`
- Year: Unknown
- Venue/status: Unknown / local PDF
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: Modeling reflections from 2D images is essential for photorealistic rendering and novel view synthesis. Recent approaches enhance Gaussian primitives with reflection-related material attributes to enable physically based rendering (PBR) with Gaussian Splatting. However, the material inference often lacks sufficient constraints, especially under limited environment modeling, resulting in illumi- nation aliasing and reduced generalization. In this work, we revisit the problem from a multi-view perspective and show that multi-view consistent material in- ference with more physically-based environment modeling is key to learning accurate reflections with Gaussian Splatting. To this end, we enforce 2D Gaus- sians to produce multi-view consistent material maps during deferred shading. We also track photometric variations across views to identify highly reflective regions, which serve as strong
- Method summary: See local PDF; 
- Key claim / relevance: Relevant local reference Limitation: Requires manual reading for details.

## 21. MILo: Mesh-In-the-Loop Gaussian Splatting for Detailed and Efficient Surface Reconstruction ANTOINE GUÉDON∗ and DIEGO GOMEZ∗,École Polytechnique, France NISSIM MARUANI,Inria, Université Côte d’Azur, France

- File: `MILo Mesh-In-the-Loop Gaussian Splatting for Detailed and Efficient Surface Reconstruction.pdf`
- Year: Unknown
- Venue/status: Unknown / local PDF
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: MILo: Mesh-In-the-Loop Gaussian Splatting for Detailed and Efficient Surface Reconstruction ANTOINE GUÉDON∗ and DIEGO GOMEZ∗,École Polytechnique, France NISSIM MARUANI,Inria, Université Côte d’Azur, France BINGCHEN GONG,École Polytechnique, France GEORGE DRETTAKIS,Inria, Université Côte d’Azur, France MAKS OVSJANIKOV,École Polytechnique, France Ours - 302 MB RaDe-GS - 2.2 GB Ours - F1↑ 0.76 GOF - F1↑ 0.68 Ours - Mesh Ours - Render Ours - Mesh Ours - Render Fig. 1.Mesh-in-the-Loop Gaussian Splatting.Our method introduces a novel differentiable mesh extraction framework that operates during the optimization of 3D Gaussian Splatting representations. At every training iteration, we differentiably extract a mesh—including both vertex locations and connectivity— directly from Gaussian parameters. This enables gradient flow from the mesh to Gaussians, allowing us to promote bidirectional consis
- Method summary: See local PDF; 
- Key claim / relevance: Relevant local reference Limitation: Requires manual reading for details.

## 22. PGSR: Planar-based Gaussian Splatting for Efficient and High-Fidelity Surface Reconstruction Danpeng Chen, Hai Li, Weicai Ye, Yifan Wang, Weijian Xie, Shangjin Zhai, Nan Wang, Haomin Liu, Hujun Bao, Guofeng Zhang

- File: `PGSR Planar-based Gaussian Splatting for Efficient and High-Fidelity Surface Reconstruction.pdf`
- Year: Unknown
- Venue/status: Unknown / local PDF
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: —Recently, 3D Gaussian Splatting (3DGS) has at- tracted widespread attention due to its high-quality rendering, H. Bao, G. Zhang, W. Ye are with the State Key Lab of CAD&CG, Zhejiang University. E-mails: {baohujun, zhangguofeng }@zju.edu.cn, maikeyewe- icai@gmail.com. D. Chen and W. Xie are with the State Key Lab of CAD&CG, Zhe- jiang University. W. Xie is also affiliated with SenseTime Research, and D. Chen is also affiliated with Tetras.AI. E-mails: 11921155@zju.edu.cn, xieweijian@sensetime.com. H. Li is with RayNeo. E-mail: lihai@ffalcon.cn. Y . Wang is with Shanghai AI Laboratory. E-mail: wangyifan@pjlab.org.cn. S. Zhai, N. Wang and H. Liu are with SenseTime Research. E-mails: {zhaishangjin, wangnan, liuhaomin }@sensetime.com. Corresponding author: Guofeng Zhang Digital Object Identifier 10.1109/TVCG.2024.3494046 and ultra-fast training and rendering speed. However, due to the unstru
- Method summary: See local PDF; 
- Key claim / relevance: Relevant local reference Limitation: Requires manual reading for details.

## 23. IRGS: Inter-Reflective Gaussian Splatting with 2D Gaussian Ray Tracing

- File: `REFLECTIVE GAUSSIAN SPLATTING.pdf`
- Year: 2025
- Venue/status: arXiv preprint
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: Novel view synthesis has experienced significant advancements owing to increas- ingly capable NeRF- and 3DGS-based methods. However, reflective object re- construction remains challenging, lacking a proper solution to achieve real-time, high-quality rendering while accommodating inter-reflection. To fill this gap, we introduce a Reflective Gaussian splatting ( Ref-Gaussian) framework character- ized with two components: (I)Physically based deferred renderingthat empowers the rendering equation with pixel-level material properties via formulating split- sum approximation; (II) Gaussian-grounded inter-reflection that realizes the de- sired inter-reflection function within a Gaussian splatting paradigm for the first time. To enhance geometry modeling, we further introduce material-aware nor- mal propagation and an initial per-Gaussian shading stage, along with 2D Gaus- sian primitives. Exte
- Method summary: 2D Gaussians with ray tracing.; 2D Gaussian ray tracing plus rasterization.
- Key claim / relevance: Directly targets inter-reflection. Limitation: UV/PBR baking and stable optimization remain open.

## 24. Specular Flow and the Recovery of Surface Structure

- File: `Roth和Black - 2006 - Specular Flow and the Recovery of Surface Structure.pdf`
- Year: 2006
- Venue/status: ECCV/IJCV-era vision paper
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: In scenes containing specular objects, the image motion observed by a moving camera may be an intermixed com- bination of optical ﬂow resulting from diffuse reﬂectance (diffuse ﬂow) and specular reﬂection (specular ﬂow). Here, with few assumptions, we formalize the notion of specular ﬂow, show how it relates to the 3D structure of the world, and develop an algorithm for estimating scene structure from 2D image motion. Unlike previous work on isolated specular highlights we use two image frames and estimate the semi-dense ﬂow arising from the specular reﬂections of textured scenes. We parametrically model the image motion of a quadratic surface patch viewed from a moving camera. The ﬂow is modeled as a probabilistic mixture of diffuse and specular components and the 3D shape is recovered using an Expectation-Maximization algorithm. Rather than treating specular reﬂections as noise to be r
- Method summary: Specular-flow field.; Geometric reflection model.
- Key claim / relevance: Foundational specular shape prior. Limitation: Does not provide mesh/material pipeline for sparse multiview RGB.

## 25. SOF: Sorted Opacity Fields for Fast Unbounded Surface Reconstruction

- File: `SOF Sorted Opacity Fields for Fast Unbounded Surface Reconstruction.pdf`
- Year: 2025
- Venue/status: TOG / preprint
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: SOF: Sorted Opacity Fields for Fast Unbounded Surface Reconstruction LUKAS RADL, Graz University of Technology, Austria FELIX WINDISCH, Graz University of Technology, Austria THOMAS DEIXELBERGER, Huawei Technologies, Austria JOZEF HLADKY, Huawei Technologies, Switzerland MICHAEL STEINER, Graz University of Technology, Austria DIETER SCHMALSTIEG, Graz University of Technology, Austria and University of Stuttgart, Germany MARKUS STEINBERGER, Graz University of Technology, Austria and Huawei Technologies, Austria Fig. 1. We introduce Sorted Opacity Fields (SOF), which allow for swift extraction of high-quality unbounded meshes. Compared to current state-of-the-art Gaussian Opacity Fields [Yu et al. 2024c], our meshes are more detailed and exhibit fewer artifacts. In addition, our approach accelerates optimization by over 3× and meshing by up to an order of magnitude. Recent advances in 3D G
- Method summary: Sorted opacity field.; Opacity-field rendering/extraction.
- Key claim / relevance: Fast unbounded reconstruction. Limitation: Reflective objects can induce wrong opacity surfaces.

## 26. SSD-GS: Scattering and Shadow Decomposition for Relightable 3D Gaussian Splatting

- File: `SSD-GS Scattering and Shadow Decomposition for Relightable 3D Gaussian Splatting.pdf`
- Year: 2025
- Venue/status: ICLR / preprint
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: We present SSD-GS, a physically-based relighting framework built upon 3D Gaussian Splatting (3DGS) that achieves high-quality reconstruction and photore- alistic relighting under novel lighting conditions. In physically-based relighting, accurately modeling light-material interactions is essential for faithful appearance reproduction. However, existing 3DGS-based relighting methods adopt coarse shading decompositions, either modeling only diffuse and specular reflections or relying on neural networks to approximate shadows and scattering. This leads to limited fidelity and poor physical interpretability, particularly for anisotropic met- als and translucent materials. To address these limitations, SSD-GS decomposes reflectance into four components: diffuse, specular, shadow, and subsurface scat- tering. We introduce a learnable dipole-based scattering module for subsurface transport, an 
- Method summary: 3DGS with scattering/shadow factors.; Relightable Gaussian rendering.
- Key claim / relevance: Addresses relighting factors. Limitation: No mirror/near-field reflection or mesh/UV output.

## 27. SuGaR: Surface-Aligned Gaussian Splatting for Efficient 3D Mesh Reconstruction and High-Quality Mesh Rendering Antoine Gu´edon Vincent Lepetit LIGM, Ecole des Ponts, Univ Gustave Eiffel, CNRS, France

- File: `SuGaR Surface-Aligned Gaussian Splatting for Efficient 3D Mesh Reconstruction and High-Quality Mesh Rendering.pdf`
- Year: Unknown
- Venue/status: Unknown / local PDF
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: We propose a method to allow precise and extremely fast mesh extraction from 3D Gaussian Splatting [15]. Gaus- sian Splatting has recently become very popular as it yields realistic rendering while being significantly faster to train than NeRFs. It is however challenging to extract a mesh from the millions of tiny 3D Gaussians as these Gaussians tend to be unorganized after optimization and no method has been proposed so far. Our first key contribution is a regularization term that encourages the Gaussians to align well with the surface of the scene. We then introduce a method that exploits this alignment to extract a mesh from the Gaussians using Poisson reconstruction, which is fast, scalable, and preserves details, in contrast to the March- ing Cubes algorithm usually applied to extract meshes from Neural SDFs. Finally, we introduce an optional refinement strategy that binds Gaussians
- Method summary: See local PDF; 
- Key claim / relevance: Relevant local reference Limitation: Requires manual reading for details.

## 28. 3D Gaussian Splatting with Self-Constrained Priors for High Fidelity Surface Reconstruction

- File: `Tang 等 - SpecTRe-GS Modeling Highly Specular Surfaces with Reflected Nearby Objects by Tracing Rays in 3D Ga.pdf`
- Year: 2025
- Venue/status: arXiv preprint
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: 3D Gaussian Splatting (3DGS), a recently emerged multi- view 3D reconstruction technique, has shown significant advantages in real-time rendering and explicit editing. However, 3DGS encounters challenges in the accurate mod- eling of both high-frequency view-dependent appearances and global illumination effects, including inter-reflection. This paper introduces SpecTRe-GS, which addresses these challenges and models highly Specular surfaces that re- flect nearby objects through Tracing Rays in 3D Gaussian Splatting. SpecTRe-GS separately models reflections from highly specular and rough surfaces to leverage the distinc- tions between their reflective properties and integrates an efficient ray tracer within the 3DGS framework for querying secondary rays, thus achieving fast and accurate rendering. Also, it incorporates normal prior guidance and joint geom- etry optimization at various sta
- Method summary: 3DGS with self-constrained geometry priors.; Differentiable image rendering
- Key claim / relevance: Reduces geometry noise without extra sensors. Limitation: Reflective surfaces remain underconstrained because reflection transport is not modeled.

## 29. 3D Gaussian Splatting with Self-Constrained Priors for High Fidelity Surface Reconstruction

- File: `Zhang 等 - 2024 - RefGaussian Disentangling Reflections from 3D Gaussian Splatting for Realistic Rendering.pdf`
- Year: 2025
- Venue/status: arXiv preprint
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: 3D Gaussian Splatting (3D-GS) has made a notable advancement in the field of neural rendering, 3D scene reconstruction, and novel view synthesis. Nevertheless, 3D-GS encounters the main challenge when it comes to accurately representing physical reflections, especially in the case of total reflection and semi-reflection that are commonly found in real-world scenes. This limitation causes reflections to be mistakenly treated as independent elements with physical presence, leading to imprecise reconstructions. Herein, to tackle this challenge, we propose RefGaussian to disentangle reflections from 3D-GS for realistically modeling reflections. Specifically, we propose to split a scene into transmitted and reflected components and represent these components using two Spherical Harmonics (SH). Given that this decomposition is not fully determined, we employ local regularization techniques to 
- Method summary: 3DGS with self-constrained geometry priors.; Differentiable image rendering
- Key claim / relevance: Reduces geometry noise without extra sensors. Limitation: Reflective surfaces remain underconstrained because reflection transport is not modeled.

## 30. Ref-GS: Directional Factorization for 2D Gaussian Splatting

- File: `Zhang 等 - 2025 - Ref-GS Directional Factorization for 2D Gaussian Splatting.pdf`
- Year: 2025
- Venue/status: arXiv preprint
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: In this paper, we introduce Ref-GS, a novel approach for di- rectional light factorization in 2D Gaussian splatting [11], which enables photorealistic view-dependent appearance rendering and precise geometry recovery. Ref-GS builds upon the deferred rendering of Gaussian splatting and ap- plies directional encoding to the deferred-rendered surface, effectively reducing the ambiguity between orientation and viewing angle. Next, we introduce a spherical Mip-grid to capture varying levels of surface roughness, enabling roughness-aware Gaussian shading. Additionally, we pro- † denote co-corresponding authors. pose a simple yet efficient geometry-lighting factorization that connects geometry and lighting via the vector outer product, significantly reducing renderer overhead when in- tegrating volumetric attributes. Our method achieves su- perior photorealistic rendering for a range of open-wo
- Method summary: 2DGS with directional appearance factorization.; 2DGS rasterization.
- Key claim / relevance: Improves view-dependent effects on surface splats. Limitation: Directional appearance alone cannot infer PBR maps or near-field reflection.

## 31. MGSR: 2D/3D Mutual-boosted Gaussian Splatting for High-fidelity Surface Reconstruction under Various Light Conditions

- File: `Zhou 等 - 2025 - MGSR 2D3D Mutual-boosted Gaussian Splatting for High-fidelity Surface Reconstruction under Various.pdf`
- Year: 2025
- Venue/status: arXiv preprint
- Authors: see first page of the local PDF; author strings were not normalized automatically to avoid introducing citation errors.
- Abstract excerpt: Novel view synthesis (NVS) and surface reconstruction (SR) are essential tasks in 3D Gaussian Splatting (3DGS). De- spite recent progress, these tasks are often addressed in- dependently, with GS-based rendering methods struggling under diverse light conditions and failing to produce ac- curate surfaces, while GS-based reconstruction methods frequently compromise rendering quality. This raises a central question: must rendering and reconstruction al- ways involve a trade-off? To address this, we propose MGSR, a 2D/3D Mutual-boosted Gaussian Splatting for Surface Reconstruction that enhances both rendering qual- ity and 3D reconstruction accuracy. MGSR introduces two branches—one based on 2DGS and the other on 3DGS. The 2DGS branch excels in surface reconstruction, providing precise geometry information to the 3DGS branch. Lever- aging this geometry, the 3DGS branch employs a geometry- gu
- Method summary: Mutual-boosted 2D and 3D Gaussians.; Hybrid Gaussian rendering.
- Key claim / relevance: Combines 2D surface accuracy and 3D appearance. Limitation: Reflective variation can still be mistaken for geometry/material.
