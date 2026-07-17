from __future__ import annotations

from semantic_validator.models import Prediction, QVAnnotation, TimeWindow


class ReferenceMockPredictor:
    """Produces deterministic mock output for data-flow verification only.

    This class uses reference annotations and therefore must never be described
    as a learned model or as evidence of target-system performance.
    """

    result_status = "PRELIMINARY_MOCK"

    def predict(self, annotation: QVAnnotation) -> Prediction:
        windows: list[TimeWindow] = []
        for index, reference in enumerate(annotation.relevant_windows):
            start = min(reference.end - 0.1, reference.start + 0.25)
            end = max(start + 0.1, reference.end - 0.25)
            windows.append(TimeWindow(start, end, max(0.5, 0.95 - 0.1 * index)))

        clip_count = max(1, int(annotation.duration / 2))
        saliency = [0.0] * clip_count
        for clip_id, worker_scores in zip(
            annotation.relevant_clip_ids, annotation.saliency_scores
        ):
            if clip_id < clip_count:
                saliency[clip_id] = sum(worker_scores) / len(worker_scores)

        return Prediction(
            qid=annotation.qid,
            query=annotation.query,
            vid=annotation.vid,
            pred_relevant_windows=windows,
            pred_saliency_scores=saliency,
            result_status=self.result_status,
            metadata={
                "generator": "ReferenceMockPredictor",
                "uses_ground_truth": True,
                "purpose": "schema_and_metric_flow_verification_only",
            },
        )

