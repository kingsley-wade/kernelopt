REQUIRED_GATES=("compile_pass","correctness_pass","target_hardware_legal","benchmark_comparable","traceable_evidence")
def review(c):
 missing=[g for g in REQUIRED_GATES if c.get(g) is not True]
 if missing: return {"decision":"reject" if any(x in missing for x in ("compile_pass","correctness_pass")) else "measure_more","reason_codes":missing}
 if c.get("statistically_credible") is not True: return {"decision":"measure_more","reason_codes":["noise_or_missing_dispersion"]}
 return {"decision":"accept","reason_codes":[]}

def benchmark_denominator(cases):
    """Keep failed, skipped and invalid cases in N; only measured valid cases are K."""
    n=len(cases)
    k=sum(1 for c in cases if c.get("status") == "PASS" and c.get("target_met") is True)
    return {"N": n, "K": k, "threshold_met": 10*k >= 7*n if n else False}
