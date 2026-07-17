from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from semantic_validator.cli import run_demo


ROOT = Path(__file__).resolve().parents[1]


class ReferenceVerificationTest(unittest.TestCase):
    def test_verification_generates_complete_result_set(self) -> None:
        with TemporaryDirectory() as directory:
            target = Path(directory)
            result = run_demo(
                ROOT / "samples" / "qvhighlights_compatible_sample.jsonl",
                ROOT / "samples" / "etri_semantic_extension_sample.jsonl",
                target,
            )
            self.assertEqual("VERIFIED_REFERENCE", result["result_status"])
            self.assertIn("verification completed", result["summary"])
            self.assertTrue((target / "predictions.jsonl").exists())
            self.assertTrue((target / "reassembly_plans.jsonl").exists())
            self.assertTrue((target / "evaluation_result.json").exists())
            integrity = result["metrics"]["semantic_relation_integrity"]
            self.assertEqual(100.0, integrity["relation_integrity_percent"])


if __name__ == "__main__":
    unittest.main()
