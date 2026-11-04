import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from kernel_opt.backend_registry import BackendRegistry
class A: backend_id='mock'
class T(unittest.TestCase):
 def test_register(self): r=BackendRegistry();r.register(A());self.assertEqual(r.ids(),['mock'])
