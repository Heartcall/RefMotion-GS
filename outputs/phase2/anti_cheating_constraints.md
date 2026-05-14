# Anti-Cheating Constraints

## Problem

A learned near-field reflection field F_nf(x, omega) can become arbitrary view-dependent color. If that happens, the model can fit images without improving geometry, normals, or texture maps. The constraints below are mandatory if F_nf is used. For the first MVP, avoid F_nf entirely.

## 1. Directional Consistency

Equation:

```text
L_dir = sum_{a,b} k_x(||x_a - x_b||)
        k_w(||omega_a - omega_b||)
        ||F_nf(x_a, omega_a) - F_nf(x_b, omega_b)||_1.
```

Degeneracy prevented: per-camera memorization where nearly identical reflected rays produce unrelated colors.

Possible harm: over-smooths true high-frequency reflected content, especially mirror-like text.

## 2. Position Smoothness / Low-Rank Constraint

Low-rank factorization:

```text
F_nf(x, omega) = sum_{m=1}^M b_m(x) h_m(omega), M small.
L_rank = sum_m TV(b_m) + lambda_h ||h_m||_2^2.
```

Degeneracy prevented: dense 5D radiance storage that memorizes training views.

Possible harm: cannot represent complex local reflections or occlusions.

## 3. Cross-View Sharing Constraint

Equation:

```text
L_share = sum_{i,j,p,q}
          kappa(D_ref(i,p,j,q))
          ||F_nf(x_i(p), omega_r_i(p))
            - F_nf(x_j(q), omega_r_j(q))||_1.
```

Degeneracy prevented: different colors for the same reflected ray observed from different views.

Possible harm: wrong correspondences can force incorrect averaging.

## 4. Energy Conservation / BRDF Bound

Equation:

```text
0 <= p_ref <= 1
0 <= S_spec(x, omega_o) <= F0_max
||C_spec||_1 <= gamma E_env + gamma_nf E_proxy
L_energy = ReLU(||C_spec||_1 - gamma E_available)^2.
```

Degeneracy prevented: reflection field explains diffuse texture by emitting unbounded radiance.

Possible harm: hard energy bounds can underfit saturated highlights.

## 5. Reflective-Region Gate Regularization

Equation:

```text
L_gate_tv = TV(p_ref)
L_gate_prior = BCE(p_ref, p_ref_prior)
L_gate_area = |mean(p_ref) - pi_ref|
```

Degeneracy prevented: all pixels become reflective and bypass UV texture supervision.

Possible harm: incorrect prior can suppress real reflective regions.

## 6. Entropy / Sparsity Prior on p_ref

Equation:

```text
L_sparse = lambda_1 mean(p_ref)
L_entropy = lambda_H mean(-p_ref log p_ref - (1-p_ref) log(1-p_ref)).
```

Use entropy with care:

- positive entropy penalty encourages binary gates,
- L1 sparsity discourages using reflection everywhere.

Degeneracy prevented: soft, ambiguous gates that route every pixel partly to reflection and partly to texture.

Possible harm: mixed glossy/diffuse materials may need intermediate p_ref.

## 7. Stop-Gradient Strategy

Schedule:

```text
Stage 1: optimize mesh/UV diffuse on non-reflective pixels. p_ref fixed.
Stage 2: optimize normals with feature reflection-cycle loss. No F_nf.
Stage 3: introduce F_nf with mesh/normals detached for N iterations.
Stage 4: alternate:
  update F_nf with geometry detached,
  update normals with F_nf detached.
```

Degeneracy prevented: simultaneous normal and reflection-field drift where each compensates for the other.

Possible harm: alternating optimization can slow convergence and freeze early mistakes.

## 8. Training Schedule

Minimal schedule if F_nf is used:

1. Warm up PGSR/2DGS mesh.
2. Bake initial UV texture using low-reflective pixels only.
3. Learn p_ref from view-dependent residuals and synthetic masks.
4. Optimize reflection-cycle normal loss without F_nf.
5. Add low-capacity F_nf only after normals improve on validation views.
6. Keep F_nf capacity fixed and evaluate held-out reflected motion.

Degeneracy prevented: the field cannot appear before geometry has a chance to explain reflection motion.

Possible harm: if geometry initialization is poor, the schedule may never recover.

## 9. Diagnostics Showing Cheating

Run these diagnostics before trusting any result:

1. Held-out camera reflection error decreases but normal error does not. This means F_nf is fitting appearance, not geometry.
2. UV albedo contains reflected scene colors. This means texture supervision is contaminated.
3. F_nf has high spatial frequency aligned with camera views. This indicates view memorization.
4. p_ref mean approaches 1.0 over most of the object. The gate is bypassing texture.
5. Randomizing reflected-object positions in synthetic validation does not hurt training-view PSNR. The model is not using physical reflection.
6. Normal perturbation test: perturb normals by known angles. A valid reflection loss should increase monotonically near the ground-truth normal.
7. Cross-view query test: same reflected ray from two views should query similar F_nf values.
8. Remove F_nf at test time. If diffuse texture quality collapses, F_nf may have been carrying texture.

## Recommendation

For the first paper, use these constraints only as design notes. Do not introduce a trainable near-field reflection field in the MVP. A learned field makes the theory harder and the novelty weaker because Ref-DGS and SpecTRe-GS already occupy that space.
