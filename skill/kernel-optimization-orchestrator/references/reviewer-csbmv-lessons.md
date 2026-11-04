# CSBMV Reviewer lessons

Require a locked base SHA, target branch, and complete staged diff. Reject untracked-file ambiguity, incremental-only binaries, stale test logs, CMake discovery mismatches, unverified API/ABI or hardware identity, and unrelated cross-architecture edits.

For semantics, require complex symmetric `A=A^T` without Hermitian conjugation; separate UPPER/LOWER, original `k`, and `k_eff`; verify physical diagonal position, negative stride, `k>=n`, padding, complex element size, overflow, alias, quick return, and race behavior.

The Golden must be independent of kernel band indexing and include dense reconstruction, nonzero imaginary parts, and wrong-conjugation killers. Precision rules, MERE/MARE, near-zero, Inf/NaN, strict inequalities, performance freeze, timing boundaries, warmups, samples, seeds, and `10*K >= 7*N` must match the formal report. Failures and NOT_RUN cases remain in the denominator. Holdout must be frozen and independent. Profile evidence must match current source and binary hashes. Dead tiling fields, rejected-candidate rollback, report/log consistency, and cleanup manifest are mandatory checks.
