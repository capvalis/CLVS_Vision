"""Export the Halmstad drone-detection videos and MATLAB labels into frames + JSON for capvision.

Input layout (after unzipping the Zenodo release):
    <src>/Data/Video_IR/IR_<CLASS>_<NNN>.mp4 + IR_<CLASS>_<NNN>_LABELS.mat
    <src>/Data/Video_V/V_<CLASS>_<NNN>.mp4  + V_<CLASS>_<NNN>_LABELS.mat
Each .mat is a MATLAB groundTruth with one (x, y, w, h) box per frame or None when the target is
absent (decoded with the mcos-decoder package).

Output layout (what capvision/importers/halmstad.py reads):
    <dst>/frames/<clip>/<index:06d>.jpg
    <dst>/labels/<clip>.json   {"clip","sensor","class","frames":[{"index","boxes":[[x,y,w,h],...]}]}
    <dst>/internet_clips.txt   (copied from --internet-clips if given)

Usage:
    python tools/halmstad_export.py --src ../Dataset/Halmstad/extracted/<dir> --dst ../Dataset/Halmstad --stride 3
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import cv2
import mcos_decoder

NAME_RE = re.compile(r"^(IR|V)_([A-Z]+)_(\d+)$")


def export_clip(mp4: Path, mat: Path, dst: Path, stride: int, quality: int) -> dict:
    m = NAME_RE.match(mp4.stem)
    if not m:
        raise ValueError(f"unexpected clip name {mp4.name}")
    sensor, cls, _ = m.groups()
    boxes = mcos_decoder.load_groundtruth(str(mat))
    cap = cv2.VideoCapture(str(mp4))
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    out_dir = dst / "frames" / mp4.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    frames = []
    idx = 0
    written = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % stride == 0:
            path = out_dir / f"{idx:06d}.jpg"
            if not path.is_file():
                cv2.imwrite(str(path), frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
            b = boxes[idx] if idx < len(boxes) else None
            frames.append({"index": idx, "boxes": [[float(v) for v in b]] if b else []})
            written += 1
        idx += 1
    cap.release()
    doc = {"clip": mp4.stem, "sensor": "IR" if sensor == "IR" else "VISIBLE", "class": cls,
           "video_frames": idx, "label_entries": len(boxes), "stride": stride, "frames": frames}
    (dst / "labels").mkdir(parents=True, exist_ok=True)
    (dst / "labels" / f"{mp4.stem}.json").write_text(json.dumps(doc))
    return {"clip": mp4.stem, "frames_in_video": idx, "frames_written": written, "label_entries": len(boxes),
            "label_mismatch": abs(idx - len(boxes)) > 2, "declared_frames": n_frames}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="extracted release dir containing Data/")
    ap.add_argument("--dst", required=True, help="output root (frames/, labels/)")
    ap.add_argument("--stride", type=int, default=3, help="keep every Nth frame (30 fps source)")
    ap.add_argument("--quality", type=int, default=92)
    ap.add_argument("--internet-clips", default=None, help="text file of clip stems to exclude (copied to dst)")
    args = ap.parse_args()
    src, dst = Path(args.src), Path(args.dst)
    clips = []
    for sub in ("Data/Video_IR", "Data/Video_V"):
        for mp4 in sorted((src / sub).glob("*.mp4")):
            mat = mp4.with_name(mp4.stem + "_LABELS.mat")
            if mat.is_file():
                clips.append((mp4, mat))
            else:
                print(f"[warn] no labels for {mp4.name}", file=sys.stderr)
    print(f"[export] {len(clips)} clips, stride {args.stride}", file=sys.stderr)
    log = []
    for i, (mp4, mat) in enumerate(clips, 1):
        log.append(export_clip(mp4, mat, dst, args.stride, args.quality))
        if i % 25 == 0:
            print(f"[export] {i}/{len(clips)}", file=sys.stderr)
    if args.internet_clips:
        (dst / "internet_clips.txt").write_text(Path(args.internet_clips).read_text())
    summary = {
        "clips": len(log),
        "frames_written": sum(r["frames_written"] for r in log),
        "frames_in_videos": sum(r["frames_in_video"] for r in log),
        "clips_with_label_mismatch": [r["clip"] for r in log if r["label_mismatch"]],
        "stride": args.stride,
    }
    (dst / "export_summary.json").write_text(json.dumps({"summary": summary, "clips": log}, indent=1))
    print(json.dumps(summary, indent=1), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
