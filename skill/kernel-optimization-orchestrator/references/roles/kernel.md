# Kernel Agent

Input: `OperatorSpec`, `ArchitectureBrief`, and `ExperimentProposal`.

Output: immutable `CandidateArtifact`, source hash, build log, resource/synchronization plan, assumptions, and rollback parent. The agent may edit implementation files for its candidate. It may not edit the Golden, thresholds, frozen manifest, Reviewer decision, or `best_candidate_id`.
