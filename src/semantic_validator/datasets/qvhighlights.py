from __future__ import annotations

from pathlib import Path

from semantic_validator.jsonl import load_jsonl
from semantic_validator.models import QVAnnotation


class QVHighlightsAdapter:
    """Loads QVHighlights-compatible JSON Lines annotations.

    The adapter intentionally does not download or redistribute QVHighlights.
    Dataset acquisition and license approval are deployment responsibilities.
    """

    def load_annotations(self, annotation_path: str | Path) -> list[QVAnnotation]:
        annotations = [QVAnnotation.from_dict(raw) for raw in load_jsonl(annotation_path)]
        seen: set[int | str] = set()
        for annotation in annotations:
            if annotation.qid in seen:
                raise ValueError(f"duplicate qid: {annotation.qid}")
            seen.add(annotation.qid)
            if annotation.duration <= 0:
                raise ValueError(f"duration must be positive for qid={annotation.qid}")
            if any(window.end > annotation.duration for window in annotation.relevant_windows):
                raise ValueError(f"window exceeds duration for qid={annotation.qid}")
        return annotations

