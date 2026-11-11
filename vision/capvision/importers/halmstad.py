"""Importer for the Halmstad drone detection dataset (CC0).

The labels ship as MATLAB `groundTruth` objects inside .mat files, which scipy cannot read. The
plan is to decode them with the `mcos-decoder` package and export, per clip, a simple JSON:
    {"clip": "...", "sensor": "IR|VISIBLE", "class": "DRONE", "frames": [{"index": 0, "boxes": [[x,y,w,h], ...]}, ...]}
plus the frames themselves extracted from the video. That export step lives in tools/ once the data
is downloaded; this importer reads the exported JSON so the rest of the pipeline is unchanged.

Config: root, frames (dir with <clip>/<index>.jpg), labels (dir with <clip>.json), exclude_internet_clips.
The 11 airplane and 38 helicopter clips sourced from YouTube are listed in the dataset's description
spreadsheet; their clip names go in `internet_clips.txt` under root and are skipped when
exclude_internet_clips is true.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from ..schema import BoxRecord, ImageRecord
from .base import Importer, image_size


class HalmstadImporter(Importer):
    source = "halmstad"

    def load(self) -> List[ImageRecord]:
        frames_dir = self.resolve("frames") if self.cfg.get("frames") else self.root / "frames"
        labels_dir = self.resolve("labels") if self.cfg.get("labels") else self.root / "labels"
        if not labels_dir.is_dir():
            raise FileNotFoundError(
                f"{labels_dir} not found. Run the MATLAB-to-JSON export in tools/ first (needs the "
                "mcos-decoder package); see the module docstring."
            )
        excluded = set()
        if self.cfg.get("exclude_internet_clips", True):
            p = self.root / "internet_clips.txt"
            if p.is_file():
                excluded = {ln.strip() for ln in p.read_text().splitlines() if ln.strip()}

        records: List[ImageRecord] = []
        for lbl in sorted(labels_dir.glob("*.json")):
            doc = json.load(open(lbl, "r", encoding="utf-8"))
            clip = doc["clip"]
            if clip in excluded:
                self.dropped["__internet_clip__"] = self.dropped.get("__internet_clip__", 0) + 1
                continue
            raw = str(doc["class"]).upper()
            leaf = self.map_label(raw)
            for fr in doc["frames"]:
                img_path = frames_dir / clip / f"{int(fr['index']):06d}.jpg"
                if not img_path.is_file():
                    continue
                w, h = image_size(img_path)
                boxes: List[BoxRecord] = []
                if leaf is not None:
                    for x, y, bw, bh in fr.get("boxes", []):
                        b = BoxRecord(float(x), float(y), float(bw), float(bh), leaf, raw).clipped(w, h)
                        if b is not None:
                            boxes.append(b)
                records.append(
                    ImageRecord(
                        path=img_path.resolve(),
                        width=w,
                        height=h,
                        source=self.source,
                        group=f"{self.source}:{clip}",
                        split_hint=None,
                        boxes=boxes,
                        meta={"sensor": doc.get("sensor"), "clip": clip},
                    )
                )
        return records
