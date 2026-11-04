class BackendRegistry:
 def __init__(self): self._adapters={}
 def register(self,adapter):
  if not getattr(adapter,"backend_id",None): raise ValueError("backend_id required")
  self._adapters[adapter.backend_id]=adapter
 def get(self,backend_id): return self._adapters[backend_id]
 def ids(self): return sorted(self._adapters)
