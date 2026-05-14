from refmotion_gs_mvp.src.experiment_protocol import (
    phase3_milestone_metadata,
    write_summary,
)


def test_phase3_metadata_blocks_forbidden_components():
    metadata = phase3_milestone_metadata(
        milestone="3.1",
        purpose="experiment_framework_refactor",
    )

    assert metadata["milestone"] == "3.1"
    assert metadata["purpose"] == "experiment_framework_refactor"
    assert metadata["implemented_dense_normal_optimization"] is False
    assert metadata["implemented_learned_near_field_reflection"] is False


def test_result_summary_mentions_oracle_mask_status(tmp_path):
    metrics = {
        "decision_checks": {
            "routing_beats_all_pixels": True,
            "routing_beats_noisy_mask": True,
            "routing_beats_oracle_mask": False,
        },
        "uv_texture_baking": {
            "specular_leakage_score": {
                "oracle_mask_exclusion": 0.18894842742715495,
                "normal_refinement_plus_routing": 0.19090032877604535,
            }
        },
        "phase3": phase3_milestone_metadata(
            milestone="3.1",
            purpose="experiment_framework_refactor",
        ),
    }
    summary_path = tmp_path / "summary.md"

    write_summary(summary_path, metrics)

    summary = summary_path.read_text(encoding="utf-8")
    assert "oracle mask" in summary.lower()
    assert "routing_beats_oracle_mask" in summary
    assert "false" in summary.lower()
