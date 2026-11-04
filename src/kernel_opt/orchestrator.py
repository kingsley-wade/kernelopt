from .model_router import ModelRouter
from .research import architecture_gate
from .run_controller import RunController

class Orchestrator:
    """Single workflow controller and sole writer of best_candidate_id."""
    def __init__(self, model_router=None, store=None, controller=None):
        self.models = model_router or ModelRouter()
        self.store = store
        self.controller = controller or RunController()
        self.state = "WAIT_MODEL"
        self.best_candidate_id = None
        self._target = None
        self._run = None

    def intake(self, models, target):
        self.state = "WAIT_MODEL"
        routing = self.models.confirm(models)
        self.state = "WAIT_HARDWARE"
        required = ("vendor", "backend", "device_sku", "architecture_id", "sdk_version")
        if any(not target.get(k) for k in required):
            return {"state": self.state, "model": routing, "status": "WAIT_HARDWARE"}
        self.state = "ARCH_RESEARCH"
        self._target = dict(target)
        return {"state": self.state, "model": routing, "target": self._target}

    def start(self, models, target, sources):
        out = self.intake(models, target)
        if out.get("status") == "WAIT_HARDWARE":
            return out
        result = architecture_gate(target, sources)
        self.state = result["status"]
        if self.state == "ARCH_RESEARCH_COMPLETE":
            self.state = "OPERATOR_SPEC"
        out["architecture"] = result
        return out

    def accept_operator_spec(self, spec_id, reference_id, correctness_tests):
        if self.state != "OPERATOR_SPEC":
            raise RuntimeError("OperatorSpec gate is not open")
        if not (spec_id and reference_id and correctness_tests):
            raise ValueError("OperatorSpec, independent reference and correctness tests are required")
        self.state = "BASELINE"
        return {"state": self.state, "spec_id": spec_id, "reference_id": reference_id}

    def record_correctness(self, passed):
        if self.state not in ("BASELINE", "CORRECTNESS_GATE"):
            raise RuntimeError("baseline correctness is not active")
        self.state = "BENCHMARK" if passed else "FAILED_CORRECTNESS"
        return self.state

    def begin_experiment(self, proposal):
        if self.state not in ("BENCHMARK", "DIAGNOSE", "REVIEW", "ACCEPTED"):
            raise RuntimeError("cannot begin an experiment in current state")
        if not self.controller.allow_experiment():
            self.state = "STOPPED_BUDGET"
            return {"state": self.state, "stop_reason": self.controller.stop_reason() or "STOPPED_BUDGET"}
        if not proposal.get("primary_change") or not proposal.get("rollback_plan"):
            raise ValueError("one primary change and rollback plan are required")
        self.state = "IMPLEMENT"
        return {"state": self.state, "proposal": proposal}

    def record_verification(self, compile_pass, correctness_pass):
        if self.state != "IMPLEMENT":
            raise RuntimeError("candidate implementation is not active")
        if not compile_pass or not correctness_pass:
            self.state = "ROLLBACK"
            self.controller.record_experiment(False)
            return {"state": self.state, "decision": "reject"}
        self.state = "REVIEW"
        return {"state": self.state}

    def apply_review(self, decision, candidate_id=None, gain=False):
        if self.state != "REVIEW":
            raise RuntimeError("review is not active")
        if decision == "accept":
            self.controller.record_experiment(gain)
            self.best_candidate_id = candidate_id
            self.state = "ACCEPTED"
            if self.store is not None and candidate_id is not None:
                self.store.write_best({"candidate_id": candidate_id}, "orchestrator")
        elif decision in ("reject", "measure_more", "experiment"):
            self.controller.record_experiment(False if decision == "reject" else gain)
            self.state = "DIAGNOSE"
        elif decision == "stop":
            self.state = "STOPPED"
        else:
            raise ValueError("unknown review decision")
        return {"state": self.state, "best_candidate_id": self.best_candidate_id, "stop_reason": self.controller.stop_reason()}

    def stop(self, reason):
        if reason not in ("COMPLETED", "STOPPED_BUDGET", "STOPPED_NO_GAIN", "BLOCKED_NO_HARDWARE", "BLOCKED_NO_OFFICIAL_ARCH", "FAILED_CORRECTNESS", "FAILED_REGISTRATION"):
            raise ValueError("invalid terminal reason")
        self.state = reason
        return {"state": self.state, "best_candidate_id": self.best_candidate_id}
