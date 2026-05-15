import json

from refmotion_gs_mvp.scripts.run_phase3_milestone32 import run
from refmotion_gs_mvp.src.decision_checks import REQUIRED_BASELINES


def test_milestone32_runner_schema_and_scope_flags(tmp_path):
    metrics = run(
        tmp_path,
        num_views=4,
        width=28,
        height=22,
        uv_height=4,
        uv_width=8,
        dense_iterations=2,
        max_active_texels=6,
        sample_count=60,
        update_radius=0,
    )
    metrics_path = tmp_path / "metrics.json"
    summary_path = tmp_path / "summary.md"
    loss_plot_path = tmp_path / "dense_loss_history.png"

    assert metrics_path.exists()
    assert summary_path.exists()
    assert loss_plot_path.exists()
    assert json.loads(metrics_path.read_text(encoding="utf-8")) == metrics

    for section in (
        "dense_normal_optimization",
        "dense_no_cycle_ablation",
        "texture_baking",
        "uv_texture_baking",
        "decision_checks",
        "phase3",
    ):
        assert section in metrics

    assert metrics["phase3"]["milestone"] == "3.2"
    assert metrics["phase3"]["implemented_dense_normal_optimization"] is True
    assert metrics["phase3"]["implemented_learned_near_field_reflection"] is False
    assert metrics["phase3"]["implemented_inter_reflection_residual"] is False
    assert metrics["phase3"]["implemented_full_pbr_optimization"] is False
    assert metrics["phase3"]["claimed_relighting_or_editing"] is False

    uv_leakage = metrics["uv_texture_baking"]["specular_leakage_score"]
    for baseline in REQUIRED_BASELINES:
        assert baseline in uv_leakage
