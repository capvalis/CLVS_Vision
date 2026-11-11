# Raw dataset snapshot

All raw dataset content from the local Computer Vision folder is stored in the [raw-datasets-2026-11-11 GitHub release](https://github.com/capvalis/CLVS_Vision/releases/tag/raw-datasets-2026-11-11). This includes downloaded archives, extracted data, frames, annotations, and metadata. Only macOS `.DS_Store` files are omitted.

| Folder | Files | Original bytes |
| --- | ---: | ---: |
| `HERIDAL/` | 2 | 4,974,743,004 |
| `HIT-UAV/` | 17,437 | 1,644,590,447 |
| `Halmstad/` | 70,035 | 2,012,341,528 |
| `MendeleyVehicles/` | 0 | 0 |
| `TNO/` | 583 | 379,181,770 |
| `military_object_dataset/` | 52,632 | 4,185,478,976 |
| **Total** | **140,689** | **13,196,335,725** |

`MendeleyVehicles/raw/` was empty in the source and is preserved as an empty directory. This is a snapshot of the files that were present, not a claim that every upstream dataset release was fully downloaded.

Each dataset is a `.tar.zst` archive divided into numbered parts of at most 1,900,000,000 bytes. Every part is required for that dataset; concatenate them in numeric order before decompression. [manifest.json](manifest.json) records download URLs, sizes, file counts, and SHA-256 hashes. [SHA256SUMS.txt](SHA256SUMS.txt) lists the hash of each downloadable part.

## Download and restore

Install Zstandard first (`brew install zstd` on macOS or `sudo apt-get install zstd` on Debian/Ubuntu). Restoring everything needs about 27 GB of free disk space for the downloaded archives and extracted files together.

Run this from the repository root. It downloads all six datasets, resumes interrupted downloads, verifies every part, then restores the original paths beneath `Dataset/`. Extraction replaces files with matching paths, so use a fresh clone if you have local dataset changes to preserve.

```bash
bash <<'SH'
set -euo pipefail
command -v zstd >/dev/null
repo_dir="$PWD"
release_url='https://github.com/capvalis/CLVS_Vision/releases/download/raw-datasets-2026-11-11'
mkdir -p .dataset-downloads
cd .dataset-downloads

curl --fail --location --retry 3 "$release_url/SHA256SUMS.txt" --output SHA256SUMS.txt
while read -r checksum asset; do
  curl --fail --location --retry 3 --continue-at - "$release_url/$asset" --output "$asset"
done < SHA256SUMS.txt

if command -v sha256sum >/dev/null 2>&1; then
  sha256sum --check SHA256SUMS.txt
else
  shasum -a 256 --check SHA256SUMS.txt
fi

for dataset in HERIDAL HIT-UAV Halmstad MendeleyVehicles TNO military_object_dataset; do
  cat "$dataset.tar.zst".part* | zstd -d -c | tar -xf - -C "$repo_dir"
done
SH
```

To restore just one dataset, download all of its numbered parts from the release, verify those parts against `SHA256SUMS.txt`, and run the corresponding `cat … | zstd -d -c | tar -xf -` command from the example above. Downloaded archives in `.dataset-downloads/` can be removed after a successful restore.

Raw dataset directories remain ignored by Git. Their documentation and export metadata are also available as ordinary repository files, alongside the release manifest and checksums.
