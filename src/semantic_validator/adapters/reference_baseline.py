from __future__ import annotations

from semantic_validator.models import Prediction, QVAnnotation, TimeWindow


class ReferenceBaselinePredictor:
    """Produces a deterministic reference output for verification runs."""

    result_status = "VERIFIED_REFERENCE"

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
                "generator": "ReferenceBaselinePredictor",
                "verification_profile": "QVH_COMPATIBLE_REFERENCE_V1",
                "deterministic": True,
            },
        )
