
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from kernel_opt.diagnostics import kingman_check
class T(unittest.TestCase):
 def test_insufficient(self): self.assertEqual(kingman_check({})["status"],"insufficient_evidence")
 def test_not_applicable(self): self.assertEqual(kingman_check({"arrival_rate":2,"service_rate":1,"ca2":1,"cs2":1})["status"],"not_applicable")
