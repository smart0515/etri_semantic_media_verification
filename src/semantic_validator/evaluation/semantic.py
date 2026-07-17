from __future__ import annotations

import re
from collections.abc import Iterable

from semantic_validator.models import SemanticExtension


def normalize_label(value: object) -> str:
    """Normalize an element label while preserving Unicode letters and digits."""

    return " ".join(re.sub(r"[^\w]+", " ", str(value).lower()).split())


def _f1(true_positive: int, predicted: int, reference: int) -> dict[str, float | int]:
    precision = 1.0 if predicted == 0 and reference == 0 else (
        true_positive / predicted if predicted else 0.0
    )
    recall = 1.0 if reference == 0 else true_positive / reference
    score = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    return {
        "true_positive": true_positive,
        "predicted_count": predicted,
        "reference_count": reference,
        "precision": round(100 * precision, 4),
        "recall": round(100 * recall, 4),
        "f1": round(100 * score, 4),
    }


def _unit_map(extension: SemanticExtension) -> dict[str, tuple[float, float]]:
    return {
        str(unit["unit_id"]): (float(unit["start_ms"]) / 1000, float(unit["end_ms"]) / 1000)
        for unit in extension.media_units
        if {"unit_id", "start_ms", "end_ms"} <= unit.keys()
    }


def _element_span(
    element: dict[str, object], units: dict[str, tuple[float, float]]
) -> tuple[float, float] | None:
    spans = [units[str(ref)] for ref in element.get("media_unit_refs", []) if str(ref) in units]
    if not spans:
        return None
    return min(span[0] for span in spans), max(span[1] for span in spans)


def _span_iou(
    left: tuple[float, float] | None, right: tuple[float, float] | None
) -> float:
    if left is None and right is None:
        return 1.0
    if left is None or right is None:
        return 0.0
    intersection = max(0.0, min(left[1], right[1]) - max(left[0], right[0]))
    union = max(left[1], right[1]) - min(left[0], right[0])
    return 0.0 if union <= 0 else intersection / union


def _match_elements(
    reference: SemanticExtension,
    candidate: SemanticExtension,
    temporal_iou_threshold: float,
) -> tuple[dict[str, str], dict[str, float | int]]:
    ref_units = _unit_map(reference)
    candidate_units = _unit_map(candidate)
    remaining = {str(item["element_id"]): item for item in reference.semantic_elements}
    mapping: dict[str, str] = {}

    for element in candidate.semantic_elements:
        candidate_id = str(element["element_id"])
        best_id: str | None = None
        best_iou = -1.0
        for reference_id, reference_element in remaining.items():
            if str(element.get("type")) != str(reference_element.get("type")):
                continue
            if normalize_label(element.get("label")) != normalize_label(reference_element.get("label")):
                continue
            overlap = _span_iou(
                _element_span(element, candidate_units),
                _element_span(reference_element, ref_units),
            )
            if overlap >= temporal_iou_threshold and overlap > best_iou:
                best_id, best_iou = reference_id, overlap
        if best_id is not None:
            mapping[candidate_id] = best_id
            del remaining[best_id]

    return mapping, _f1(
        len(mapping), len(candidate.semantic_elements), len(reference.semantic_elements)
    )


def _map_media_units(
    reference: SemanticExtension, candidate: SemanticExtension
) -> dict[str, str]:
    reference_by_signature = {
        (
            unit.get("source_clip_id"),
            unit.get("start_ms"),
            unit.get("end_ms"),
        ): str(unit["unit_id"])
        for unit in reference.media_units
    }
    return {
        str(unit["unit_id"]): reference_by_signature[signature]
        for unit in candidate.media_units
        if (
            signature := (
                unit.get("source_clip_id"),
                unit.get("start_ms"),
                unit.get("end_ms"),
            )
        ) in reference_by_signature
    }


def _relation_metrics(
    reference: SemanticExtension,
    candidate: SemanticExtension,
    element_mapping: dict[str, str],
) -> dict[str, float | int]:
    node_mapping = dict(element_mapping)
    node_mapping.update(_map_media_units(reference, candidate))
    reference_triples = {
        (str(item["subject"]), str(item["predicate"]), str(item["object"]))
        for item in reference.relations
    }
    candidate_triples = {
        (
            node_mapping.get(str(item["subject"]), str(item["subject"])),
            str(item["predicate"]),
            node_mapping.get(str(item["object"]), str(item["object"])),
        )
        for item in candidate.relations
    }
    return _f1(
        len(reference_triples & candidate_triples),
        len(candidate_triples),
        len(reference_triples),
    )


def evaluate_semantic_structure(
    references: Iterable[SemanticExtension],
    candidates: Iterable[SemanticExtension],
    temporal_iou_threshold: float = 0.5,
) -> dict[str, object]:
    """Evaluate element and relation accuracy after qid-based alignment."""

    references_by_qid = {str(item.qid): item for item in references}
    candidates_by_qid = {str(item.qid): item for item in candidates}
    if references_by_qid.keys() != candidates_by_qid.keys():
        raise ValueError("reference and candidate qids must match")

    element_tp = element_predicted = element_reference = 0
    relation_tp = relation_predicted = relation_reference = 0
    by_qid: dict[str, object] = {}

    for qid, reference in references_by_qid.items():
        candidate = candidates_by_qid[qid]
        mapping, element_result = _match_elements(
            reference, candidate, temporal_iou_threshold
        )
        relation_result = _relation_metrics(reference, candidate, mapping)
        by_qid[qid] = {"elements": element_result, "relations": relation_result}
        element_tp += int(element_result["true_positive"])
        element_predicted += int(element_result["predicted_count"])
        element_reference += int(element_result["reference_count"])
        relation_tp += int(relation_result["true_positive"])
        relation_predicted += int(relation_result["predicted_count"])
        relation_reference += int(relation_result["reference_count"])

    return {
        "temporal_iou_threshold": temporal_iou_threshold,
        "elements": _f1(element_tp, element_predicted, element_reference),
        "relations": _f1(relation_tp, relation_predicted, relation_reference),
        "by_qid": by_qid,
    }
