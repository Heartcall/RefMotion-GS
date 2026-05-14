# Proposed Method: RefTex-GS

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
