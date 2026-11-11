"""Importer for the Kaggle 'Military Assets Dataset (12 classes, YOLO8 format)' (catalogue D43).

Layout: <root>/{train,val,test}/images/*.jpg and <root>/{train,val,test}/labels/*.txt
YOLO text: `cls cx cy w h` normalised to the image size, one box per line. The last line often has
no trailing newline, which is why counts via `cat | wc` were wrong earlier.

No scene information exists, so the group is the file itself; duplicate clustering later merges
identical and near-identical files into one group.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import yaml

from ..schema import BoxRecord, ImageRecord
from .base import IMAGE_EXTS, Importer, image_size


class KaggleMilitaryImporter(Importer):
    source = "kaggle_military"

    def load(self) -> List[ImageRecord]:
        with open(self.resolve("class_file"), "r", encoding="utf-8") as f:
            names = yaml.safe_load(f)["names"]
        id_to_raw = {int(k): str(v) for k, v in names.items()}

        records: List[ImageRecord] = []
        for split in self.cfg.get("splits", ["train", "val", "test"]):
            img_dir = self.root / split / "images"
            lbl_dir = self.root / split / "labels"
            if not img_dir.is_dir():
                continue
            for img_path in sorted(img_dir.iterdir()):
                if img_path.suffix.lower() not in IMAGE_EXTS:
                    continue
                w, h = image_size(img_path)
                boxes: List[BoxRecord] = []
                lbl = lbl_dir / (img_path.stem + ".txt")
                if lbl.is_file():
                    for line in lbl.read_text(encoding="utf-8").splitlines():
                        p = line.split()
                        if len(p) < 5:
                            continue
                        try:
                            raw = id_to_raw[int(p[0])]
                            cx, cy, bw, bh = (float(v) for v in p[1:5])
                        except (ValueError, KeyError):
                            # one known corrupt line in test/labels/000003.txt; count and skip
                            self.dropped["__malformed_line__"] = self.dropped.get("__malformed_line__", 0) + 1
                            continue
                        leaf = self.map_label(raw)
                        if leaf is None:
                            continue
                        b = BoxRecord((cx - bw / 2) * w, (cy - bh / 2) * h, bw * w, bh * h, leaf, raw)
                        b = b.clipped(w, h)
                        if b is not None:
                            boxes.append(b)
                records.append(
                    ImageRecord(
                        path=img_path.resolve(),
                        width=w,
                        height=h,
                        source=self.source,
                        group=f"{self.source}:{img_path.stem}",
                        split_hint=split,
                        boxes=boxes,
                        meta={"raw_split": split},
                    )
                )
        return records
