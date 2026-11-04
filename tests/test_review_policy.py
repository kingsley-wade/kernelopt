import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from kernel_opt.review_policy import review
class T(unittest.TestCase):
 def test_correctness_blocks(self): self.assertEqual(review({'compile_pass':True})['decision'],'reject')
