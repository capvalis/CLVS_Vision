"""Launch D-FINE training for a generated config, single process, on cpu / mps / cuda.

Example:
    python -m capvision.train.run --name kaggle_v1_s640 --device mps --pretrained obj365
    python -m capvision.train.run --name kaggle_v1_s640 --device cuda --pretrained obj365 --amp

--pretrained downloads the matching official checkpoint into vision/weights/ if missing:
    coco      -> dfine_<size>_coco.pth
    obj365    -> dfine_<size>_obj365.pth      (best starting point for new domains)
    obj2coco  -> dfine_<size>_obj2coco.pth
or pass a path to a .pth file.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

import yaml

from .. import DFINE_DIR, RUNS_DIR, WEIGHTS_DIR

WEIGHT_URLS = {
    "coco": "https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_{size}_coco.pth",
    "obj365": "https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_{size}_obj365.pth",
    "obj2coco": "https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_{size}_obj2coco.pth",
}


def ensure_weights(kind: str, size: str) -> Path:
    if kind.endswith(".pth"):
        p = Path(kind)
        if not p.is_file():
            raise FileNotFoundError(p)
        return p
    WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
    url = WEIGHT_URLS[kind].format(size=size)
    dst = WEIGHTS_DIR / Path(url).name
    if not dst.is_file():
        print(f"[weights] downloading {url}", file=sys.stderr)
        tmp = dst.with_suffix(".part")
        urllib.request.urlretrieve(url, tmp)
        tmp.rename(dst)
    return dst


def model_size_of(config: Path) -> str:
    """Infer the D-FINE size letter from the backbone block of a generated config."""
    cfg = yaml.safe_load(open(config))
    hg = cfg.get("HGNetv2", {})
    name = hg.get("name", "B0")
    if name == "B0":
        return "n" if len(hg.get("return_idx", [1, 2, 3])) == 2 else "s"
    return {"B2": "m", "B4": "l", "B5": "x"}.get(name, "s")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="run name under vision/runs/")
    ap.add_argument("--device", default="cpu", choices=["cpu", "mps", "cuda"])
    ap.add_argument("--pretrained", default=None, help="coco | obj365 | obj2coco | path.pth")
    ap.add_argument("--size", default=None, help="model size letter for weight download; inferred from config if omitted")
    ap.add_argument("--resume", default=None)
    ap.add_argument("--amp", action="store_true")
    ap.add_argument("--test-only", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--update", nargs="*", default=[], help="extra key=value overrides passed to D-FINE -u")
    args = ap.parse_args(argv)

    run_dir = RUNS_DIR / args.name
    config = run_dir / "config.yml"
    if not config.is_file():
        raise FileNotFoundError(f"{config} missing; run make_config first")

    cmd = [sys.executable, str(DFINE_DIR / "train.py"), "-c", str(config), "--device", args.device, "--seed", str(args.seed)]
    if args.pretrained:
        size = args.size or model_size_of(config)
        cmd += ["-t", str(ensure_weights(args.pretrained, size))]
    if args.resume:
        cmd += ["-r", args.resume]
    if args.amp and args.device == "cuda":
        cmd.append("--use-amp")
    if args.test_only:
        cmd.append("--test-only")
    if args.update:
        cmd += ["-u"] + args.update

    env = dict(os.environ)
    env["PYTHONPATH"] = str(DFINE_DIR) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONUNBUFFERED"] = "1"  # otherwise the child's log only appears in 8 KB blocks
    if args.device == "mps":
        env.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
    log = run_dir / "train.log"
    print("[run]", " ".join(cmd), file=sys.stderr)
    with open(log, "a", encoding="utf-8") as lf:
        proc = subprocess.Popen(cmd, cwd=str(DFINE_DIR), env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
            lf.write(line)
            lf.flush()
        proc.wait()
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
