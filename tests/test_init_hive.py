import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "init_hive.py"
SPEC = importlib.util.spec_from_file_location("init_hive", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class InitHiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "project with spaces"
        self.project.mkdir()
        (self.project / "source.txt").write_bytes(b"existing work\x00\xff")

    def run_cli(self, path=None):
        return subprocess.run([sys.executable, str(SCRIPT), str(path or self.project)], capture_output=True, text=True)

    def test_creates_empty_state_and_preserves_source(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        hive = self.project / "hive"
        self.assertEqual(json.loads((hive / "features.json").read_text()), [])
        config = json.loads((hive / "config.json").read_text())
        self.assertEqual(config["model_selection"], "queen")
        self.assertEqual(config["bee_names"], MODULE.DEFAULT_NAMES)
        self.assertEqual(config["capabilities"], {})
        self.assertEqual(config["max_parallel_workers"], 1)
        self.assertTrue(all((hive / name).is_dir() for name in ("briefs", "reports", "research")))
        self.assertEqual((self.project / "source.txt").read_bytes(), b"existing work\x00\xff")

    def test_partial_custom_names_keep_role_defaults(self):
        MODULE.initialize(self.project, ["queen=أطلس", "builder=Patch"])
        config = json.loads((self.project / "hive" / "config.json").read_text())
        self.assertEqual(config["bee_names"]["queen"], "أطلس")
        self.assertEqual(config["bee_names"]["builder"], "Patch")
        self.assertEqual(config["bee_names"]["inspector"], "Inspector")
        self.assertEqual(config["model_selection"], "queen")

    def test_invalid_names_rejected_before_any_write(self):
        for value in ["unknown=Name", "queen=", "queen=Line\nBreak", "queen", "queen=" + "x" * 65]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    MODULE.initialize(self.project, [value])
                self.assertFalse((self.project / "hive").exists())

    def test_cli_accepts_custom_name(self):
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.project), "--bee-name", "queen=Atlas"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        config = json.loads((self.project / "hive" / "config.json").read_text())
        self.assertEqual(config["bee_names"]["queen"], "Atlas")

    def test_reinitialization_preserves_all_state(self):
        self.assertEqual(self.run_cli().returncode, 0)
        state = self.project / "hive" / "features.json"
        state.write_text('[{"id":"F01","passes":true}]')
        before = {str(p): p.read_bytes() for p in self.project.rglob("*") if p.is_file()}
        self.assertEqual(self.run_cli().returncode, 2)
        after = {str(p): p.read_bytes() for p in self.project.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_nonexistent_project_is_not_created(self):
        missing = self.project / "absent"
        self.assertEqual(self.run_cli(missing).returncode, 2)
        self.assertFalse(missing.exists())

    def test_file_is_not_project(self):
        self.assertEqual(self.run_cli(self.project / "source.txt").returncode, 2)

    def test_hive_file_is_preserved(self):
        hive = self.project / "hive"
        hive.write_text("keep")
        self.assertEqual(self.run_cli().returncode, 2)
        self.assertEqual(hive.read_text(), "keep")

    def test_hive_symlink_is_not_followed(self):
        target = Path(self.temp.name) / "elsewhere"
        target.mkdir()
        try:
            (self.project / "hive").symlink_to(target, target_is_directory=True)
        except OSError:
            self.skipTest("Symlinks unavailable")
        self.assertEqual(self.run_cli().returncode, 2)
        self.assertEqual(list(target.iterdir()), [])

    def test_concurrent_initializers_have_one_winner(self):
        command = [sys.executable, str(SCRIPT), str(self.project)]
        processes = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        for process in processes:
            process.communicate(timeout=15)
        self.assertEqual(sorted(p.returncode for p in processes), [0, 2])
        self.assertEqual(json.loads((self.project / "hive" / "features.json").read_text()), [])

    def test_partial_failure_reports_and_preserves_project(self):
        with mock.patch.object(Path, "open", side_effect=PermissionError("simulated disk error")):
            with self.assertRaisesRegex(OSError, "Setup incomplete"):
                MODULE.initialize(self.project)
        self.assertTrue((self.project / "hive").is_dir())
        self.assertEqual((self.project / "source.txt").read_bytes(), b"existing work\x00\xff")
        self.assertEqual(self.run_cli().returncode, 2)


if __name__ == "__main__":
    unittest.main()
