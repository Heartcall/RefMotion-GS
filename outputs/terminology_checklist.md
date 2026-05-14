# Terminology Checklist

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
