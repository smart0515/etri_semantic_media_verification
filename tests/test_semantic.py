from __future__ import annotations

import copy
import unittest
from pathlib import Path

from semantic_validator.evaluation import evaluate_semantic_structure, normalize_label
from semantic_validator.jsonl import load_jsonl
from semantic_validator.models import SemanticExtension


ROOT = Path(__file__).resolve().parents[1]


class SemanticEvaluationTest(unittest.TestCase):
    def setUp(self) -> None:
        rows = load_jsonl(ROOT / "samples" / "etri_semantic_extension_sample.jsonl")
        self.references = [SemanticExtension.from_dict(row) for row in rows]

    def test_normalize_label(self) -> None:
        self.assertEqual("playing basketball", normalize_label(" Playing-Basketball "))

    def test_exact_semantic_structure_scores_one_hundred(self) -> None:
        result = evaluate_semantic_structure(self.references, self.references)
        self.assertEqual(100.0, result["elements"]["f1"])
        self.assertEqual(100.0, result["relations"]["f1"])

    def test_missing_relation_reduces_recall(self) -> None:
        candidates = copy.deepcopy(self.references)
        candidates[0].relations.pop()
        result = evaluate_semantic_structure(self.references, candidates)
        self.assertLess(result["relations"]["recall"], 100.0)


if __name__ == "__main__":
    unittest.main()
