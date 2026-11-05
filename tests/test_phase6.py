import sys,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from datamind.final_eval import final_predict,claim
class FakePipeline:
    def __init__(self):self.calls=0
    def predict_proba(self,X):
        self.calls+=1
        return np.tile([.75,.25],(len(X),1))
class FinalTests(unittest.TestCase):
    def fixture(self):
        return SimpleNamespace(train_patients_={1},train_ids_={1},columns=["a"],pipeline=FakePipeline()),pd.DataFrame({"ecg_id":[2],"patient_id":[2],"strat_fold":[10]}),pd.DataFrame({"a":[1.]})
    def test_one_call_no_fit(self):
        model,m,x=self.fixture()
        np.testing.assert_equal(final_predict(model,m,x),[.25])
        self.assertEqual(model.pipeline.calls,1)
    def test_forbidden_patient_and_fold(self):
        model,m,x=self.fixture(); m.patient_id=1
        with self.assertRaises(ValueError):final_predict(model,m,x)
        m.patient_id=2; m.strat_fold=9
        with self.assertRaises(ValueError):final_predict(model,m,x)
        self.assertEqual(model.pipeline.calls,0)
    def test_alignment(self):
        model,m,x=self.fixture(); x.index=[4]
        with self.assertRaises(ValueError):final_predict(model,m,x)
    def test_exclusive_claim(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"lock";claim(p)
            with self.assertRaises(FileExistsError):claim(p)
if __name__=="__main__":unittest.main()
