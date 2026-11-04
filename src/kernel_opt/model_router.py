class ModelRouter:
 def __init__(self,runtime_default="runtime-default",routing_supported=False): self.runtime_default=runtime_default; self.routing_supported=routing_supported
 def confirm(self,requested):
  required=("orchestrator","kernel","performance","benchmark","reviewer"); missing=[x for x in required if not requested.get(x)]
  if missing: raise ValueError("model confirmation missing: "+", ".join(missing))
  effective=dict(requested) if self.routing_supported else {k:self.runtime_default for k in required}
  return {"requested":dict(requested),"effective":effective,"model_routing_supported":self.routing_supported,"disclosure":"native routing unavailable; sequential role fallback" if not self.routing_supported else "native role routing"}
