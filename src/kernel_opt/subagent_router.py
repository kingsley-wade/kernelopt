class SubagentRouter:
 def __init__(self,native_dispatch=None): self.native_dispatch=native_dispatch
 @property
 def native_subagents(self): return self.native_dispatch is not None
 def run(self,role,payload,handler=None):
  if self.native_dispatch: return self.native_dispatch(role,payload)
  if handler is None: raise ValueError("fallback requires a role handler")
  return {"role":role,"native_subagents":False,"result":handler(payload)}
