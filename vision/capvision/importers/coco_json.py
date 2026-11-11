"""Importer for COCO-format JSON (SeaDronesSee). Config: root, images (dir), and any number of
`*_json` keys, each an annotation file; the key prefix (train/val/test) becomes the split hint.

Group key: SeaDronesSee images carry a `source` or `video_id`-like field in some releases; when
present it is used, otherwise the file stem. Boxes in classes mapped to null are dropped; boxes in
the `ignored` category become iscrowd regions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from ..schema import BoxRecord, ImageRecord
from .base import Importer, image_size


class CocoJsonImporter(Importer):
    def __init__(self, spec, cfg, cv_root):
        super().__init__(spec, cfg, cv_root)
        self.source = str(cfg.get("source") or "")
        if self.source not in spec.sources:
            raise ValueError("coco_json importer needs a 'source' key naming a mapping in classes.yaml")

    def load(self) -> List[ImageRecord]:
        img_dir = self.resolve("images") if self.cfg.get("images") else self.root
        records: List[ImageRecord] = []
        for key, val in self.cfg.items():
            if not key.endswith("_json"):
                continue
            split = key[: -len("_json")]
            ann_path = Path(str(val))
            ann_path = ann_path if ann_path.is_absolute() else (self.root / ann_path)
            if not ann_path.is_file():
                continue
            doc = json.load(open(ann_path, "r", encoding="utf-8"))
            cats = {c["id"]: c["name"] for c in doc["categories"]}
            by_img = {}
            for a in doc["annotations"]:
                by_img.setdefault(a["image_id"], []).append(a)
            for im in doc["images"]:
                img_path = img_dir / im["file_name"]
                if not img_path.is_file():
                    self.dropped["__missing_image__"] = self.dropped.get("__missing_image__", 0) + 1
                    continue
                w, h = im.get("width"), im.get("height")
                if not w or not h:
                    w, h = image_size(img_path)
                boxes: List[BoxRecord] = []
                for a in by_img.get(im["id"], []):
                    raw = cats[a["category_id"]]
                    leaf = self.map_label(raw)
                    if leaf is None:
                        continue
                    x, y, bw, bh = a["bbox"]
                    b = BoxRecord(x, y, bw, bh, leaf, raw, ignore=bool(a.get("iscrowd", 0))).clipped(w, h)
                    if b is not None:
                        boxes.append(b)
                group = str(im.get("source") or im.get("video_id") or im.get("clip") or Path(im["file_name"]).stem)
                records.append(
                    ImageRecord(
                        path=img_path.resolve(),
                        width=int(w),
                        height=int(h),
                        source=self.source,
                        group=f"{self.source}:{group}",
                        split_hint=split,
                        boxes=boxes,
                        meta={k: im[k] for k in im if k not in ("id", "file_name", "width", "height")},
                    )
                )
        return records
