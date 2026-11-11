"""Run a trained D-FINE checkpoint over a COCO split and write COCO-format predictions plus speed.

Example:
    python -m capvision.train.infer --name kaggle_v1_s640 --checkpoint runs/kaggle_v1_s640/best_stg1.pth \
        --gt datasets/kaggle_v1/annotations/instances_val.json --out runs/kaggle_v1_s640/preds_val.json --device mps

The output file is {"predictions": [...COCO results...], "speed": {...}} so the scorecard can show
accuracy and latency together. Latency is measured per image at batch size 1 (model forward plus
post-processing, excluding file decode) after a warm-up, reporting p50/p95/p99.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import List

import numpy as np
import torch
import torch.nn as nn
import torchvision.transforms as T
from PIL import Image

from .. import DFINE_DIR, RUNS_DIR


def load_model(config: Path, checkpoint: Path, device: str) -> nn.Module:
    sys.path.insert(0, str(DFINE_DIR))
    from src.core import YAMLConfig  # noqa: E402

    cfg = YAMLConfig(str(config), resume=str(checkpoint))
    if "HGNetv2" in cfg.yaml_cfg:
        cfg.yaml_cfg["HGNetv2"]["pretrained"] = False
    ck = torch.load(str(checkpoint), map_location="cpu")
    state = ck["ema"]["module"] if "ema" in ck else ck["model"]
    cfg.model.load_state_dict(state)

    class Model(nn.Module):
        def __init__(self):
            super().__init__()
            self.model = cfg.model.deploy()
            self.postprocessor = cfg.postprocessor.deploy()

        def forward(self, images, orig_sizes):
            return self.postprocessor(self.model(images), orig_sizes)

    return Model().to(device).eval(), cfg.yaml_cfg.get("eval_spatial_size", [640, 640])[0]


@torch.no_grad()
def run(config: Path, checkpoint: Path, gt_json: Path, out_json: Path, device: str, score_thr: float = 0.001, limit: int = 0):
    model, size = load_model(config, checkpoint, device)
    gt = json.load(open(gt_json))
    # image root: the train config stores it
    import yaml
    img_root = Path(yaml.safe_load(open(config))["val_dataloader"]["dataset"]["img_folder"])
    tf = T.Compose([T.Resize((size, size)), T.ToTensor()])

    preds: List[dict] = []
    times: List[float] = []
    images = gt["images"][:limit] if limit else gt["images"]
    for n, im in enumerate(images):
        pil = Image.open(img_root / im["file_name"]).convert("RGB")
        w, h = pil.size
        x = tf(pil).unsqueeze(0).to(device)
        orig = torch.tensor([[w, h]]).to(device)
        if device == "mps":
            torch.mps.synchronize()
        elif device == "cuda":
            torch.cuda.synchronize()
        t0 = time.perf_counter()
        labels, boxes, scores = model(x, orig)
        if device == "mps":
            torch.mps.synchronize()
        elif device == "cuda":
            torch.cuda.synchronize()
        times.append((time.perf_counter() - t0) * 1000.0)
        lab, box, sc = labels[0].cpu().numpy(), boxes[0].cpu().numpy(), scores[0].cpu().numpy()
        for l, b, s in zip(lab, box, sc):
            if s < score_thr:
                continue
            x0, y0, x1, y1 = b.tolist()
            preds.append({"image_id": im["id"], "category_id": int(l), "bbox": [x0, y0, x1 - x0, y1 - y0], "score": float(s)})
        if (n + 1) % 100 == 0:
            print(f"[infer] {n + 1}/{len(images)}", file=sys.stderr)
    warm = times[5:] if len(times) > 10 else times
    speed = {
        "device": device, "input_size": size, "batch": 1, "images": len(images),
        "ms_p50": float(np.percentile(warm, 50)), "ms_p95": float(np.percentile(warm, 95)),
        "ms_p99": float(np.percentile(warm, 99)), "ms_mean": float(np.mean(warm)),
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    json.dump({"predictions": preds, "speed": speed}, open(out_json, "w"))
    print(f"[infer] wrote {len(preds)} predictions; speed {speed}", file=sys.stderr)
    return speed


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--gt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--score-thr", type=float, default=0.001)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args(argv)
    run(RUNS_DIR / args.name / "config.yml", Path(args.checkpoint), Path(args.gt), Path(args.out), args.device, args.score_thr, args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
