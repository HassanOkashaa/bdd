import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from init_hive import initialize
from validate_hive import validate


class ValidateHiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        initialize(self.project)
        self.feature = {"id": "F01", "description": "Save URLs", "depends_on": [], "acceptance": ["Duplicate stays single"], "status": "pending", "passes": False, "evidence": [], "blocked_reason": None}

    def write_features(self, features):
        (self.project / "hive/features.json").write_text(json.dumps(features))

    def test_initialized_and_pending_state_are_valid(self):
        self.assertEqual(validate(self.project), [])
        self.write_features([self.feature])
        self.assertEqual(validate(self.project), [])

    def test_rejects_observed_manual_fallback_drift_without_mutation(self):
        self.write_features({"features": [self.feature]})
        path = self.project / "hive/config.json"
        config = json.loads(path.read_text())
        config["budgets"] = {"repair_rounds_per_feature": config.pop("max_repair_rounds_per_feature")}
        del config["bee_names"]["scout"]
        path.write_text(json.dumps(config))
        before = {str(p): p.read_bytes() for p in self.project.rglob("*") if p.is_file()}
        errors = validate(self.project)
        self.assertGreaterEqual(len(errors), 3)
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.project.rglob("*") if p.is_file()})

    def test_pass_needs_consistent_status_and_evidence(self):
        for status, passed in [("passed", False), ("pending", True), ("passed", True)]:
            with self.subTest(status=status, passed=passed):
                feature = dict(self.feature, status=status, passes=passed)
                self.write_features([feature])
                self.assertTrue(validate(self.project))
        feature = dict(self.feature, status="passed", passes=True, evidence=[{"criterion": "Duplicate stays single", "command": "python3 -m unittest", "result": "pass", "revision": "fixture-v1", "report": "hive/reports/test.md"}])
        self.write_features([feature])
        self.assertEqual(validate(self.project), [])

    def test_unknown_duplicate_and_cyclic_dependencies_are_rejected(self):
        cases = [[dict(self.feature, depends_on=["absent"])], [self.feature, self.feature], [dict(self.feature, depends_on=["F02"]), dict(self.feature, id="F02", depends_on=["F01"])]]
        for features in cases:
            self.write_features(features)
            self.assertTrue(validate(self.project))

    def test_boolean_budgets_and_blocked_without_reason_are_rejected(self):
        path = self.project / "hive/config.json"
        config = json.loads(path.read_text()); config["max_parallel_workers"] = True
        path.write_text(json.dumps(config))
        self.write_features([dict(self.feature, status="blocked")])
        self.assertGreaterEqual(len(validate(self.project)), 2)

    def test_bad_json_and_wrong_types_report_errors(self):
        path = self.project / "hive/features.json"
        path.write_text("not json")
        self.assertTrue(validate(self.project))
        self.write_features([None, dict(self.feature, id=[], status=[]), dict(self.feature, depends_on=[{}])])
        self.assertTrue(validate(self.project))

    def test_cli_failure_exit_code(self):
        self.write_features({"features": []})
        result = subprocess.run([sys.executable, str(SCRIPTS / "validate_hive.py"), str(self.project)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("top-level array", result.stderr)

    def test_duplicate_keys_deep_nesting_and_nonstandard_constants_fail_cleanly(self):
        path = self.project / "hive/config.json"
        original = path.read_text()
        cases = [original.replace('"schema_version": 1', '"schema_version": 2, "schema_version": 1'), '[' * 10000 + ']' * 10000, original.replace('"capabilities": {}', '"capabilities": {"bad": NaN}')]
        for content in cases:
            with self.subTest(prefix=content[:40]):
                path.write_text(content)
                result = subprocess.run([sys.executable, str(SCRIPTS / "validate_hive.py"), str(self.project)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(path.read_text(), content)
