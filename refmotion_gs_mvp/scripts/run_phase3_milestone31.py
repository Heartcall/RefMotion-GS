from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

os.environ.setdefault("MPLCONFIGDIR", "/tmp/refmotion_gs_mvp_mpl")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from refmotion_gs_mvp.scripts.run_mvp_diagnostics import run as run_mvp_diagnostics
from refmotion_gs_mvp.src.decision_checks import compute_routing_decision_checks
from refmotion_gs_mvp.src.experiment_protocol import (
    phase3_milestone_metadata,
    write_summary,
)


def run(out_dir: Path) -> dict:
    """Run the Milestone 3.1 framework path without changing MVP behavior."""
    metrics = run_mvp_diagnostics(out_dir)
    uv_leakage = metrics["uv_texture_baking"]["specular_leakage_score"]
    metrics["decision_checks"].update(compute_routing_decision_checks(uv_leakage))
    metrics["phase3"] = phase3_milestone_metadata(
        milestone="3.1",
        purpose="experiment_framework_refactor",
    )

    with (out_dir / "metrics.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    write_summary(out_dir / "summary.md", metrics)
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out-dir",
        default="refmotion_gs_mvp/outputs/phase3/milestone_31_framework",
    )
    args = parser.parse_args()

    metrics = run(Path(args.out_dir))
    print(json.dumps(metrics["decision_checks"], indent=2))


if __name__ == "__main__":
    main()
