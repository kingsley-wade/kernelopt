import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'src'))
from kernel_opt.contracts import ContractError, validate_operator_spec
class T(unittest.TestCase):
    def base(self): return {"op":"GEMM","formula":"C[m,n]=sum_k A[m,k]B[k,n]","inputs":["A","B"],"outputs":["C"],"shapes":{"M":2,"N":3,"K":4},"numerics":{"acc":"fp32"},"reference_impl":"independent","test_cases":["small"],"reduction_axis":"K","output_axes":["M","N"]}
    def test_k_reduction(self): validate_operator_spec(self.base())
    def test_wrong_axis_rejected(self):
        x=self.base(); x["reduction_axis"]="M"
        with self.assertRaises(ContractError): validate_operator_spec(x)
