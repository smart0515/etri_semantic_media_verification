import unittest

from semantic_validator.evaluation.moment import temporal_iou
from semantic_validator.models import TimeWindow


class MomentMetricTest(unittest.TestCase):
    def test_temporal_iou(self) -> None:
        left = TimeWindow(0, 10)
        right = TimeWindow(5, 15)
        self.assertAlmostEqual(1 / 3, temporal_iou(left, right))

    def test_disjoint_iou_is_zero(self) -> None:
        self.assertEqual(0.0, temporal_iou(TimeWindow(0, 2), TimeWindow(3, 5)))


if __name__ == "__main__":
    unittest.main()

