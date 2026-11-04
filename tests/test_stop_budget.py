import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'src'))
from kernel_opt.run_controller import RunController
class T(unittest.TestCase):
    def test_budget_and_no_gain(self):
        c=RunController(max_experiments=2,max_no_gain=2)
        c.record_experiment(False); self.assertTrue(c.allow_experiment())
        c.record_experiment(False); self.assertEqual(c.stop_reason(), 'STOPPED_BUDGET')
