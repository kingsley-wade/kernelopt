
from math import isfinite
def kingman_check(data):
    keys=("arrival_rate","service_rate","ca2","cs2")
    if any(k not in data for k in keys): return {"status":"insufficient_evidence","reason":"arrival/service variability required"}
    rho=data["arrival_rate"]/data["service_rate"] if data["service_rate"] else float("inf")
    if not (0 < rho < 1): return {"status":"not_applicable","rho":rho}
    wq=(rho/(1-rho))*((data["ca2"]+data["cs2"])/2)/data["service_rate"]
    return {"status":"measured_model","rho":rho,"mean_wait":wq,"provenance_kind":"derived"}
def roofline_check(operation_count, kernel_seconds, peak, bandwidth, bytes_moved):
    if min(operation_count,kernel_seconds,peak,bandwidth,bytes_moved)<=0: return {"status":"insufficient_evidence"}
    arithmetic_intensity=operation_count/bytes_moved
    ceiling=min(peak,bandwidth*arithmetic_intensity)
    return {"status":"derived","arithmetic_intensity":arithmetic_intensity,"ceiling":ceiling,"achieved":operation_count/kernel_seconds}
