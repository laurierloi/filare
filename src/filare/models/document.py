"""Document-level representation emitted/consumed before rendering."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

import yaml

from filare.models.page import (
    BOMPage,
    CutPage,
    HarnessPage,
    PageBase,
    TerminationPage,
    TitlePage,
)


def _yaml_dumps(data: Any) -> str:
    return yaml.safe_dump(data, sort_keys=True)


@dataclass
class DocumentRepresentation:
    """A structured, pre-render view of a document (pages, diagrams, notes, BOMs)."""

    metadata: Dict[str, Any] = field(default_factory=dict)
    pages: List[PageBase] = field(default_factory=list)
    notes: Optional[str] = None
    bom: Optional[Dict[str, Any]] = None
    extras: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "metadata": self.metadata,
            "pages": [
                _coerce_for_yaml(p.model_dump() if hasattr(p, "model_dump") else p)
                for p in self.pages
            ],
            "notes": self.notes,
            "bom": self.bom,
            "extras": _coerce_for_yaml(self.extras),
        }

    def compute_hash(self) -> str:
        serialized = _yaml_dumps(self.as_dict()).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

    def to_yaml(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_yaml_dumps(self.as_dict()), encoding="utf-8")

    @classmethod
    def from_yaml(cls, path: Path) -> "DocumentRepresentation":
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        page_models: List[PageBase] = []
        for page in data.get("pages", []):
            page_type = page.get("type") if isinstance(page, dict) else None
            if page_type == "harness":
                model: Type[PageBase] = HarnessPage
            elif page_type == "bom":
                model = BOMPage
            elif page_type == "cut":
                model = CutPage
            elif page_type == "termination":
                model = TerminationPage
            elif page_type == "title":
                model = TitlePage
            else:
                model = PageBase
            page_models.append(model(**page))
        return cls(
            metadata=data.get("metadata", {}),
            pages=page_models,
            notes=data.get("notes"),
            bom=data.get("bom"),
            extras=data.get("extras", {}),
        )


class DocumentHashRegistry:
    """Tracks hashes of generated documents to detect user edits."""

    def __init__(self, path: Path):
        self.path = path
        self._hashes: Dict[str, str] = {}

    def load(self) -> None:
        if not self.path.exists():
            self._hashes = {}
            return
        data = yaml.safe_load(self.path.read_text(encoding="utf-8")) or {}
        if isinstance(data, list):
            # legacy list support: treat as unknown filename entries
            self._hashes = {f"unknown_{i}": h for i, h in enumerate(data)}
        else:
            self._hashes = dict(data)

    def contains(self, filename: str, value: str) -> bool:
        return self._hashes.get(filename) == value

    def add(self, filename: str, value: str) -> None:
        self._hashes[filename] = value

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(_yaml_dumps(self._hashes), encoding="utf-8")


def _coerce_for_yaml(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _coerce_for_yaml(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_coerce_for_yaml(v) for v in value]
    if hasattr(value, "value"):
        return getattr(value, "value")
    return value
