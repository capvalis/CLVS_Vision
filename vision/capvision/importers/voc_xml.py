"""Importer for Pascal VOC XML annotations (HIT-UAV, HERIDAL, Mendeley vehicles).

Config keys: root, images (dir), annotations (dir), optional group_regex (applied to the file stem;
all capture groups joined form the scene key), optional official_test_list (file with stems that
form the raw test split).

HIT-UAV note: use its normal_xml folder, not the COCO JSON (known offset bug, repo issue #6).
HERIDAL note: a few XML files claim 4000x3000 while the JPEG is 4000x2250; the JPEG wins and boxes
are clipped.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Optional

from ..schema import BoxRecord, ImageRecord
from .base import IMAGE_EXTS, Importer, image_size


class VocXmlImporter(Importer):
    def __init__(self, spec, cfg, cv_root):
        super().__init__(spec, cfg, cv_root)
        self.source = str(cfg.get("source") or cfg.get("name") or "")
        if self.source not in spec.sources:
            raise ValueError(f"voc_xml importer needs a 'source' key naming a mapping in classes.yaml, got {self.source!r}")
        self.group_re = re.compile(cfg["group_regex"]) if cfg.get("group_regex") else None

    def _group(self, stem: str) -> str:
        if self.group_re:
            m = self.group_re.match(stem)
            if m:
                return f"{self.source}:" + "_".join(m.groups())
        return f"{self.source}:{stem}"

    def load(self) -> List[ImageRecord]:
        img_dir = self.resolve("images")
        ann_dir = self.resolve("annotations")
        test_stems = set()
        if self.cfg.get("official_test_list"):
            p = self.resolve("official_test_list")
            if p.is_file():
                test_stems = {ln.strip().split()[0] for ln in p.read_text().splitlines() if ln.strip()}

        images = {}
        for p in img_dir.rglob("*"):
            if p.suffix.lower() in IMAGE_EXTS:
                images[p.stem] = p

        records: List[ImageRecord] = []
        for xml_path in sorted(ann_dir.rglob("*.xml")):
            stem = xml_path.stem
            img_path = images.get(stem)
            if img_path is None:
                self.dropped["__missing_image__"] = self.dropped.get("__missing_image__", 0) + 1
                continue
            w, h = image_size(img_path)
            root = ET.parse(xml_path).getroot()
            boxes: List[BoxRecord] = []
            for obj in root.iter("object"):
                raw = (obj.findtext("name") or "").strip()
                leaf = self.map_label(raw)
                if leaf is None:
                    continue
                bb = obj.find("bndbox")
                if bb is None:
                    continue
                x0, y0, x1, y1 = (float(bb.findtext(k)) for k in ("xmin", "ymin", "xmax", "ymax"))
                b = BoxRecord(x0, y0, x1 - x0, y1 - y0, leaf, raw).clipped(w, h)
                if b is not None:
                    boxes.append(b)
            hint: Optional[str] = "test" if stem in test_stems else None
            records.append(
                ImageRecord(
                    path=img_path.resolve(),
                    width=w,
                    height=h,
                    source=self.source,
                    group=self._group(stem),
                    split_hint=hint,
                    boxes=boxes,
                )
            )
        return records
