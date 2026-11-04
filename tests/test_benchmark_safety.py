
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from kernel_opt.backends.base import NotConfiguredAdapter
class T(unittest.TestCase):
 def test_no_device_is_not_available(self): self.assertEqual(NotConfiguredAdapter().benchmark({}, {}, 1)["status"],"NOT_CONFIGURED")
