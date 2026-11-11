"""Common in-memory records for images and boxes, and the COCO writer.

Every importer produces ImageRecord objects. build_dataset deduplicates, splits and writes COCO JSON.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional

from .classes import ClassSpec


@dataclass
class BoxRecord:
    x: float            # top-left x, pixels
    y: float            # top-left y, pixels
    w: float
    h: float
    cls: str            # leaf class name
    source_label: str   # the raw label as found in the dataset
    ignore: bool = False  # True -> region is kept as "iscrowd" so detections there are not penalised

    def clipped(self, width: int, height: int) -> Optional["BoxRecord"]:
        x0 = max(0.0, self.x)
        y0 = max(0.0, self.y)
        x1 = min(float(width), self.x + self.w)
        y1 = min(float(height), self.y + self.h)
        if x1 - x0 < 1.0 or y1 - y0 < 1.0:
            return None
        return BoxRecord(x0, y0, x1 - x0, y1 - y0, self.cls, self.source_label, self.ignore)


@dataclass
class ImageRecord:
    path: Path                  # absolute path to the image file
    width: int
    height: int
    source: str                 # dataset key, e.g. "kaggle_military"
    group: str                  # scene / flight / clip key; images in one group never cross splits
    split_hint: Optional[str]   # "train" / "val" / "test" from the raw dataset, or None
    boxes: List[BoxRecord] = field(default_factory=list)
    meta: Dict[str, object] = field(default_factory=dict)
    md5: Optional[str] = None
    dhash: Optional[int] = None

    @property
    def class_counts(self) -> Dict[str, int]:
        out: Dict[str, int] = {}
        for b in self.boxes:
            if not b.ignore:
                out[b.cls] = out.get(b.cls, 0) + 1
        return out


def write_coco(
    records: List[ImageRecord],
    spec: ClassSpec,
    out_json: Path,
    image_root: Path,
) -> Dict[str, int]:
    """Write records as a COCO detection file. file_name is relative to image_root.

    Category ids are 0-based (see ClassSpec) because D-FINE uses them directly as class indices.
    """
    images, annotations = [], []
    ann_id = 1
    for img_id, r in enumerate(records, start=1):
        try:
            rel = str(r.path.relative_to(image_root))
        except ValueError:
            rel = str(r.path)
        images.append(
            {
                "id": img_id,
                "file_name": rel,
                "width": r.width,
                "height": r.height,
                "source": r.source,
                "group": r.group,
                "md5": r.md5,
            }
        )
        for b in r.boxes:
            annotations.append(
                {
                    "id": ann_id,
                    "image_id": img_id,
                    "category_id": spec.leaf_id(b.cls),
                    "bbox": [round(b.x, 2), round(b.y, 2), round(b.w, 2), round(b.h, 2)],
                    "area": round(b.w * b.h, 2),
                    "iscrowd": 1 if b.ignore else 0,
                    "source_label": b.source_label,
                }
            )
            ann_id += 1
    doc = {
        "info": {"description": "capvision build", "class_version": spec.version},
        "images": images,
        "annotations": annotations,
        "categories": spec.coco_categories(),
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(doc, f)
    return {"images": len(images), "annotations": len(annotations)}


def record_summary(records: List[ImageRecord]) -> Dict[str, object]:
    classes: Dict[str, int] = {}
    empty = 0
    for r in records:
        if not r.boxes:
            empty += 1
        for k, v in r.class_counts.items():
            classes[k] = classes.get(k, 0) + v
    return {"images": len(records), "empty_images": empty, "boxes_per_class": dict(sorted(classes.items()))}
