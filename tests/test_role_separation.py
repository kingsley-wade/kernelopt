import sys,unittest,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from kernel_opt.state_store import StateStore
class T(unittest.TestCase):
 def test_only_orchestrator(self):
  with self.assertRaises(PermissionError): StateStore(Path(tempfile.gettempdir())/'ko-state.jsonl').write_best({},'kernel')
