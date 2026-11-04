
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from kernel_opt.research import architecture_gate
class T(unittest.TestCase):
 def test_complete_requires_sources(self):
  t={"vendor":"nvidia","backend":"cuda","device_sku":"x","architecture_id":"sm_x","sdk_version":"x"}
  self.assertEqual(architecture_gate(t,[])["status"],"BLOCKED_NO_OFFICIAL_ARCH")
 def test_verified_sources_pass(self):
  t={"vendor":"nvidia","backend":"cuda","device_sku":"x","architecture_id":"sm_x","sdk_version":"x"}; s=[{"url":"https://vendor.example","title":"arch","diagram_verified":True}]
  self.assertEqual(architecture_gate(t,s)["status"],"ARCH_RESEARCH_COMPLETE")
