STAGES=("S0_CORRECTNESS","S1_SCALE_OUT","S2_MEMORY_ACCESS","S3_ON_CHIP_REUSE","S4_COMPUTE_REUSE","S5_PIPELINE","S6_HARDWARE_LIMIT")
def choose_stage(e):
 if not e.get("correctness_pass"): return "S0_CORRECTNESS"
 if e.get("idle_compute_units"): return "S1_SCALE_OUT"
 if e.get("high_memory_traffic"): return "S2_MEMORY_ACCESS"
 if e.get("reuse_opportunity"): return "S3_ON_CHIP_REUSE"
 if e.get("compute_reuse_opportunity"): return "S4_COMPUTE_REUSE"
 if e.get("input_wait_gap"): return "S5_PIPELINE"
 return "S6_HARDWARE_LIMIT"
