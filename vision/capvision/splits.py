"""Group-aware train/val/test splitting.

Rules:
1. A group (scene, clip, flight, or duplicate cluster) is never divided across splits.
2. If a record carries an official split hint we want to honour (for example HERIDAL's test list),
   its whole group follows that hint.
3. Remaining groups are assigned greedily, largest first, to the split whose per-class deficit is
   largest, so rare classes end up in every split rather than all in train.
"""

from __future__ import annotations

import random
from collections import defaultdict
from typing import Dict, List, Optional, Sequence

from .schema import ImageRecord

SPLITS = ("train", "val", "test")


def assign_splits(
    records: Sequence[ImageRecord],
    group_of: Sequence[str],
    ratios: Dict[str, float] = None,
    honour_hints: bool = False,
    seed: int = 0,
) -> List[str]:
    ratios = ratios or {"train": 0.8, "val": 0.1, "test": 0.1}
    assert abs(sum(ratios.values()) - 1.0) < 1e-6
    rng = random.Random(seed)

    members: Dict[str, List[int]] = defaultdict(list)
    for i, g in enumerate(group_of):
        members[g].append(i)

    # class totals per group
    group_counts: Dict[str, Dict[str, int]] = {}
    total: Dict[str, int] = defaultdict(int)
    for g, idxs in members.items():
        c: Dict[str, int] = defaultdict(int)
        for i in idxs:
            for k, v in records[i].class_counts.items():
                c[k] += v
        c["__images__"] = len(idxs)
        group_counts[g] = dict(c)
        for k, v in c.items():
            total[k] += v

    assigned: Dict[str, str] = {}
    have: Dict[str, Dict[str, int]] = {s: defaultdict(int) for s in SPLITS}

    def take(g: str, s: str) -> None:
        assigned[g] = s
        for k, v in group_counts[g].items():
            have[s][k] += v

    if honour_hints:
        for g, idxs in members.items():
            hints = {records[i].split_hint for i in idxs if records[i].split_hint}
            if len(hints) == 1:
                take(g, hints.pop())
            # mixed hints inside one group -> fall through to greedy assignment

    pending = [g for g in members if g not in assigned]
    rng.shuffle(pending)
    pending.sort(key=lambda g: -group_counts[g]["__images__"])  # large groups first, ties random

    for g in pending:
        best, best_score = None, None
        for s in SPLITS:
            if ratios.get(s, 0) <= 0:
                continue
            # deficit: how far this split is below its target share, summed over classes present in g
            score = 0.0
            for k in group_counts[g]:
                target = ratios[s] * total[k]
                score += (target - have[s][k]) / max(1.0, target)
            if best_score is None or score > best_score:
                best, best_score = s, score
        take(g, best)

    return [assigned[g] for g in group_of]


def split_report(records: Sequence[ImageRecord], splits: Sequence[str]) -> Dict[str, Dict[str, int]]:
    out: Dict[str, Dict[str, int]] = {s: defaultdict(int) for s in SPLITS}
    for r, s in zip(records, splits):
        out[s]["images"] += 1
        if not r.boxes:
            out[s]["empty_images"] += 1
        for k, v in r.class_counts.items():
            out[s][k] += v
    return {s: dict(sorted(v.items())) for s, v in out.items()}
