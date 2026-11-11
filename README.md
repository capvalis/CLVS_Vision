# CLVS Vision

Capvalis Computer Vision research, dataset documentation, and model pipeline.

- [Project context](Project%20Context.md)
- [Architecture](Architecture.md)
- [Training datasets](Training%20Datasets.md)
- [Vision pipeline setup and usage](vision/README.md)
- [Dataset research and comparisons](Understanding/)
- [Research notes](research_notes/) and [reports](reports/)

## Raw datasets

The complete raw dataset snapshot is available in the [11 November 2026 dataset release](https://github.com/capvalis/CLVS_Vision/releases/tag/raw-datasets-2026-11-11): 140,689 files totaling 13.2 GB before compression. Large files are stored as release assets so a normal Git clone stays small.

Follow [Dataset/README.md](Dataset/README.md) to download, verify, and restore the original `Dataset/` folder structure. Dataset metadata and checksums are tracked in this repository.

The existing pipeline ignore rules keep its virtual environment, downloaded third-party code, model weights, built datasets, and training outputs local. See [vision/README.md](vision/README.md) to set up the pipeline.
