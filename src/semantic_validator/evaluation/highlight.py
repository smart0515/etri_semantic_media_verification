from __future__ import annotations

from collections.abc import Iterable

from semantic_validator.models import Prediction, QVAnnotation


def _average_precision_binary(labels: list[int], scores: list[float]) -> float:
    positives = sum(labels)
    if positives == 0:
        return 0.0
    ranked = sorted(range(len(scores)), key=lambda index: scores[index], reverse=True)
    hits = 0
    precision_sum = 0.0
    for rank, index in enumerate(ranked, start=1):
        if labels[index]:
            hits += 1
            precision_sum += hits / rank
    return precision_sum / positives


def evaluate_highlight_detection(
    annotations: Iterable[QVAnnotation],
    predictions: Iterable[Prediction],
    positive_thresholds: list[int] | None = None,
) -> dict[str, object]:
    thresholds = positive_thresholds or [2, 3, 4]
    gt_by_qid = {annotation.qid: annotation for annotation in annotations}
    pred_by_qid = {prediction.qid: prediction for prediction in predictions}
    names = {2: "Fair", 3: "Good", 4: "VeryGood"}
    result: dict[str, object] = {}

    for threshold in thresholds:
        ap_scores: list[float] = []
        hit_scores: list[float] = []
        for qid, annotation in gt_by_qid.items():
            prediction = pred_by_qid[qid]
            clip_count = max(1, int(annotation.duration / 2))
            worker_labels = [[0] * clip_count for _ in range(3)]
            for clip_id, scores in zip(annotation.relevant_clip_ids, annotation.saliency_scores):
                if clip_id >= clip_count:
                    continue
                for worker_index, score in enumerate(scores):
                    worker_labels[worker_index][clip_id] = int(score >= threshold)

            predicted_scores = list(prediction.pred_saliency_scores[:clip_count])
            predicted_scores.extend([0.0] * (clip_count - len(predicted_scores)))
            for labels in worker_labels:
                ap_scores.append(_average_precision_binary(labels, predicted_scores))
            best_index = max(range(clip_count), key=lambda index: predicted_scores[index])
            hit_scores.append(float(any(labels[best_index] for labels in worker_labels)))

        label = names.get(threshold, str(threshold))
        result[f"HL-min-{label}"] = {
            "HL-mAP": round(100 * sum(ap_scores) / len(ap_scores), 4),
            "HL-Hit1": round(100 * sum(hit_scores) / len(hit_scores), 4),
        }
    return result

