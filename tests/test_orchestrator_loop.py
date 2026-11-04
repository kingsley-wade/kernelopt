import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'src'))
from kernel_opt.orchestrator import Orchestrator
from kernel_opt.model_router import ModelRouter

class T(unittest.TestCase):
    def setUp(self):
        self.o = Orchestrator(ModelRouter(routing_supported=False))
        self.models = {"orchestrator":"o","kernel":"k","performance":"p","benchmark":"b","reviewer":"r"}
        self.target = {"vendor":"nvidia","backend":"cuda","device_sku":"x","architecture_id":"sm_x","sdk_version":"x"}
        self.sources = [{"url":"https://vendor.example/arch","title":"Architecture","diagram_verified":True}]
    def test_loop_and_best_writer(self):
        self.o.start(self.models, self.target, self.sources)
        self.o.accept_operator_spec("spec-1", "ref-1", ["case-1"])
        self.assertEqual(self.o.record_correctness(True), "BENCHMARK")
        self.o.begin_experiment({"primary_change":"tile","rollback_plan":"restore-parent"})
        self.assertEqual(self.o.record_verification(True, True)["state"], "REVIEW")
        self.assertEqual(self.o.apply_review("accept", "candidate-1", gain=True)["best_candidate_id"], "candidate-1")

if __name__ == '__main__': unittest.main()
