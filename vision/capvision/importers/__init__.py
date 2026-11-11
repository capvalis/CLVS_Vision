"""Dataset importers. Each returns a list of ImageRecord with leaf class names already applied."""

from .base import Importer, image_size
from .kaggle_military import KaggleMilitaryImporter
from .voc_xml import VocXmlImporter
from .coco_json import CocoJsonImporter
from .halmstad import HalmstadImporter

IMPORTERS = {
    "kaggle_military": KaggleMilitaryImporter,
    "voc_xml": VocXmlImporter,
    "coco_json": CocoJsonImporter,
    "halmstad": HalmstadImporter,
}

__all__ = ["Importer", "image_size", "IMPORTERS"]
