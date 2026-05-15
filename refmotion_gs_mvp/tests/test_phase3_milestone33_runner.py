import json

from refmotion_gs_mvp.scripts.run_phase3_milestone33 import run
from refmotion_gs_mvp.src.decision_checks import REQUIRED_BASELINES


def test_milestone33_runner_schema_baselines_and_scope_flags(tmp_path):
    metrics = run(
        tmp_path,
        num_views=6,
        width=24,
        height=20,
        uv_height=4,
        uv_width=8,
        dense_iterations=2,
        max_active_texels=8,
        sample_count=30,
        update_radius=1,
    )
    metrics_path = tmp_path / "metrics.json"
    summary_path = tmp_path / "summary.md"
    dense_plot_path = tmp_path / "dense_loss_history.png"
    hit_plot_path = tmp_path / "reflector_hit_map.png"

    assert metrics_path.exists()
    assert summary_path.exists()
    assert dense_plot_path.exists()
    assert hit_plot_path.exists()
    assert json.loads(metrics_path.read_text(encoding="utf-8")) == metrics

    for section in (
        "dataset",
        "reflectors",
        "loss_landscape",
        "global_rotation_reference",
        "dense_normal_optimization",
        "dense_no_cycle_ablation",
        "pixel_baking",
        "uv_texture_baking",
        "decision_checks",
        "phase3",
    ):
        assert section in metrics

    assert metrics["dataset"]["scene_type"] == "analytic_near_object_reflection"
    assert metrics["dataset"]["reflector_hit_fraction"] >= 0.15
    assert metrics["dataset"]["train_view_indices"] == [0, 1, 2, 3]
    assert metrics["dataset"]["test_view_indices"] == [4, 5]

    dense = metrics["dense_normal_optimization"]
    assert dense["method_name"] == "dense_reflection_cycle_optimizer"
    assert dense["uses_reflection_cycle_loss"] is True
    assert metrics["dense_no_cycle_ablation"]["uses_reflection_cycle_loss"] is False

    phase3 = metrics["phase3"]
    assert phase3["milestone"] == "3.3"
    assert phase3["purpose"] == "stricter_scene_or_renderer_validation"
    assert phase3["renderer_path"] == "analytic_near_object_fallback"
    assert phase3["used_blender_cycles"] is False
    assert phase3["implements_learned_near_field_reflection_field"] is False
    assert phase3["implements_inter_reflection_residual"] is False
    assert phase3["implements_full_pbr_optimization"] is False
    assert phase3["claims_relighting_or_material_editing"] is False
    assert phase3["claims_representation_novelty"] is False

    for metric_group in ("pixel_baking", "uv_texture_baking"):
        leakage = metrics[metric_group]["specular_leakage_score"]
        for baseline in REQUIRED_BASELINES:
            assert baseline in leakage

    for decision_check in (
        "loss_correlated_near_gt",
        "reflector_hit_fraction_sufficient",
        "dense_normal_error_improves_10_percent",
        "dense_beats_no_cycle_ablation",
        "routing_beats_all_pixels",
        "routing_beats_noisy_mask",
        "routing_beats_oracle_mask",
    ):
        assert decision_check in metrics["decision_checks"]
