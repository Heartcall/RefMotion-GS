# RefMotion-GS Agent Instructions

This directory is the active project root for RefMotion-GS. Future Codex sessions should treat these files as the persistent internal workflow:

- `ACTIVE_SCOPE.md`
- `NEXT_ACTION.md`
- `OPERATING_PROTOCOL.md`
- `DECISION_LOG.md`
- `IMPLEMENTATION_LOG.md`
- `MVP_RESULTS.md`
- `PROJECT_PLAN.md`
- `PROMPTS/*.md`

## Required Startup

1. Read `ACTIVE_SCOPE.md`.
2. Read `NEXT_ACTION.md`.
3. Read `OPERATING_PROTOCOL.md`.
4. Read the latest entries in `IMPLEMENTATION_LOG.md`, `MVP_RESULTS.md`, and `DECISION_LOG.md`.
5. Inspect the exact source, scripts, tests, and outputs named by `NEXT_ACTION.md`.
6. Continue the workflow without asking the user for a new prompt unless the stop conditions in `OPERATING_PROTOCOL.md` are met.

## Active Project Scope

The active project is **RefMotion-GS**, not full RefTex-GS.

The only defensible core claim is:

> Reflection-induced multi-view motion can supervise reflective-region normals and reduce specular leakage in texture recovery, compared with photometric and mask-only baselines.

Do not implement or claim:

- learned near-field reflection fields,
- inter-reflection residuals,
- full PBR optimization,
- relighting,
- material editing,
- mesh representation novelty,
- UV representation novelty,
- PBR representation novelty,
- Gaussian representation novelty.

Mesh, UV, baking, and Gaussian-related components are allowed only as implementation or evaluation scaffolding.

## Current Technical State

The existing MVP has completed a preliminary analytic path:

- deterministic analytic synthetic sphere renderer,
- camera and reflection geometry,
- Formulation A reflection-cycle diagnostic,
- constrained global normal-offset optimization,
- pixel-space and sphere-UV texture routing diagnostics,
- unit tests and `run_mvp_diagnostics.py`.

The current evidence supports **continue with caution**, not a paper-level success claim. The strongest unresolved issue is that normal-refinement plus routing nearly matches but does not beat oracle reflective-mask exclusion on leakage.

## Default Verification Commands

Run these after implementation changes unless `NEXT_ACTION.md` gives a narrower or broader command set:

```bash
pytest refmotion_gs_mvp/tests -q
python -m py_compile refmotion_gs_mvp/src/*.py refmotion_gs_mvp/scripts/run_mvp_diagnostics.py
python refmotion_gs_mvp/scripts/run_mvp_diagnostics.py --out-dir refmotion_gs_mvp/outputs/run_latest
```

When adding a new script, include it in the compile command. When adding a new result directory, write a markdown summary next to the metrics.

## Work Rules

- Execute only the current milestone named in `NEXT_ACTION.md`.
- Before planning a new stage, audit the current evidence and update the plan.
- Use tests for new behavior and keep generated metrics reproducible.
- Record commands, exact outputs, metrics, and inference in `IMPLEMENTATION_LOG.md` or a result file.
- Update `DECISION_LOG.md` for every milestone decision.
- Update `NEXT_ACTION.md` at the end of each session with the exact next task.
- Stop only when the next step needs user input, environment access, a scope change, a project pivot, or abandonment.

