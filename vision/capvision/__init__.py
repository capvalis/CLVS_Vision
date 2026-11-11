"""capvision: dataset building, scorecard and training wrappers for the Capvalis drone vision model.

Plain language: this package turns raw datasets into one common format, removes duplicates,
splits them by scene, scores detectors by object size, and drives D-FINE training and export.
"""

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
VISION_DIR = PACKAGE_DIR.parent                      # .../Computer Vision/vision
CV_DIR = VISION_DIR.parent                           # .../Computer Vision
CONFIG_DIR = VISION_DIR / "configs"
DFINE_DIR = VISION_DIR / "third_party" / "D-FINE"
WEIGHTS_DIR = VISION_DIR / "weights"
DATASETS_OUT = VISION_DIR / "datasets"
RUNS_DIR = VISION_DIR / "runs"

__version__ = "0.1.0"
