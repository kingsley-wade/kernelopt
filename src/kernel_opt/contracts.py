from datetime import datetime, timezone
from typing import Any
COMMON={"schema_version","run_id","artifact_id","created_at","producer_role","evidence_ids","status","provenance_kind"}
PROVENANCE={"measured","derived","estimated","simulated"}
ROLES={"orchestrator","kernel","performance","benchmark","reviewer","system"}
class ContractError(ValueError): pass
def now_iso(): return datetime.now(timezone.utc).isoformat()
def make_artifact(kind,run_id,producer_role,status,*,evidence_ids=None,provenance_kind="derived",**fields):
 if producer_role not in ROLES: raise ContractError("unknown producer_role")
 if provenance_kind not in PROVENANCE: raise ContractError("unknown provenance_kind")
 d={"schema_version":"1.0","run_id":run_id,"artifact_id":f"{kind}-{run_id}","created_at":now_iso(),"producer_role":producer_role,"evidence_ids":list(evidence_ids or []),"status":status,"provenance_kind":provenance_kind}; d.update(fields); return d
def validate_contract(obj,required=None,allowed=None):
 if not isinstance(obj,dict): raise ContractError("contract must be an object")
 if COMMON-set(obj): raise ContractError(f"missing common fields: {sorted(COMMON-set(obj))}")
 if obj["provenance_kind"] not in PROVENANCE or obj["producer_role"] not in ROLES: raise ContractError("invalid common field")
 if not isinstance(obj["evidence_ids"],list): raise ContractError("evidence_ids must be list")
 if required and not set(required).issubset(obj): raise ContractError(f"missing fields: {sorted(set(required)-set(obj))}")
 if allowed is not None and set(obj)-set(allowed): raise ContractError(f"unknown fields: {sorted(set(obj)-set(allowed))}")
def validate_run_request(obj):
 validate_contract(obj,{"requested_agent_model","effective_agent_model","backend","device_sku","sdk_version","objective","budget"})
 if not obj.get("requested_agent_model") or not obj.get("backend"): raise ContractError("model and backend must be confirmed")
def validate_candidate(obj):
 validate_contract(obj,{"candidate_id","parent_id","source_hash","code_paths","build_log_id","design_id","change_set"})
 if not isinstance(obj["code_paths"],list): raise ContractError("code_paths must be a list")

def validate_operator_spec(spec):
    """Reject ambiguous specs before benchmark; GEMM K must be the reduction axis."""
    if not isinstance(spec, dict):
        raise ContractError("OperatorSpec must be an object")
    for field in ("formula", "inputs", "outputs", "shapes", "numerics", "reference_impl", "test_cases"):
        if not spec.get(field):
            raise ContractError(f"OperatorSpec missing {field}")
    if spec.get("op") == "GEMM":
        if spec.get("reduction_axis") != "K":
            raise ContractError("GEMM reduction_axis must be K")
        if spec.get("output_axes") != ["M", "N"]:
            raise ContractError("GEMM output axes must be M,N")
