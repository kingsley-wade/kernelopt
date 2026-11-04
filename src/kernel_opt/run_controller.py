
class RunController:
 def __init__(self,max_experiments=30,max_repairs=3,max_no_gain=4): self.max_experiments=max_experiments;self.max_repairs=max_repairs;self.max_no_gain=max_no_gain;self.experiments=0;self.repairs=0;self.no_gain=0
 def allow_experiment(self): return self.experiments<self.max_experiments and self.no_gain<self.max_no_gain
 def record_experiment(self,gain):
  self.experiments+=1; self.no_gain=0 if gain else self.no_gain+1
 def record_repair(self): self.repairs+=1; return self.repairs<=self.max_repairs
 def stop_reason(self):
  if self.experiments>=self.max_experiments:return "STOPPED_BUDGET"
  if self.no_gain>=self.max_no_gain:return "STOPPED_NO_GAIN"
  return None
