import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from kernel_opt.contracts import *
class T(unittest.TestCase):
 def test_required(self): validate_run_request(make_artifact("run","r","orchestrator","new",requested_agent_model="m",effective_agent_model="m",backend="mock",device_sku="d",sdk_version="s",objective="x",budget={}))
 def test_bad_provenance(self):
  with self.assertRaises(ContractError): make_artifact("x","r","system","new",provenance_kind="fake")
