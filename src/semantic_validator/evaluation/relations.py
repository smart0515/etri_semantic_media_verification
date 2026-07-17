from __future__ import annotations

from collections.abc import Iterable

from semantic_validator.models import SemanticExtension


def evaluate_relation_integrity(
    extensions: Iterable[SemanticExtension], allowed_predicates: set[str]
) -> dict[str, object]:
    relation_count = 0
    valid_relation_count = 0
    undeclared_nodes: list[dict[str, object]] = []
    unknown_predicates: list[dict[str, object]] = []

    for extension in extensions:
        node_ids = {
            str(element["element_id"])
            for element in extension.semantic_elements
            if "element_id" in element
        }
        node_ids.update(
            str(unit["unit_id"]) for unit in extension.media_units if "unit_id" in unit
        )
        for relation in extension.relations:
            relation_count += 1
            subject = str(relation.get("subject", ""))
            object_id = str(relation.get("object", ""))
            predicate = str(relation.get("predicate", ""))
            nodes_valid = subject in node_ids and object_id in node_ids
            predicate_valid = predicate in allowed_predicates
            if not nodes_valid:
                undeclared_nodes.append(
                    {
                        "qid": extension.qid,
                        "relation_id": relation.get("relation_id"),
                        "subject": subject,
                        "object": object_id,
                    }
                )
            if not predicate_valid:
                unknown_predicates.append(
                    {
                        "qid": extension.qid,
                        "relation_id": relation.get("relation_id"),
                        "predicate": predicate,
                    }
                )
            if nodes_valid and predicate_valid:
                valid_relation_count += 1

    validity = 100.0 if relation_count == 0 else 100 * valid_relation_count / relation_count
    return {
        "relation_count": relation_count,
        "valid_relation_count": valid_relation_count,
        "relation_integrity_percent": round(validity, 4),
        "undeclared_nodes": undeclared_nodes,
        "unknown_predicates": unknown_predicates,
    }

