"""Phase 3 experiment metadata and reporting helpers."""

from pathlib import Path
from typing import Any


def phase3_milestone_metadata(milestone: str, purpose: str) -> dict[str, Any]:
    """Create Phase 3 milestone metadata with forbidden components disabled."""
    return {
        "milestone": milestone,
        "purpose": purpose,
        "implemented_dense_normal_optimization": False,
        "implemented_learned_near_field_reflection": False,
    }


def write_summary(path: str | Path, metrics: dict[str, Any]) -> None:
    """Write a compact markdown summary for Phase 3 metrics."""
    summary_path = Path(path)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    decision_checks = metrics.get("decision_checks", {})
    phase3 = metrics.get("phase3", {})
    uv_leakage = (
        metrics.get("uv_texture_baking", {}).get("specular_leakage_score", {})
    )

    routing_oracle = decision_checks.get("routing_beats_oracle_mask")
    oracle_leakage = uv_leakage.get("oracle_mask_exclusion")
    routing_leakage = uv_leakage.get("normal_refinement_plus_routing")

    lines = [
        "# Phase 3 Milestone Summary",
        "",
        "## Metadata",
        "",
        f"- milestone: {phase3.get('milestone', 'unknown')}",
        f"- purpose: {phase3.get('purpose', 'unknown')}",
        "- implemented_dense_normal_optimization: "
        f"{str(phase3.get('implemented_dense_normal_optimization', False)).lower()}",
        "- implemented_learned_near_field_reflection: "
        f"{str(phase3.get('implemented_learned_near_field_reflection', False)).lower()}",
        "",
        "## Decision Checks",
        "",
    ]

    for name in sorted(decision_checks):
        lines.append(f"- {name}: {str(decision_checks[name]).lower()}")

    lines.extend(
        [
            "",
            "## Oracle Mask Status",
            "",
            f"- routing_beats_oracle_mask: {str(routing_oracle).lower()}",
            f"- oracle mask exclusion leakage: {oracle_leakage}",
            f"- normal refinement plus routing leakage: {routing_leakage}",
        ]
    )

    if routing_oracle is False:
        lines.append(
            "- inference: routing does not beat oracle mask exclusion on this "
            "leakage metric and must be interpreted against noisy-mask, albedo, "
            "UV seam, or normal-accuracy evidence."
        )

    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
