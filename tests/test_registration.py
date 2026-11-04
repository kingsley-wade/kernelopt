import json,unittest
from pathlib import Path
class T(unittest.TestCase):
 def test_report_shape(self):
  p=Path(__file__).parents[1]/'registration_report.json'
  if p.exists(): self.assertIn('native_subagents',json.loads(p.read_text()))
