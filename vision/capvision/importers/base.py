from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image

from ..classes import ClassSpec
from ..schema import ImageRecord

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def image_size(path: Path) -> Tuple[int, int]:
    """(width, height) without decoding the pixels."""
    with Image.open(path) as im:
        return im.size


class Importer(ABC):
    source: str = ""

    def __init__(self, spec: ClassSpec, cfg: Dict[str, object], cv_root: Path) -> None:
        self.spec = spec
        self.cfg = cfg
        self.cv_root = cv_root
        root = Path(str(cfg["root"]))
        self.root = root if root.is_absolute() else (cv_root / root)
        self.dropped: Dict[str, int] = {}

    def resolve(self, key: str) -> Path:
        p = Path(str(self.cfg[key]))
        return p if p.is_absolute() else (self.root / p)

    def map_label(self, raw: str):
        leaf = self.spec.map_label(self.source, raw)
        if leaf is None:
            self.dropped[raw] = self.dropped.get(raw, 0) + 1
        return leaf

    @abstractmethod
    def load(self) -> List[ImageRecord]: ...
