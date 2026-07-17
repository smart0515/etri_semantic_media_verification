from __future__ import annotations

from pathlib import Path
from typing import Protocol

from semantic_validator.models import QVAnnotation


class DatasetAdapter(Protocol):
    def load_annotations(self, annotation_path: str | Path) -> list[QVAnnotation]:
        """Convert an external annotation file into the common verification model."""
        ...

