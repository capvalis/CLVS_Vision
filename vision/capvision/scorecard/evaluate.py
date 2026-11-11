"""Score a COCO results file against a COCO ground-truth file.

Reports, at leaf level and at parent level (soldier counted as person, tank as military_vehicle...):
- AP (IoU 0.50:0.95), AP50, AP75 overall
- AP and AP50 per object-size bucket by longest side: tiny <16 px, small 16-32, medium 32-96, large >96
- AP50 per class
- recall at 100 detections per size bucket
Speed numbers come from the inference step and are merged in by report.py.

Usage:
    python -m capvision.scorecard.evaluate --gt datasets/x/annotations/instances_val.json \
        --pred runs/x/preds_val.json --out runs/x/scorecard_val.json
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

from ..classes import ClassSpec, load_classes

try:
    from faster_coco_eval import COCO, COCOeval_faster as COCOeval
except ImportError:  # pragma: no cover
    from pycocotools.coco import COCO  # type: ignore
    from pycocotools.cocoeval import COCOeval  # type: ignore

# size buckets by longest side -> area ranges (area = side^2 for a square box; a reasonable proxy)
SIZE_BUCKETS = {
    "all": [0, 1e10],
    "tiny": [0, 16 ** 2],
    "small": [16 ** 2, 32 ** 2],
    "medium": [32 ** 2, 96 ** 2],
    "large": [96 ** 2, 1e10],
}


def _remap_to_parents(gt: dict, preds: List[dict], spec: ClassSpec):
    l2p = spec.leaf_to_parent_id()
    gt2 = json.loads(json.dumps(gt))
    gt2["categories"] = [{"id": i, "name": n} for i, n in enumerate(spec.parent_names())]
    for a in gt2["annotations"]:
        a["category_id"] = l2p[a["category_id"]]
    preds2 = []
    for p in preds:
        q = dict(p)
        q["category_id"] = l2p[p["category_id"]]
        preds2.append(q)
    return gt2, preds2


def _coco_from_dict(doc: dict) -> COCO:
    c = COCO()
    c.dataset = doc
    with contextlib.redirect_stdout(io.StringIO()):
        c.createIndex()
    return c


def _ap_at(ev, iou_thr: Optional[float], area_idx: int, cat_idx: Optional[int] = None, max_det_idx: int = -1) -> float:
    p = ev.eval["precision"]  # [T, R, K, A, M]
    if iou_thr is None:
        t = slice(None)
    else:
        t = int(np.where(np.isclose(ev.params.iouThrs, iou_thr))[0][0])
    k = slice(None) if cat_idx is None else cat_idx
    s = p[t, :, k, area_idx, max_det_idx]
    s = s[s > -1]
    return float(np.mean(s)) if s.size else float("nan")


def _recall_at(ev, area_idx: int, max_det_idx: int = -1) -> float:
    r = ev.eval["recall"]  # [T, K, A, M]
    s = r[:, :, area_idx, max_det_idx]
    s = s[s > -1]
    return float(np.mean(s)) if s.size else float("nan")


def evaluate_level(gt_doc: dict, preds: List[dict], names: List[str]) -> Dict[str, object]:
    gt = _coco_from_dict(gt_doc)
    if not preds:
        return {"note": "no predictions", "AP": 0.0, "AP50": 0.0, "AP75": 0.0}
    with contextlib.redirect_stdout(io.StringIO()):
        dt = gt.loadRes(preds)
        ev = COCOeval(gt, dt, iouType="bbox")
        ev.params.areaRng = list(SIZE_BUCKETS.values())
        ev.params.areaRngLbl = list(SIZE_BUCKETS.keys())
        ev.params.maxDets = [1, 10, 100]
        ev.evaluate()
        ev.accumulate()
    out: Dict[str, object] = {}
    out["AP"] = _ap_at(ev, None, 0)
    out["AP50"] = _ap_at(ev, 0.5, 0)
    out["AP75"] = _ap_at(ev, 0.75, 0)
    out["by_size"] = {}
    for ai, lbl in enumerate(SIZE_BUCKETS):
        out["by_size"][lbl] = {
            "AP": _ap_at(ev, None, ai),
            "AP50": _ap_at(ev, 0.5, ai),
            "AR100": _recall_at(ev, ai),
        }
    out["per_class_AP50"] = {}
    cat_ids = ev.params.catIds
    for ki, cid in enumerate(cat_ids):
        name = names[cid] if 0 <= cid < len(names) else str(cid)
        n_gt = sum(1 for a in gt_doc["annotations"] if a["category_id"] == cid and not a.get("iscrowd"))
        out["per_class_AP50"][name] = {"AP50": _ap_at(ev, 0.5, 0, ki), "AP": _ap_at(ev, None, 0, ki), "gt_boxes": n_gt}
    return out


def evaluate(gt_path: Path, pred_path: Path, spec: Optional[ClassSpec] = None) -> Dict[str, object]:
    spec = spec or load_classes()
    gt_doc = json.load(open(gt_path, "r", encoding="utf-8"))
    preds = json.load(open(pred_path, "r", encoding="utf-8"))
    if isinstance(preds, dict) and "predictions" in preds:
        speed = preds.get("speed")
        preds = preds["predictions"]
    else:
        speed = None
    leaf = evaluate_level(gt_doc, preds, spec.leaves)
    gt_p, preds_p = _remap_to_parents(gt_doc, preds, spec)
    parent = evaluate_level(gt_p, preds_p, spec.parent_names())
    return {
        "gt": str(gt_path),
        "pred": str(pred_path),
        "images": len(gt_doc["images"]),
        "gt_boxes": len(gt_doc["annotations"]),
        "predictions": len(preds),
        "leaf": leaf,
        "parent": parent,
        "speed": speed,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gt", required=True)
    ap.add_argument("--pred", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    res = evaluate(Path(args.gt), Path(args.pred))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(args.out, "w", encoding="utf-8"), indent=2)
    from .report import to_markdown

    md = Path(args.out).with_suffix(".md")
    md.write_text(to_markdown(res), encoding="utf-8")
    print(to_markdown(res))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
