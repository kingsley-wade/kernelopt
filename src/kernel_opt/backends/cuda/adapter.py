import shutil,subprocess
class CudaAdapter:
 backend_id="cuda"
 def _tool(self,n): return shutil.which(n)
 def discover_devices(self):
  tool=self._tool("nvidia-smi")
  if not tool: return []
  p=subprocess.run([tool,"--query-gpu=name,driver_version","--format=csv,noheader"],capture_output=True,text=True,timeout=10)
  return [{"raw":x.strip()} for x in p.stdout.splitlines() if x.strip()]
 def probe_capabilities(self,target):
  return {"status":"READY" if self.discover_devices() else "NOT_CONFIGURED","tools":{x:bool(self._tool(x)) for x in ("nvidia-smi","nvcc","ncu\",\"nsys")}}
 def fetch_architecture_sources(self,target): return []
 def validate_kernel_design(self,spec,design): return {"status":"UNVERIFIED","reason":"requires SKU-specific official sources"}
 def _unavailable(self): return {"status":"NOT_CONFIGURED","provenance_kind":"estimated"}
 def compile(self,candidate,timeout_s): return self._unavailable()
 def run_reference_check(self,candidate,spec,timeout_s): return self._unavailable()
 def benchmark(self,candidate,plan,timeout_s): return self._unavailable()
 def profile(self,candidate,plan,timeout_s): return self._unavailable()
 def normalize_metrics(self,raw_artifacts): return []
