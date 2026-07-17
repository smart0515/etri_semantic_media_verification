from __future__ import annotations

from collections.abc import Iterable

from semantic_validator.models import Prediction, QVAnnotation, TimeWindow


DEFAULT_IOU_THRESHOLDS = [round(0.5 + 0.05 * index, 2) for index in range(10)]


def temporal_iou(left: TimeWindow, right: TimeWindow) -> float:
    intersection = max(0.0, min(left.end, right.end) - max(left.start, right.start))
    union = max(left.end, right.end) - min(left.start, right.start)
    return 0.0 if union <= 0 else intersection / union


def _average_precision(
    predictions: list[TimeWindow], ground_truth: list[TimeWindow], threshold: float
) -> float:
    if not ground_truth:
        return 0.0
    ranked = sorted(predictions, key=lambda item: item.score or 0.0, reverse=True)
    matched: set[int] = set()
    precision_sum = 0.0
    true_positives = 0
    for rank, prediction in enumerate(ranked, start=1):
        best_index = None
        best_iou = -1.0
        for index, expected in enumerate(ground_truth):
            if index in matched:
                continue
            score = temporal_iou(prediction, expected)
            if score > best_iou:
                best_index = index
                best_iou = score
        if best_index is not None and best_iou >= threshold:
            matched.add(best_index)
            true_positives += 1
            precision_sum += true_positives / rank
    return precision_sum / len(ground_truth)


def evaluate_moment_retrieval(
    annotations: Iterable[QVAnnotation],
    predictions: Iterable[Prediction],
    iou_thresholds: list[float] | None = None,
) -> dict[str, object]:
    thresholds = iou_thresholds or DEFAULT_IOU_THRESHOLDS
    gt_by_qid = {annotation.qid: annotation for annotation in annotations}
    pred_by_qid = {prediction.qid: prediction for prediction in predictions}
    if gt_by_qid.keys() != pred_by_qid.keys():
        raise ValueError("ground-truth and prediction qids must match")

    ap_by_threshold: dict[str, float] = {}
    recall_by_threshold: dict[str, float] = {}
    for threshold in thresholds:
        aps: list[float] = []
        hits: list[float] = []
        for qid, annotation in gt_by_qid.items():
            predicted = pred_by_qid[qid].pred_relevant_windows[:10]
            aps.append(_average_precision(predicted, annotation.relevant_windows, threshold))
            top = predicted[0] if predicted else None
            hits.append(
                float(
                    top is not None
                    and any(temporal_iou(top, expected) >= threshold for expected in annotation.relevant_windows)
                )
            )
        ap_by_threshold[f"{threshold:.2f}"] = round(100 * sum(aps) / len(aps), 4)
        recall_by_threshold[f"{threshold:.2f}"] = round(100 * sum(hits) / len(hits), 4)

    return {
        "MR-mAP": {
            "average_0.50_0.95": round(sum(ap_by_threshold.values()) / len(ap_by_threshold), 4),
            "by_tIoU": ap_by_threshold,
        },
        "MR-R1": {
            "at_tIoU_0.50": recall_by_threshold.get("0.50"),
            "at_tIoU_0.70": recall_by_threshold.get("0.70"),
            "by_tIoU": recall_by_threshold,
        },
    }

