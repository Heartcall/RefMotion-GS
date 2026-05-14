import pytest

from refmotion_gs_mvp.src.decision_checks import (
    compute_routing_decision_checks,
    require_baselines,
)


def test_decision_checks_preserve_mvp_thresholds():
    uv_leakage = {
        "all_pixels": 0.8937587779761458,
        "oracle_mask_exclusion": 0.18894842742715495,
        "noisy_mask_only": 0.48688553583972904,
        "reflection_confidence_routing": 0.20555594061539617,
        "normal_refinement_plus_routing": 0.19090032877604535,
    }

    checks = compute_routing_decision_checks(uv_leakage)

    assert checks["routing_beats_all_pixels"] is True
    assert checks["routing_beats_noisy_mask"] is True
    assert checks["routing_beats_oracle_mask"] is False


def test_decision_checks_require_all_baselines():
    incomplete = {
        "all_pixels": 0.8937587779761458,
        "oracle_mask_exclusion": 0.18894842742715495,
        "noisy_mask_only": 0.48688553583972904,
        "normal_refinement_plus_routing": 0.19090032877604535,
    }

    with pytest.raises(KeyError, match="reflection_confidence_routing"):
        require_baselines(incomplete)
