import sys
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from datamind.pilot import MedianIndicators, GuardedModel, allowed, load_development, threshold95, combine, choose_C
from datamind.evaluation import cluster_intervals, paired, metrics
CFG={"solver":"lbfgs","max_iter":3000,"tol":1e-6,"seed":20261104}
class PilotTests(unittest.TestCase):
    def test_paired_bootstrap_uses_common_complete_cohort(self):
        frame=pd.DataFrame({"patient_id":[1,1,2,3],"y":[0,1,0,1],"complete":[True,True,False,False],
                            "E2-C":[.2,.8,.99,.01],"E2":[.2,.8,.01,.99]})
        result=cluster_intervals(frame,["E2-C","E2"],50,7,False)
        ci=result["paired_brier"]["E2-C minus E2"]
        self.assertEqual(ci["low"],0)
        self.assertEqual(ci["high"],0)
        self.assertEqual(paired(frame,"E2-C","E2",frame.complete)["delta_brier"],0)
    def test_metrics_known_probabilities(self):
        r=metrics([0,1],[.2,.8])
        self.assertAlmostEqual(r["brier"],.04)
        self.assertEqual(r["roc_auc"],1)
        self.assertEqual(r["sensitivity"],1)
    def test_imputer_train_only_empty_zero_and_fixed_indicators(self):
        t=MedianIndicators(True,True).fit([[0,np.nan],[2,np.nan],[4,np.nan]])
        np.testing.assert_equal(t.statistics_,[2,0])
        before=t.statistics_.copy()
        out=t.transform([[100,7],[np.nan,np.nan]])
        np.testing.assert_equal(out,[[100,7,0,0],[2,0,1,1]])
        np.testing.assert_equal(before,t.statistics_)
    def test_complete_rejects_missing(self):
        with self.assertRaises(ValueError): MedianIndicators(False).fit([[np.nan]])
    def test_partition_guards(self):
        for fold in [9,10]:
            with self.assertRaises(ValueError):
                allowed(pd.DataFrame({"strat_fold":[fold],"ecg_id":[1]}),True)
        with self.assertRaises(ValueError):
            allowed(pd.DataFrame({"strat_fold":[10],"ecg_id":[1]}))
    def test_predict_guard_and_scaler_train_only(self):
        m=pd.DataFrame({"ecg_id":[1,2,3,4],"patient_id":[1,2,3,4],"strat_fold":[1]*4,"y":[0,0,1,1]})
        x=pd.DataFrame({"signal":[0.,1.,2.,3.]})
        model=GuardedModel("E3",1,CFG,list(x)).fit(m,x)
        np.testing.assert_equal(model.pipeline["scale"].mean_,[1.5])
        with self.assertRaises(ValueError): model.predict(m,x)
        other=m.copy()
        other.patient_id+=10
        other.strat_fold=10
        with self.assertRaises(ValueError): model.predict(other,x)
        other.strat_fold=9
        model.predict(other,x*100)
        np.testing.assert_equal(model.pipeline["scale"].mean_,[1.5])
    def test_duplicate_guard(self):
        with self.assertRaises(ValueError):
            allowed(pd.DataFrame({"ecg_id":[1,1],"strat_fold":[1,1]}))
    def test_threshold_ties_and_boundary(self):
        y=np.array([0]*20+[1,1])
        p=np.array([.1]*19+[.3,.2,.5])
        t=threshold95(y,p)
        self.assertGreaterEqual(np.mean(p[y==0]<t),.95)
        self.assertEqual(t,.2)
    def test_composition_and_C_tie(self):
        p=combine({"E1":np.array([.1,np.nan,np.nan]),"E2":np.array([.2,.3,np.nan]),"B0":np.array([.05]*3)})
        np.testing.assert_equal(p["Hybrid"],[.1,.3,.05])
        self.assertEqual(choose_C({.01:.1000001,1:.1},1e-6),.01)
    def test_real_data_schema_disjoint_and_exclusion(self):
        m,x,a=load_development(ROOT)
        self.assertEqual(x.shape,(19601,531))
        self.assertNotIn(10,set(m.strat_fold))
        self.assertEqual(m.groupby("patient_id").strat_fold.nunique().max(),1)
        self.assertEqual(a["duplicate_feature_profiles_dev"],0)
        for field in ["scp_codes","report","patient_id","ecg_id","heart_axis"]:
            self.assertNotIn(field,x.columns)
if __name__=="__main__": unittest.main()
