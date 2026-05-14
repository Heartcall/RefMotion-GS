# Theory Rewrite

## Definitions

Let image i have camera center o_i, rotation R_i, intrinsics K_i, and pixel p in homogeneous image coordinates. The camera ray is

```text
d_i(p) = normalize(R_i^T K_i^{-1} p)
r_i(p, t) = o_i + t d_i(p), t > 0.
```

Let M be the current triangle mesh. The visible surface point is

```text
x_i(p) = first_intersection(r_i(p, t), M).
```

The outgoing view direction at the surface is

```text
omega_o_i(p) = normalize(o_i - x_i(p)).
```

The surface normal is

```text
n(x) = normalize(n_mesh(x) + T_x n_tex(u(x))),
```

where n_mesh is the interpolated mesh normal, T_x is the tangent frame, n_tex is an optional tangent-space normal map, and u(x) is the UV coordinate.

The reflected ray direction is

```text
omega_r_i(p) = 2 dot(n(x), omega_o_i(p)) n(x) - omega_o_i(p).
```

The ambiguity: for reflective pixels, I_i(p) is not texture at u(x). It is radiance arriving along omega_r_i(p), modulated by BRDF. A correct loss must avoid treating I_i(p) as diffuse texture evidence.

## What Was Weak in Phase 1

The Phase 1 term

```text
L_ref = sum p_ref ||I_i(p) - R(...)|| + lambda_flow ||Pi_j(x') - p'_j||
```

does not define x', p'_j, or the correspondence mechanism. It also lets a learned F_nf absorb errors unless capacity and gradients are controlled. The following alternatives make the supervision explicit.

## Formulation A: Feature-Space Reflection-Cycle Consistency

### Assumptions

1. The object is static and cameras are calibrated.
2. The reflective surface is opaque.
3. Reflected content is at least partly visible in multiple views, either directly or through reflection.
4. A frozen image feature extractor phi produces features that are more stable than RGB under small lighting changes.
5. Initial mesh geometry is close enough that reflected-ray neighborhoods are meaningful.

### Correspondence Definition

For a reflective pixel p in view i:

```text
x = x_i(p)
n = n(x)
omega_r = reflect(omega_o_i(p), n)
```

Instead of requiring a hard reflected 3D hit, define a feature query in a second view j by searching along the epipolar-consistent image neighborhood predicted by reflection geometry.

Let q_j(s) be candidate pixels in view j whose visible surface points x_j(q) have reflected rays omega_r_j(q) close to omega_r_i(p) and whose surface positions are close in reflection-ray Pluecker space:

```text
P_i = (omega_r_i, m_i = x_i cross omega_r_i)
P_j(q) = (omega_r_j(q), m_j(q) = x_j(q) cross omega_r_j(q)).
D_ref(i,p,j,q) = ||omega_r_i - omega_r_j(q)||_2^2 + beta ||m_i - m_j(q)||_2^2.
```

The soft correspondence weights are

```text
w_ij(p,q) = softmax_q(-D_ref(i,p,j,q) / tau)
```

over a local candidate set Q_j(p). The reflected feature predicted from view j is

```text
F_j_ref(p) = sum_{q in Q_j(p)} stopgrad(w_ij(p,q)) phi(I_j)(q).
```

The feature-space reflection-cycle loss is

```text
L_cycle = sum_{i,p in Omega_ref} p_ref(u(x))
          sum_{j in N(i)} rho( phi(I_i)(p) - F_j_ref(p) ).
```

For a stronger cycle:

```text
q_hat = argmax_q w_ij(p,q)
p_back = argmin_p' D_ref(j,q_hat,i,p')
L_back = ||p - stopgrad(p_back)||_1
```

or a soft version with expected pixel coordinates.

### What Is p'_j?

In this formulation, p'_j is not an arbitrary learned point. It is the soft reflected-ray correspondence in image j:

```text
p'_j = sum_{q in Q_j(p)} w_ij(p,q) q.
```

The correspondence is image-space and feature-space, constrained by world-space reflected-ray geometry.

### Optimized Variables

Optimized:

- mesh vertices V,
- normal-map parameters n_tex if used,
- surface Gaussian positions constrained to the mesh,
- reflective-region logits p_ref only after warmup.

Detached:

- image features phi(I),
- correspondence weights w_ij in the first version,
- mesh visibility for the first MVP stage.

### Gradient Path

The main normal gradient comes from D_ref when w_ij is not detached, or from a differentiable soft-min variant:

```text
L_cycle_soft = -tau log sum_q exp(-D_ref(i,p,j,q)/tau) * sim(phi_i(p), phi_j(q)).
```

For MVP stability, first detach correspondences and optimize only a diagnostic normal perturbation; then enable gradients through D_ref after verifying that the loss basin points toward ground-truth normals.

### Avoiding Trivial Solutions

The model cannot minimize L_cycle by painting arbitrary color into a reflection field because no learned reflection field appears in Formulation A. The only adjustable geometric variable affecting correspondence is the normal/mesh. Texture is supervised separately only on non-reflective or low-p_ref samples.

### Failure Cases

- Reflected content is not visible in other views.
- Repeated textures create ambiguous feature matches.
- Initial geometry is too wrong.
- Very rough reflections blur features beyond reliable matching.
- Dynamic reflected objects violate the static assumption.

### Computational Cost

For B reflective pixels, K nearby views, and Q candidates per view, cost is O(B K Q) feature comparisons. MVP can sample 2k to 10k reflective pixels per iteration and use 16 to 64 candidates.

### Suitability for First Implementation

Suitable. It avoids learning F_nf, directly tests the core hypothesis, and gives a clean ablation against RGB and mask-only texture baking.

## Formulation B: Proxy-Reflector-Field Consistency

### Assumptions

1. Reflected radiance can be approximated by a compact proxy field P(y, omega) in a bounded volume around the object.
2. The proxy is shared across views.
3. Proxy capacity is limited, so it cannot memorize arbitrary per-view colors.
4. Initial normals are close enough for reflected rays to query the right proxy region.

### Proxy Representation

Use either sparse reflection Gaussians or a compact radiance grid:

```text
P = {g_l = (mu_l, Sigma_l, c_l, sigma_l)}_{l=1}^L
```

or

```text
F_proxy(y, omega) = MLP_lowrank( hash(y), SH_low(omega) ).
```

For a surface point x and reflected direction omega_r, the soft reflected query is

```text
C_proxy(x, omega_r) =
  sum_l A_l(x, omega_r) c_l / (sum_l A_l + eps)

A_l = exp(-d_perp(ray(x, omega_r), mu_l)^2 / sigma_l^2)
      exp(-t_l / eta)
      v_l,
```

where t_l is the closest positive ray parameter and v_l is optional visibility.

### Rendering Term

For reflective pixels:

```text
C_i(p) = (1 - p_ref) a(u) + p_ref S(x, omega_o, n, rho) C_proxy(x, omega_r),
```

where S is a bounded specular weight from a simplified BRDF.

The proxy consistency loss is

```text
L_proxy = sum_{i,p in Omega_ref} p_ref(u)
          rho( phi(I_i)(p) - phi_render(C_proxy(x_i(p), omega_r_i(p))) ).
```

To use cross-view sharing, enforce that two rays with nearby Pluecker coordinates query similar proxy features:

```text
L_share = sum_{(i,p),(j,q)}
          kappa(D_ref(i,p,j,q))
          ||C_proxy(x_i, omega_r_i) - C_proxy(x_j, omega_r_j)||_1.
```

### What Is the Reflected Point?

There is no single hard reflected point. The reflected point is a soft ray query over proxy primitives:

```text
y_hat(x, omega_r) = sum_l A_l mu_l / (sum_l A_l + eps).
```

Then

```text
p'_j = Pi_j(y_hat)
```

only if y_hat is visible in camera j. Otherwise p'_j is undefined and the loss should use proxy-feature consistency rather than image-space projection.

### Optimized Variables

Optimized:

- mesh vertices and normals,
- reflective gate,
- proxy positions and colors, after geometry warmup,
- low-capacity environment/proxy parameters.

Detached:

- image features,
- proxy parameters during normal-only warmup,
- reflective gate during first geometry stage.

### Gradient Path

Normals affect omega_r, which changes proxy query weights A_l and thus C_proxy. Proxy parameters also receive gradients, so anti-cheating constraints are mandatory.

### Avoiding Trivial Solutions

This formulation is dangerous. It needs:

- low proxy capacity,
- cross-view sharing,
- BRDF energy bounds,
- stop-gradient schedule,
- reflection gate sparsity,
- held-out-view diagnostics.

Without these, the proxy can become arbitrary view-dependent color.

### Failure Cases

- Proxy memorizes training views.
- Proxy absorbs normal error.
- Reflected world is outside proxy volume.
- Occlusion along reflected rays is wrong.
- Inter-reflection creates radiance not representable by single-bounce proxy.

### Computational Cost

Sparse proxy Gaussians: O(B L_local), where L_local is the number of proxy primitives near each reflected ray. With acceleration, this is practical but heavier than Formulation A.

Compact MLP/grid: O(B) queries, but training can be slower and harder to diagnose.

### Suitability for First Implementation

Not suitable for the first MVP. It is a second-stage system component after Formulation A proves that reflection-induced motion improves normals or texture leakage.

## Recommended Theory for First Paper

Use Formulation A first. It is narrower, more falsifiable, and less vulnerable to the criticism that the reflection field memorizes the images. The first submission should not introduce F_nf unless Formulation A succeeds and reviewers can see why a learned proxy is necessary.
