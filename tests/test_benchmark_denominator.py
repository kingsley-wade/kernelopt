import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'src'))
from kernel_opt.review_policy import benchmark_denominator
class T(unittest.TestCase):
    def test_failures_stay_in_denominator(self):
        x=benchmark_denominator([{'status':'PASS','target_met':True},{'status':'FAIL'},{'status':'NOT_RUN'}])
        self.assertEqual((x['K'],x['N']),(1,3)); self.assertFalse(x['threshold_met'])
