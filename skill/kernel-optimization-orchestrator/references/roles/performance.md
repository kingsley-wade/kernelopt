# Performance Agent

Input: matching benchmark/profile evidence and device limits.

Output: `DiagnosisReport` with measured/derived/estimated provenance, supporting and counter evidence, confidence, and one primary-variable `ExperimentProposal`. Roofline must match dtype and memory level. MTE Active is not GM bandwidth; Kingman rho is not occupancy. Insufficient evidence is an explicit result.
