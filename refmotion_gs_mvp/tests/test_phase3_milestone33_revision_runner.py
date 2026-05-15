import json

from refmotion_gs_mvp.scripts.run_phase3_milestone33_revision import run


def test_milestone33_revision_runner_schema_and_scope(tmp_path):
    metrics = run(
        tmp_path,
        num_views=4,
        width=18,
        height=16,
        uv_height=8,
        uv_width=16,
        dense_iterations=2,
        max_active_texels=8,
        sample_count=20,
        update_radius=1,
    )

    metrics_path = tmp_path / "metrics.json"
    summary_path = tmp_path / "summary.md"
    objective_plot_path = tmp_path / "objective_vs_normal_error.png"
    coverage_plot_path = tmp_path / "reflector_hit_coverage_by_texel.png"

    assert metrics_path.exists()
    assert summary_path.exists()
    assert objective_plot_path.exists()
    assert coverage_plot_path.exists()
    assert json.loads(metrics_path.read_text(encoding="utf-8")) == metrics

    for section in (
        "dataset",
        "reflectors",
        "baseline_milestone33_decision_checks",
        "dense_trajectory_diagnostics",
        "coverage_diagnostics",
        "routing_diagnostics",
        "phase3",
        "recommendation",
    ):
        assert section in metrics

    phase3 = metrics["phase3"]
    assert phase3["milestone"] == "3.3_revision"
    assert phase3["purpose"] == "dense_normal_gate_failure_diagnostics"
    assert phase3["implements_learned_near_field_reflection_field"] is False
    assert phase3["implements_inter_reflection_residual"] is False
    assert phase3["implements_full_pbr_optimization"] is False
    assert phase3["claims_relighting_or_material_editing"] is False
    assert phase3["claims_representation_novelty"] is False

    routing = metrics["routing_diagnostics"]
    assert "normal_refinement_improves_over_reflection_confidence" in routing
    assert "normal_refinement_beats_oracle_mask" in routing

    summary_text = summary_path.read_text(encoding="utf-8")
    assert "oracle mask exclusion remains an honest comparator" in summary_text
