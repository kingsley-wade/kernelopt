import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from kernel_opt.research import architecture_gate
class T(unittest.TestCase):
 def test_arch_block(self): self.assertEqual(architecture_gate({},[])["status"],"BLOCKED_NO_OFFICIAL_ARCH")
