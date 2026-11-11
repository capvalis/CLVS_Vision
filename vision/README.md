# vision: the Capvalis drone vision model pipeline

Plain language: this folder turns raw datasets into one clean training set, trains an Apache-licensed
transformer detector (D-FINE), scores it by object size and speed, and exports it for the ground station.
Design and reasons are in `../Project Context.md`, `../Training Datasets.md` and `../Architecture.md`.

## Layout

| Path | What |
|---|---|
| `configs/classes.yaml` | The adopted class list and every dataset's label mapping |
| `configs/datasets.yaml` | Where each raw dataset lives and which importer reads it |
| `capvision/importers/` | Readers for YOLO text, VOC XML, COCO JSON and the Halmstad export |
| `capvision/dedup.py` | Exact (MD5) and near-duplicate (dHash) detection |
| `capvision/splits.py` | Scene-aware train/val/test assignment |
| `capvision/build_dataset.py` | Import, deduplicate, split, write COCO JSON and a report |
| `capvision/scorecard/` | AP by size bucket and class, parent-level and leaf-level, plus speed |
| `capvision/train/` | Config generator, trainer launcher, inference with latency |
| `third_party/D-FINE` | Upstream detector, Apache-2.0, unmodified |
| `datasets/`, `runs/`, `weights/` | Built data, training outputs, downloaded checkpoints (not in git) |

## Setup

```sh
cd "Computer Vision/vision"
/opt/homebrew/bin/python3.12 -m venv .venv && . .venv/bin/activate
pip install torch torchvision numpy pillow opencv-python-headless pycocotools pyyaml tqdm scipy pandas matplotlib faster-coco-eval
git clone --depth 1 https://github.com/Peterande/D-FINE.git third_party/D-FINE
```

## Use

```sh
# 1. build a dataset (dedup + scene split + COCO)
python -m capvision.build_dataset --sources kaggle_military --name kaggle_v1

# 2. make a training config and train
python -m capvision.train.make_config --dataset kaggle_v1 --model s --input 640 --epochs 40 --batch 8 --name kaggle_v1_s640
python -m capvision.train.run --name kaggle_v1_s640 --device mps --pretrained obj365

# 3. predict and score
python -m capvision.train.infer --name kaggle_v1_s640 --checkpoint runs/kaggle_v1_s640/best_stg1.pth \
    --gt datasets/kaggle_v1/annotations/instances_val.json --out runs/kaggle_v1_s640/preds_val.json --device mps
python -m capvision.scorecard.evaluate --gt datasets/kaggle_v1/annotations/instances_val.json \
    --pred runs/kaggle_v1_s640/preds_val.json --out runs/kaggle_v1_s640/scorecard_val.json
```

Every build writes `datasets/<name>/REPORT.md`; every scorecard writes a `.md` next to its `.json`.

## On an NVIDIA machine

Same commands with `--device cuda --amp`, batch 16 to 32, workers 8. Copy `datasets/`, `weights/` and `configs/`;
images stay at the same relative paths under the Computer Vision folder (the image root recorded in
`datasets/<name>/build.json`).

## Things that are easy to get wrong

- Category ids in the COCO files are **0-based** on purpose: D-FINE uses them directly as class indices.
- D-FINE-N has no stride-8 feature map; use S or larger for small objects.
- The Mac (Apple M5, 16 GB) trains D-FINE-S at roughly 10 s per batch of 8 and is for smoke tests only.
- Stop a background run with `pkill -f capvision.train.run; pkill -f D-FINE/train.py`.
