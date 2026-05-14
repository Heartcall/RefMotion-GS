"""Decision checks for RefMotion-GS routing metrics."""

REQUIRED_BASELINES: tuple[str, ...] = (
    "all_pixels",
    "oracle_mask_exclusion",
    "noisy_mask_only",
    "reflection_confidence_routing",
    "normal_refinement_plus_routing",
)


def require_baselines(
    metric_values: dict[str, float],
    required: tuple[str, ...] | None = None,
) -> None:
    """Validate that all required metric baselines are present."""
    required_baselines = REQUIRED_BASELINES if required is None else required
    missing = tuple(name for name in required_baselines if name not in metric_values)
    if missing:
        raise KeyError(", ".join(missing))


def compute_routing_decision_checks(uv_leakage: dict[str, float]) -> dict[str, bool]:
    """Compute leakage decision checks for the current routing method."""
    require_baselines(uv_leakage)
    routing_leakage = uv_leakage["normal_refinement_plus_routing"]

    return {
        "routing_beats_all_pixels": routing_leakage < uv_leakage["all_pixels"],
        "routing_beats_noisy_mask": routing_leakage < uv_leakage["noisy_mask_only"],
        "routing_beats_oracle_mask": (
            routing_leakage < uv_leakage["oracle_mask_exclusion"]
        ),
    }
