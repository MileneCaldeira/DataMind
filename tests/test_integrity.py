import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from datamind.integrity import audit, disjoint_patients, missing, unique
class IntegrityTests(unittest.TestCase):
    def test_real_inputs(self):
        a=audit(ROOT)
        self.assertEqual(a["partitions"]["train"]["exams"],17418)
        self.assertEqual(a["partitions"]["train"]["complete531"],8874)
        self.assertEqual(a["partitions"]["train"]["complete8"],17417)
    def test_patient_leak_is_rejected(self):
        with self.assertRaises(ValueError):
            disjoint_patients([{"patient_id":"1","strat_fold":"1"},{"patient_id":"1","strat_fold":"10"}])
    def test_duplicate_join_rejected(self):
        with self.assertRaises(ValueError):
            unique([{"ecg_id":"1"},{"ecg_id":"1"}],"ecg_id")
    def test_zero_is_not_missing(self):
        self.assertFalse(missing("0"))
        self.assertTrue(missing("NaN"))
if __name__=="__main__":
    unittest.main()
