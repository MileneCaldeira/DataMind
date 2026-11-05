"""Strictly non-predictive fixtures. Run only this file, not the legacy full suite."""
import hashlib
import importlib.util
import tempfile
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


verify = module("verify_preservation")
backup = module("backup_project")


class PreservationTests(unittest.TestCase):
    def test_exact_hash_and_tampering(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "file").write_bytes(b"original")
            entries = {"file": verify.digest(root / "file")}
            self.assertEqual(verify.verify_entries(root, entries), 1)
            (root / "file").write_bytes(b"changed")
            with self.assertRaises(ValueError):
                verify.verify_entries(root, entries)

    def test_history_requires_exact_registered_transition(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "doc").write_bytes(b"current")
            before = {"doc": hashlib.sha256(b"old").hexdigest()}
            changes = {"doc": {"before_sha256": before["doc"],
                              "current_sha256": verify.digest(root / "doc"),
                              "epoch": "maintenance", "recovered_utf8": "old"}}
            result = verify.verify_history(root, before, changes)
            self.assertEqual(result["old_bytes_recovered"], ["doc"])
            (root / "doc").write_bytes(b"unexpected")
            with self.assertRaises(ValueError):
                verify.verify_history(root, before, changes)

    def test_unregistered_history_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "doc").write_bytes(b"new")
            with self.assertRaises(ValueError):
                verify.verify_history(root, {"doc": "0" * 64}, {})

    def test_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                verify.local(Path(d), "../outside")

    def test_cli_refuses_same_physical_disk(self):
        with tempfile.TemporaryDirectory() as d:
            with mock.patch.object(backup, "physical_disk", return_value=0):
                with mock.patch("sys.argv", ["backup", "--destination", d, "--authorized-destination"]):
                    with mock.patch.object(backup, "copy_snapshot") as copy:
                        with self.assertRaises(SystemExit):
                            backup.main()
                        copy.assert_not_called()

    def test_recovered_history_tamper_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root / "doc").write_bytes(b"current")
            before = {"doc": hashlib.sha256(b"old").hexdigest()}
            changes = {"doc": {"before_sha256": before["doc"],
                              "current_sha256": verify.digest(root / "doc"),
                              "epoch": "maintenance", "recovered_utf8": "tampered"}}
            with self.assertRaises(ValueError):
                verify.verify_history(root, before, changes)

    def test_backup_copy_restore_and_tamper(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); source = root / "source"; dest = root / "dest"
            source.mkdir(); dest.mkdir()
            (source / "record.json").write_text('{"fixture": true}', encoding="utf-8")
            (source / "nested").mkdir()
            (source / "nested" / "bytes").write_bytes(bytes(range(256)))
            first, receipt = backup.copy_snapshot(source, dest, critical=["record.json"])
            second, _ = backup.copy_snapshot(source, dest, critical=["record.json"])
            self.assertNotEqual(first, second)
            self.assertEqual(receipt["files"], 2)
            self.assertTrue((first / "restore_check/record.json").is_file())
            (first / "project/nested/bytes").write_bytes(b"tampered")
            with self.assertRaises(ValueError):
                backup.verify_copy(first / "project", receipt["hashes"])

    def test_backup_inside_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d); dest = source / "backup"; dest.mkdir()
            with self.assertRaises(ValueError):
                backup.copy_snapshot(source, dest, critical=[])

    def test_essential_excludes_only_named_environments(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d)
            (source / ".venv-phase5").mkdir()
            (source / ".venv-phase5/package").write_bytes(b"fixture")
            (source / "data").mkdir()
            (source / "data/original").write_bytes(b"keep")
            self.assertEqual(set(backup.inventory(source, True)), {"data/original"})


if __name__ == "__main__":
    unittest.main()
