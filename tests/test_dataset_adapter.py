from pathlib import Path
import unittest

from semantic_validator.datasets import QVHighlightsAdapter


ROOT = Path(__file__).resolve().parents[1]


class QVHighlightsAdapterTest(unittest.TestCase):
    def test_loads_synthetic_compatible_samples(self) -> None:
        annotations = QVHighlightsAdapter().load_annotations(
            ROOT / "samples" / "qvhighlights_compatible_sample.jsonl"
        )
        self.assertEqual(3, len(annotations))
        self.assertEqual("SYN-001", annotations[0].qid)
        self.assertEqual(4, len(annotations[0].relevant_clip_ids))
        self.assertFalse(annotations[0].provenance["contains_external_media"])


if __name__ == "__main__":
    unittest.main()

