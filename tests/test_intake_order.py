import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from kernel_opt.orchestrator import Orchestrator
from kernel_opt.model_router import ModelRouter
class T(unittest.TestCase):
 def test_model_then_hardware(self): self.assertEqual(Orchestrator(ModelRouter()).start({"orchestrator":"o","kernel":"k","performance":"p","benchmark":"b","reviewer":"r"},{"vendor":"nvidia"},[])["status"],"WAIT_HARDWARE")
