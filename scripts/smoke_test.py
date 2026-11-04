import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from kernel_opt.model_router import ModelRouter
from kernel_opt.orchestrator import Orchestrator
from kernel_opt.research import architecture_gate
from kernel_opt.subagent_router import SubagentRouter
from kernel_opt.review_policy import review
models={"orchestrator":"default","kernel":"k","performance":"p","benchmark":"b","reviewer":"r"}
assert ModelRouter(runtime_default="runtime-default").confirm(models)["effective"]["kernel"]=="runtime-default"
assert Orchestrator(ModelRouter()).start(models,{"vendor":"nvidia"},[])["status"]=="WAIT_HARDWARE"
assert architecture_gate({},[])["status"]=="BLOCKED_NO_OFFICIAL_ARCH"
assert SubagentRouter().run("reviewer",{},lambda p:{"ok":True})["native_subagents"] is False
assert review({"compile_pass":False})["decision"]=="reject"
print("dry-run mock: PASS (no hardware metrics fabricated)")
