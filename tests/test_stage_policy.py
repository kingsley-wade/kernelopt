import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from kernel_opt.stages import choose_stage
class T(unittest.TestCase):
 def test_first(self): self.assertEqual(choose_stage({}),"S0_CORRECTNESS")
 def test_memory(self): self.assertEqual(choose_stage({"correctness_pass":True,"high_memory_traffic":True}),"S2_MEMORY_ACCESS")
