---
name: kernel-optimization-orchestrator
description: >-
  Coordinate evidence-driven CUDA or Ascend C kernel optimization with a
  user-confirmed Orchestrator model, Kernel, Performance, Benchmark, and
  Reviewer roles, official architecture research, independent correctness,
  staged experiments, reproducible evidence, and explicit stop decisions.
---

# Kernel Optimization Orchestrator

Use this skill for building, reviewing, profiling, benchmarking, or optimizing GPU/NPU kernels. The workflow is controlled by one Orchestrator and four role agents:

- Orchestrator: uses the user-confirmed default model; selects work, assigns roles, controls experiments, updates `best_candidate_id`, and decides stop/rollback.
- Kernel Agent: implements an immutable candidate.
- Performance Agent: produces evidence and diagnosis.
- Benchmark Agent: runs independent correctness and comparable measurements.
- Reviewer Agent: accepts, rejects, requests evidence, or stops.

Before every new operator task, ask for the Orchestrator/default model and each subagent model. Then ask for vendor, backend, device SKU, architecture ID, SDK, driver, and runtime device ID. Record requested and effective models separately. If the Runtime cannot route native subagents, run roles sequentially and disclose `native_subagents=false`; never claim native routing.

Follow this gate order:

`WAIT_MODEL → WAIT_HARDWARE → ARCH_RESEARCH → OPERATOR_SPEC → BASELINE → CORRECTNESS → BENCHMARK → DIAGNOSE → ONE_FACTOR_EXPERIMENT → REVIEW → ACCEPT/ROLLBACK/STOP`

Do not generate hardware-specific code before official architecture sources and an `ArchitectureBrief`. Do not tune before an `OperatorSpec`, independent Reference, and correctness tests. Keep measured, derived, estimated, and simulated values distinct. A missing device or SDK produces `NOT_CONFIGURED`, never fabricated latency.

Read the relevant supporting material from `references/` before acting:

- [workflow](references/workflow.md), [roles](references/roles/)
- [contracts](references/contracts.md), [architecture research](references/architecture_research.md)
- [CUDA backend](references/backend_cuda.md), [Ascend C backend](references/backend_ascendc.md)
- [diagnostics](references/diagnostics.md), [stages](references/stage_playbook.md)
- [CSBMV Reviewer lessons](references/reviewer-csbmv-lessons.md)

The Orchestrator controls experiment budgets, retries, device locking, rollback, and terminal states. The Reviewer checks source-to-binary provenance, clean build, CMake registration, API/ABI and hardware identity, CSBMV complex symmetric semantics (`A=A^T`, no conjugation), original `k` versus `k_eff`, stride/padding/overflow/alias/race, independent Golden, precision contract, performance denominator and holdout independence, profile/source hashes, dead tiling fields, unrelated changes, report consistency, and artifact cleanup.
