"""The target class list and the per-source label mappings (configs/classes.yaml)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from . import CONFIG_DIR


@dataclass
class ClassSpec:
    version: int
    leaves: List[str]
    parents: Dict[str, str]
    alert_exclude: List[str]
    sources: Dict[str, Dict[str, Optional[str]]]
    _leaf_to_id: Dict[str, int] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        # Category ids are 0-based on purpose: D-FINE (remap_mscoco_category: False) uses the COCO
        # category_id directly as the class index, so ids must be exactly 0 .. num_classes-1.
        self._leaf_to_id = {name: i for i, name in enumerate(self.leaves)}
        for child, parent in self.parents.items():
            if child not in self._leaf_to_id or parent not in self._leaf_to_id:
                raise ValueError(f"parents entry {child}->{parent} refers to an unknown leaf")
        for src, mapping in self.sources.items():
            for raw, leaf in mapping.items():
                if leaf is not None and leaf not in self._leaf_to_id:
                    raise ValueError(f"source {src}: label {raw!r} maps to unknown leaf {leaf!r}")

    # ---- ids -------------------------------------------------------------------------
    def leaf_id(self, name: str) -> int:
        return self._leaf_to_id[name]

    def leaf_name(self, cid: int) -> str:
        return self.leaves[cid]

    @property
    def num_classes(self) -> int:
        return len(self.leaves)

    def coco_categories(self) -> List[dict]:
        return [
            {"id": self.leaf_id(n), "name": n, "supercategory": self.parents.get(n, n)}
            for n in self.leaves
        ]

    # ---- hierarchy -------------------------------------------------------------------
    def parent_of(self, name: str) -> str:
        """Top-level name for a leaf (itself if it has no parent)."""
        while name in self.parents:
            name = self.parents[name]
        return name

    def parent_names(self) -> List[str]:
        seen: List[str] = []
        for n in self.leaves:
            p = self.parent_of(n)
            if p not in seen:
                seen.append(p)
        return seen

    def leaf_to_parent_id(self) -> Dict[int, int]:
        """Map leaf category id -> parent category id (parent ids are 0-based over parent_names())."""
        pid = {n: i for i, n in enumerate(self.parent_names())}
        return {self.leaf_id(n): pid[self.parent_of(n)] for n in self.leaves}

    # ---- sources ---------------------------------------------------------------------
    def map_label(self, source: str, raw_label: str) -> Optional[str]:
        """Translate a raw dataset label to a leaf name. None means drop the box.

        Raises KeyError for a label the mapping does not mention, so new labels are never silently
        dropped or guessed.
        """
        mapping = self.sources[source]
        if raw_label not in mapping:
            raise KeyError(f"source {source!r}: label {raw_label!r} is not in configs/classes.yaml")
        return mapping[raw_label]


def load_classes(path: Optional[Path] = None) -> ClassSpec:
    path = path or (CONFIG_DIR / "classes.yaml")
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return ClassSpec(
        version=int(raw["version"]),
        leaves=list(raw["leaves"]),
        parents=dict(raw.get("parents") or {}),
        alert_exclude=list(raw.get("alert_exclude") or []),
        sources={k: dict(v or {}) for k, v in (raw.get("sources") or {}).items()},
    )
