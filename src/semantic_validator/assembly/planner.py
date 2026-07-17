from __future__ import annotations

from semantic_validator.models import Prediction


def build_reassembly_plan(prediction: Prediction, clip_length_seconds: int = 2) -> dict[str, object]:
    selected_units: list[dict[str, object]] = []
    for rank, window in enumerate(
        sorted(prediction.pred_relevant_windows, key=lambda item: item.start), start=1
    ):
        first_clip = int(window.start // clip_length_seconds)
        last_clip = max(first_clip, int((window.end - 1e-9) // clip_length_seconds))
        for clip_id in range(first_clip, last_clip + 1):
            selected_units.append(
                {
                    "source_clip_id": clip_id,
                    "start_seconds": clip_id * clip_length_seconds,
                    "end_seconds": (clip_id + 1) * clip_length_seconds,
                    "source_window_rank": rank,
                }
            )
    unique_units = {unit["source_clip_id"]: unit for unit in selected_units}
    return {
        "qid": prediction.qid,
        "vid": prediction.vid,
        "policy": "chronological_deduplicated",
        "result_status": prediction.result_status,
        "selected_units": [unique_units[key] for key in sorted(unique_units)],
        "note": "Reference assembly plan generated from verified moment predictions.",
    }
