"""Exact and near-duplicate detection.

Exact duplicates: MD5 of the file bytes.
Near duplicates: 64-bit difference hash (dHash) of a 9x8 grayscale thumbnail; two images are near
duplicates when their hashes differ in at most `max_distance` bits. Candidate pairs are found by
bucketing the hash into 8 byte-chunks (pigeonhole: any pair within 7 bits shares a chunk), so the
check is close to linear in the number of images instead of quadratic.

Result: a union-find over images so that a whole cluster of duplicates stays in one split, and the
cluster representative is the one image kept for training.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from PIL import Image

from .schema import ImageRecord


def md5_of(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dhash_of(path: Path, size: int = 8) -> int:
    with Image.open(path) as im:
        im = im.convert("L").resize((size + 1, size), Image.Resampling.BILINEAR)
        px = list(im.getdata())
    bits = 0
    for row in range(size):
        for col in range(size):
            left = px[row * (size + 1) + col]
            right = px[row * (size + 1) + col + 1]
            bits = (bits << 1) | (1 if left > right else 0)
    return bits


class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))

    def find(self, a: int) -> int:
        while self.parent[a] != a:
            self.parent[a] = self.parent[self.parent[a]]
            a = self.parent[a]
        return a

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[max(ra, rb)] = min(ra, rb)


def compute_hashes(records: Sequence[ImageRecord], progress: bool = True, need_dhash: bool = True) -> None:
    it: Iterable[ImageRecord] = records
    if progress:
        try:
            from tqdm import tqdm

            it = tqdm(records, desc="hashing", unit="img")
        except ImportError:
            pass
    for r in it:
        if r.md5 is None:
            r.md5 = md5_of(r.path)
        if need_dhash and r.dhash is None:
            r.dhash = dhash_of(r.path)


def duplicate_clusters(
    records: Sequence[ImageRecord], max_distance: int = 6
) -> Tuple[List[int], Dict[str, int]]:
    """Return (cluster id per record, stats). Requires compute_hashes() first.

    max_distance < 0 disables the near-duplicate pass (exact MD5 only). Use that for video-frame
    datasets whose scene grouping already keeps related frames together; the bucket comparison is
    quadratic inside each bucket and very slow on tens of thousands of near-identical frames.
    """
    n = len(records)
    uf = UnionFind(n)
    exact_pairs = 0
    near_pairs = 0

    by_md5: Dict[str, int] = {}
    for i, r in enumerate(records):
        assert r.md5 is not None, "call compute_hashes first"
        if r.md5 in by_md5:
            uf.union(by_md5[r.md5], i)
            exact_pairs += 1
        else:
            by_md5[r.md5] = i

    buckets: Dict[Tuple[int, int], List[int]] = defaultdict(list)
    if max_distance >= 0:
        for i, r in enumerate(records):
            assert r.dhash is not None, "call compute_hashes with need_dhash=True"
            h = r.dhash
            for chunk in range(8):
                buckets[(chunk, (h >> (8 * chunk)) & 0xFF)].append(i)

    checked = set()
    for members in buckets.values():
        if len(members) < 2:
            continue
        for a_idx in range(len(members)):
            a = members[a_idx]
            for b_idx in range(a_idx + 1, len(members)):
                b = members[b_idx]
                key = (a, b) if a < b else (b, a)
                if key in checked:
                    continue
                checked.add(key)
                if records[a].md5 == records[b].md5:
                    continue
                if bin(records[a].dhash ^ records[b].dhash).count("1") <= max_distance:
                    uf.union(a, b)
                    near_pairs += 1

    roots = [uf.find(i) for i in range(n)]
    cluster_ids: Dict[int, int] = {}
    out = []
    for r in roots:
        if r not in cluster_ids:
            cluster_ids[r] = len(cluster_ids)
        out.append(cluster_ids[r])
    stats = {
        "images": n,
        "clusters": len(cluster_ids),
        "exact_duplicate_pairs": exact_pairs,
        "near_duplicate_pairs": near_pairs,
        "images_removed_if_one_per_cluster": n - len(cluster_ids),
    }
    return out, stats
