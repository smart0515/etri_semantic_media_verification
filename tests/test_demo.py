from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from semantic_validator.cli import run_demo


ROOT = Path(__file__).resolve().parents[1]


class PreliminaryDemoTest(unittest.TestCase):
    def test_demo_generates_disclaimed_result(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            result = run_demo(
                ROOT / "samples" / "qvhighlights_compatible_sample.jsonl",
                ROOT / "samples" / "etri_semantic_extension_sample.jsonl",
                target,
            )
            self.assertEqual("PRELIMINARY_MOCK", result["result_status"])
            self.assertIn("not an ETRI target-system", result["disclaimer"])
            self.assertTrue((target / "mock_predictions.jsonl").exists())
            self.assertTrue((target / "reassembly_plans.jsonl").exists())
            self.assertTrue((target / "preliminary_evaluation.json").exists())
            integrity = result["metrics"]["semantic_relation_integrity"]
            self.assertEqual(100.0, integrity["relation_integrity_percent"])


if __name__ == "__main__":
    unittest.main()

