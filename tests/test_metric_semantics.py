import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'src'))
from kernel_opt.diagnostics import roofline_check
class T(unittest.TestCase):
    def test_roofline_is_derived(self):
        x=roofline_check(100, 1, 200, 10, 20)
        self.assertEqual(x['status'], 'derived'); self.assertIn('arithmetic_intensity', x)
