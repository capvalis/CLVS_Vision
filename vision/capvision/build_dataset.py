"""Build a training-ready dataset: import -> deduplicate -> split by group -> write COCO JSON + report.

Usage (from the vision/ folder, inside the venv):
    python -m capvision.build_dataset --sources kaggle_military --name kaggle_v1
    python -m capvision.build_dataset --sources hit_uav heridal seadronessee halmstad --name foundation_v1

Output: vision/datasets/<name>/annotations/instances_{train,val,test}.json, build.json, REPORT.md.
Images are not copied; file_name is relative to the Computer Vision folder (the "image root").
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Dict, List

import yaml

from . import CONFIG_DIR, CV_DIR, DATASETS_OUT
from .classes import load_classes
from .dedup import compute_hashes, duplicate_clusters
from .importers import IMPORTERS
from .schema import ImageRecord, record_summary, write_coco
from .splits import assign_splits, split_report


def load_dataset_cfg() -> Dict[str, dict]:
    with open(CONFIG_DIR / "datasets.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def size_bucket(b_w: float, b_h: float) -> str:
    s = max(b_w, b_h)
    if s < 16:
        return "tiny(<16px)"
    if s < 32:
        return "small(16-32)"
    if s < 96:
        return "medium(32-96)"
    return "large(>96)"


def main(argv: List[str] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sources", nargs="+", required=True, help="keys from configs/datasets.yaml")
    ap.add_argument("--name", required=True, help="output dataset name under vision/datasets/")
    ap.add_argument("--ratios", nargs=3, type=float, default=[0.8, 0.1, 0.1], metavar=("TRAIN", "VAL", "TEST"))
    ap.add_argument("--honour-hints", action="store_true", help="keep the raw dataset's own split where it has one")
    ap.add_argument("--near-dup-bits", type=int, default=6, help="dHash Hamming distance treated as a duplicate")
    ap.add_argument("--keep-duplicates", action="store_true", help="keep all images, only force clusters into one split")
    ap.add_argument("--no-near-dup", action="store_true", help="exact-duplicate check only (fast; for video-frame sets already grouped by clip)")
    ap.add_argument("--drop-empty", action="store_true", help="drop images with no boxes after mapping")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--limit", type=int, default=0, help="debug: keep only the first N records per source")
    args = ap.parse_args(argv)

    t0 = time.time()
    spec = load_classes()
    ds_cfg = load_dataset_cfg()
    out_dir = DATASETS_OUT / args.name
    out_dir.mkdir(parents=True, exist_ok=True)

    records: List[ImageRecord] = []
    import_log: Dict[str, dict] = {}
    for key in args.sources:
        cfg = ds_cfg[key]
        imp = IMPORTERS[cfg["importer"]](spec, cfg, CV_DIR)
        recs = imp.load()
        if args.limit:
            recs = recs[: args.limit]
        import_log[key] = {"records": len(recs), "dropped_labels": dict(imp.dropped), **record_summary(recs)}
        print(f"[import] {key}: {len(recs)} images, dropped={dict(imp.dropped)}", file=sys.stderr)
        records.extend(recs)
    if not records:
        print("nothing imported", file=sys.stderr)
        return 1

    # --- duplicates -------------------------------------------------------------------
    compute_hashes(records, need_dhash=not args.no_near_dup)
    cluster_of, dup_stats = duplicate_clusters(records, max_distance=-1 if args.no_near_dup else args.near_dup_bits)
    print(f"[dedup] {dup_stats}", file=sys.stderr)

    # group = raw group, merged with duplicate cluster (union): images that are duplicates of each
    # other must share a split even if their raw groups differ.
    group_key = [f"{records[i].group}|c{cluster_of[i]}" for i in range(len(records))]
    # merge raw groups that share a cluster
    cluster_to_groups: Dict[int, set] = {}
    for i, c in enumerate(cluster_of):
        cluster_to_groups.setdefault(c, set()).add(records[i].group)
    group_alias: Dict[str, str] = {}
    for c, groups in cluster_to_groups.items():
        rep = min(groups)
        for g in groups:
            # union-find over group names via alias chain
            root_g = g
            while root_g in group_alias and group_alias[root_g] != root_g:
                root_g = group_alias[root_g]
            root_rep = rep
            while root_rep in group_alias and group_alias[root_rep] != root_rep:
                root_rep = group_alias[root_rep]
            if root_g != root_rep:
                group_alias[max(root_g, root_rep)] = min(root_g, root_rep)
    def final_group(g: str) -> str:
        while g in group_alias and group_alias[g] != g:
            g = group_alias[g]
        return g
    group_key = [final_group(r.group) for r in records]

    # --- choose which images to keep -----------------------------------------------------
    keep = [True] * len(records)
    if not args.keep_duplicates:
        seen: Dict[int, int] = {}
        for i, c in enumerate(cluster_of):
            if c in seen:
                # keep the one with more boxes; tie -> first
                j = seen[c]
                if len(records[i].boxes) > len(records[j].boxes):
                    keep[j] = False
                    seen[c] = i
                else:
                    keep[i] = False
            else:
                seen[c] = i
    if args.drop_empty:
        for i, r in enumerate(records):
            if not r.boxes:
                keep[i] = False
    kept = [r for r, k in zip(records, keep) if k]
    kept_groups = [g for g, k in zip(group_key, keep) if k]
    print(f"[keep] {len(kept)} of {len(records)} images", file=sys.stderr)

    # --- split -----------------------------------------------------------------------
    ratios = {"train": args.ratios[0], "val": args.ratios[1], "test": args.ratios[2]}
    splits = assign_splits(kept, kept_groups, ratios, honour_hints=args.honour_hints, seed=args.seed)
    rep = split_report(kept, splits)

    # --- write -----------------------------------------------------------------------
    written = {}
    for s in ("train", "val", "test"):
        recs = [r for r, sp in zip(kept, splits) if sp == s]
        if not recs:
            continue
        written[s] = write_coco(recs, spec, out_dir / "annotations" / f"instances_{s}.json", CV_DIR)

    # --- stats for the report -----------------------------------------------------------
    size_counts: Dict[str, Counter] = {}
    for r in kept:
        for b in r.boxes:
            size_counts.setdefault(b.cls, Counter())[size_bucket(b.w, b.h)] += 1
    raw_split_vs_new = Counter()
    for r, s in zip(kept, splits):
        raw_split_vs_new[(r.split_hint or "none", s)] += 1

    build = {
        "name": args.name,
        "built_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "class_version": spec.version,
        "categories": spec.coco_categories(),
        "image_root": str(CV_DIR),
        "sources": import_log,
        "dedup": dup_stats,
        "kept_images": len(kept),
        "ratios": ratios,
        "honour_hints": args.honour_hints,
        "seed": args.seed,
        "splits": rep,
        "written": written,
        "raw_split_to_new_split": {f"{a}->{b}": n for (a, b), n in sorted(raw_split_vs_new.items())},
        "box_size_buckets": {k: dict(v) for k, v in sorted(size_counts.items())},
        "seconds": round(time.time() - t0, 1),
    }
    with open(out_dir / "build.json", "w", encoding="utf-8") as f:
        json.dump(build, f, indent=2)
    write_report(out_dir / "REPORT.md", build)
    print(f"[done] {out_dir} in {build['seconds']} s", file=sys.stderr)
    return 0


def write_report(path: Path, b: dict) -> None:
    lines = [f"# Dataset build: {b['name']}", "", f"Built {b['built_at']}. Class list version {b['class_version']}. Image root `{b['image_root']}`.", ""]
    lines += ["## Sources", "", "| Source | Images | Empty | Dropped labels |", "|---|---:|---:|---|"]
    for k, v in b["sources"].items():
        lines.append(f"| {k} | {v['images']} | {v['empty_images']} | {v['dropped_labels'] or '-'} |")
    d = b["dedup"]
    lines += ["", "## Duplicates", "", f"- {d['images']} images, {d['clusters']} unique clusters, {d['exact_duplicate_pairs']} exact and {d['near_duplicate_pairs']} near-duplicate pairs.", f"- Kept {b['kept_images']} images (one per cluster unless --keep-duplicates).", ""]
    lines += ["## Splits (boxes per class)", ""]
    classes = sorted({k for s in b["splits"].values() for k in s if k not in ("images", "empty_images")})
    lines += ["| Split | Images | Empty | " + " | ".join(classes) + " |", "|---|---:|---:|" + "---:|" * len(classes)]
    for s, v in b["splits"].items():
        if not v:
            continue
        lines.append(f"| {s} | {v.get('images',0)} | {v.get('empty_images',0)} | " + " | ".join(str(v.get(c, 0)) for c in classes) + " |")
    lines += ["", "## Raw split to new split", "", "| Raw -> new | Images |", "|---|---:|"]
    for k, n in b["raw_split_to_new_split"].items():
        lines.append(f"| {k} | {n} |")
    lines += ["", "## Box sizes (longest side) per class", "", "| Class | tiny(<16px) | small(16-32) | medium(32-96) | large(>96) |", "|---|---:|---:|---:|---:|"]
    for c, v in b["box_size_buckets"].items():
        lines.append(f"| {c} | {v.get('tiny(<16px)',0)} | {v.get('small(16-32)',0)} | {v.get('medium(32-96)',0)} | {v.get('large(>96)',0)} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
