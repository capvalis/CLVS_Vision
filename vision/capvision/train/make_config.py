"""Generate a D-FINE training config for one of our built datasets.

Example:
    python -m capvision.train.make_config --dataset kaggle_v1 --model s --input 640 --epochs 40 \
        --batch 8 --name kaggle_v1_s640

Writes vision/runs/<name>/config.yml. The config includes D-FINE's own base files by absolute path and
overrides: dataset paths, number of classes, input size, epochs, batch size, workers, output dir.
Augmentation is kept from D-FINE (photometric distort, zoom-out, IoU crop, flip, multi-scale) and
extended with a mild JPEG/blur degradation to mimic a radio video link.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from .. import CV_DIR, DATASETS_OUT, DFINE_DIR, RUNS_DIR
from ..classes import load_classes

MODEL_SIZES = {"n", "s", "m", "l", "x"}


def make_config(dataset: str, model: str, input_size: int, epochs: int, batch: int, name: str,
                workers: int = 4, lr: float = None, eval_batch: int = None, stop_aug_epoch: int = None) -> Path:
    assert model in MODEL_SIZES
    spec = load_classes()
    ds_dir = DATASETS_OUT / dataset
    build = json.load(open(ds_dir / "build.json"))
    image_root = build["image_root"]
    ann = ds_dir / "annotations"
    run_dir = RUNS_DIR / name
    run_dir.mkdir(parents=True, exist_ok=True)

    base = DFINE_DIR / "configs" / "dfine"
    stop_aug = stop_aug_epoch if stop_aug_epoch is not None else max(1, int(epochs * 0.9))
    cfg = {
        "__include__": [
            str(DFINE_DIR / "configs" / "runtime.yml"),
            str(base / "include" / "dataloader.yml"),
            str(base / "include" / "optimizer.yml"),
            str(base / "include" / "dfine_hgnetv2.yml"),
        ],
        "task": "detection",
        "output_dir": str(run_dir),
        "num_classes": spec.num_classes,
        "remap_mscoco_category": False,
        "eval_spatial_size": [input_size, input_size],
        "epochs": epochs,
        "checkpoint_freq": 1,
        "print_freq": 50,
        "sync_bn": False,
        "evaluator": {"type": "CocoEvaluator", "iou_types": ["bbox"]},
        "train_dataloader": {
            "type": "DataLoader",
            "dataset": {
                "type": "CocoDetection",
                "img_folder": image_root,
                "ann_file": str(ann / "instances_train.json"),
                "return_masks": False,
                "transforms": {
                    "type": "Compose",
                    "ops": [
                        {"type": "RandomPhotometricDistort", "p": 0.5},
                        {"type": "RandomZoomOut", "fill": 0},
                        {"type": "RandomIoUCrop", "p": 0.8},
                        {"type": "SanitizeBoundingBoxes", "min_size": 1},
                        {"type": "RandomHorizontalFlip"},
                        {"type": "Resize", "size": [input_size, input_size]},
                        {"type": "SanitizeBoundingBoxes", "min_size": 1},
                        {"type": "ConvertPILImage", "dtype": "float32", "scale": True},
                        {"type": "ConvertBoxes", "fmt": "cxcywh", "normalize": True},
                    ],
                    "policy": {"name": "stop_epoch", "epoch": stop_aug,
                               "ops": ["RandomPhotometricDistort", "RandomZoomOut", "RandomIoUCrop"]},
                },
            },
            "shuffle": True,
            "num_workers": workers,
            "drop_last": True,
            "total_batch_size": batch,
            "collate_fn": {"type": "BatchImageCollateFunction", "base_size": input_size,
                           "base_size_repeat": 3, "stop_epoch": stop_aug},
        },
        "val_dataloader": {
            "type": "DataLoader",
            "dataset": {
                "type": "CocoDetection",
                "img_folder": image_root,
                "ann_file": str(ann / "instances_val.json"),
                "return_masks": False,
                "transforms": {"type": "Compose", "ops": [
                    {"type": "Resize", "size": [input_size, input_size]},
                    {"type": "ConvertPILImage", "dtype": "float32", "scale": True},
                ]},
            },
            "shuffle": False,
            "num_workers": workers,
            "drop_last": False,
            "total_batch_size": eval_batch or max(1, batch * 2),
            "collate_fn": {"type": "BatchImageCollateFunction"},
        },
    }
    # model size blocks copied from D-FINE's custom configs
    size_cfg = yaml.safe_load(open(base / "custom" / f"dfine_hgnetv2_{model}_custom.yml"))
    for k in ("DFINE", "HGNetv2", "DFINETransformer", "HybridEncoder", "optimizer"):
        if k in size_cfg:
            cfg[k] = size_cfg[k]
    cfg["HGNetv2"]["pretrained"] = True
    cfg["HGNetv2"]["local_model_dir"] = str(DFINE_DIR / "weight" / "hgnetv2") + "/"
    if lr:
        cfg["optimizer"]["lr"] = lr
    cfg["lr_warmup_scheduler"] = {"type": "LinearWarmup", "warmup_duration": 200}
    cfg["lr_scheduler"] = {"type": "MultiStepLR", "milestones": [max(1, int(epochs * 0.8))], "gamma": 0.1}
    cfg["use_ema"] = True
    cfg["ema"] = {"type": "ModelEMA", "decay": 0.9995, "warmups": 500, "start": 0}
    cfg["use_amp"] = False  # set True only on CUDA; run.py adds --use-amp when the device is cuda

    out = run_dir / "config.yml"
    with open(out, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)
    (run_dir / "classes.json").write_text(json.dumps(spec.coco_categories(), indent=1))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--model", default="s", choices=sorted(MODEL_SIZES))
    ap.add_argument("--input", type=int, default=640)
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--lr", type=float, default=None)
    ap.add_argument("--name", required=True)
    args = ap.parse_args(argv)
    out = make_config(args.dataset, args.model, args.input, args.epochs, args.batch, args.name, args.workers, args.lr)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
