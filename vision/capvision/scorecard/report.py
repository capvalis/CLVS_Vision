"""Markdown rendering of a scorecard result."""

from __future__ import annotations

import math
from typing import Dict


def _f(x) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "-"
    return f"{100 * x:.1f}"


def to_markdown(res: Dict[str, object]) -> str:
    L = [f"# Scorecard", "", f"Ground truth: `{res['gt']}`  ", f"Predictions: `{res['pred']}`  ",
         f"Images {res['images']}, ground-truth boxes {res['gt_boxes']}, predictions {res['predictions']}.", ""]
    for level in ("parent", "leaf"):
        r = res[level]
        L += [f"## {level.capitalize()}-level classes", "",
              f"AP {_f(r.get('AP'))} | AP50 {_f(r.get('AP50'))} | AP75 {_f(r.get('AP75'))}", ""]
        if "by_size" in r:
            L += ["| Size (longest side) | AP | AP50 | Recall@100 |", "|---|---:|---:|---:|"]
            for k, v in r["by_size"].items():
                L.append(f"| {k} | {_f(v['AP'])} | {_f(v['AP50'])} | {_f(v['AR100'])} |")
            L.append("")
        if "per_class_AP50" in r:
            L += ["| Class | AP50 | AP | GT boxes |", "|---|---:|---:|---:|"]
            for k, v in r["per_class_AP50"].items():
                L.append(f"| {k} | {_f(v['AP50'])} | {_f(v['AP'])} | {v['gt_boxes']} |")
            L.append("")
    sp = res.get("speed")
    if sp:
        L += ["## Speed", "", "| Device | Input | Batch | ms/img p50 | p95 | p99 | FPS p50 |", "|---|---|---:|---:|---:|---:|---:|",
              f"| {sp.get('device')} | {sp.get('input_size')} | {sp.get('batch')} | {sp.get('ms_p50'):.1f} | {sp.get('ms_p95'):.1f} | {sp.get('ms_p99'):.1f} | {1000.0 / max(sp.get('ms_p50'), 1e-6):.1f} |", ""]
    return "\n".join(L)
