import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from kernel_opt.backends.cuda.adapter import CudaAdapter
class T(unittest.TestCase):
 def test_no_fake_latency(self): self.assertIn(CudaAdapter().benchmark({}, {}, 1)['status'],('NOT_CONFIGURED','READY'))
