from pathlib import Path
import json,os,tempfile
class StateStore:
 def __init__(self,path): self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
 def append(self,event):
  with self.path.open("a",encoding="utf-8") as f: f.write(json.dumps(event,sort_keys=True)+"\n")
 def events(self): return [json.loads(x) for x in self.path.read_text().splitlines() if x.strip()] if self.path.exists() else []
 def write_best(self,candidate,writer_role):
  if writer_role!="orchestrator": raise PermissionError("only orchestrator may update best_candidate")
  target=self.path.with_suffix('.best.json'); fd,tmp=tempfile.mkstemp(dir=target.parent,prefix='.best-',text=True)
  with os.fdopen(fd,'w',encoding='utf-8') as f: json.dump(candidate,f,indent=2,sort_keys=True)
  os.replace(tmp,target)
