from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class TimeWindow:
    start: float
    end: float
    score: float | None = None

    def __post_init__(self) -> None:
        if self.start < 0:
            raise ValueError("window start must be non-negative")
        if self.end <= self.start:
            raise ValueError("window end must be greater than start")

    def as_list(self) -> list[float]:
        values = [float(self.start), float(self.end)]
        if self.score is not None:
            values.append(float(self.score))
        return values


@dataclass
class QVAnnotation:
    qid: int | str
    query: str
    duration: float
    vid: str
    relevant_windows: list[TimeWindow]
    relevant_clip_ids: list[int]
    saliency_scores: list[list[int]]
    provenance: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "QVAnnotation":
        missing = {
            "qid",
            "query",
            "duration",
            "vid",
            "relevant_windows",
            "relevant_clip_ids",
            "saliency_scores",
        } - raw.keys()
        if missing:
            raise ValueError(f"missing annotation fields: {sorted(missing)}")
        windows = [TimeWindow(float(w[0]), float(w[1])) for w in raw["relevant_windows"]]
        clip_ids = [int(v) for v in raw["relevant_clip_ids"]]
        scores = [[int(s) for s in row] for row in raw["saliency_scores"]]
        if len(clip_ids) != len(scores):
            raise ValueError("relevant_clip_ids and saliency_scores must have equal lengths")
        if any(len(row) != 3 for row in scores):
            raise ValueError("each saliency score row must contain three annotator scores")
        if any(score < 0 or score > 4 for row in scores for score in row):
            raise ValueError("saliency scores must be in range 0..4")
        return cls(
            qid=raw["qid"],
            query=str(raw["query"]),
            duration=float(raw["duration"]),
            vid=str(raw["vid"]),
            relevant_windows=windows,
            relevant_clip_ids=clip_ids,
            saliency_scores=scores,
            provenance=dict(raw.get("provenance", {})),
        )


@dataclass
class Prediction:
    qid: int | str
    query: str
    vid: str
    pred_relevant_windows: list[TimeWindow]
    pred_saliency_scores: list[float]
    result_status: str = "PRELIMINARY_MOCK"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "qid": self.qid,
            "query": self.query,
            "vid": self.vid,
            "pred_relevant_windows": [window.as_list() for window in self.pred_relevant_windows],
            "pred_saliency_scores": [round(float(score), 6) for score in self.pred_saliency_scores],
            "result_status": self.result_status,
            "metadata": self.metadata,
        }


@dataclass
class SemanticExtension:
    schema_version: str
    qid: int | str
    annotation_status: str
    semantic_elements: list[dict[str, Any]]
    media_units: list[dict[str, Any]]
    relations: list[dict[str, Any]]
    expected_assembly: dict[str, Any]
    source: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "SemanticExtension":
        return cls(
            schema_version=str(raw["schema_version"]),
            qid=raw["qid"],
            annotation_status=str(raw["annotation_status"]),
            semantic_elements=list(raw.get("semantic_elements", [])),
            media_units=list(raw.get("media_units", [])),
            relations=list(raw.get("relations", [])),
            expected_assembly=dict(raw.get("expected_assembly", {})),
            source=dict(raw.get("source", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

