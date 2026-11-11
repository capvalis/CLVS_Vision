"""Rebuild an exact dataset archive using public source bytes and saved tar headers."""

import argparse
import base64
import gzip
import hashlib
import json
import shutil
import subprocess
import threading
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    'HERIDAL': [
        {'url': 'https://zenodo.org/api/records/5662351/files/heridal_keras_retinanet_voc.zip/content',
         'size': 4974743004, 'extract': False},
    ],
    'HIT-UAV': [
        {'url': 'https://zenodo.org/api/records/7633134/files/suojiashun/HIT-UAV-Infrared-Thermal-Dataset-v1.2.1.zip/content',
         'size': 814751578, 'extract': True},
    ],
    'TNO': [
        {'url': 'https://ndownloader.figshare.com/files/1475454', 'size': 122712465, 'extract': True},
        {'url': 'https://ndownloader.figshare.com/files/37872186', 'size': 108241, 'extract': False},
    ],
    'military_object_dataset': [
        {'url': 'https://www.kaggle.com/api/v1/datasets/download/rawsi18/military-assets-dataset-12-classes-yolo8-format?datasetVersionNumber=5',
         'extract': True},
    ],
}


def digest_file(path):
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(4 * 1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def download_sources(name, cache):
    index = {}
    for number, source in enumerate(SOURCES[name]):
        path = cache / f'source-{number}.bin'
        command = ['curl', '--fail', '--location', '--retry', '5', '--retry-delay', '5',
                   '--user-agent', 'kaggle-api-v1.7.4', '--output', str(path)]
        if 'size' in source:
            command.extend(['--range', f"0-{source['size'] - 1}"])
        command.append(source['url'])
        subprocess.run(command, check=True)
        if 'size' in source:
            if path.stat().st_size < source['size']:
                raise RuntimeError('Downloaded source is shorter than the local snapshot.')
            # HERIDAL was only partly downloaded in the original local snapshot.
            # Preserve that exact prefix, even if the server ignores the Range request.
            with path.open('r+b') as handle:
                handle.truncate(source['size'])
        index[digest_file(path)] = path
        if source['extract']:
            target = cache / f'extracted-{number}'
            target.mkdir()
            with zipfile.ZipFile(path) as archive:
                for member in archive.infolist():
                    if member.is_dir():
                        continue
                    destination = (target / member.filename).resolve()
                    if not destination.is_relative_to(target.resolve()):
                        raise RuntimeError('Unsafe path in source archive.')
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(member) as original, destination.open('wb') as copied:
                        shutil.copyfileobj(original, copied, 4 * 1024 * 1024)
                    index[digest_file(destination)] = destination
        print(f'Indexed source {number + 1} for {name}', flush=True)
    return index


def rebuild(name, destination, local_source=None):
    manifest = json.loads((ROOT / 'Dataset/manifest.json').read_text())
    expected = next(dataset for dataset in manifest['datasets'] if dataset['name'] == name)
    recipe_dir = ROOT / 'Dataset/archive-recipes'
    records = json.loads(gzip.decompress((recipe_dir / f'{name}.recipe.json.gz').read_bytes()))
    destination.mkdir(parents=True, exist_ok=True)
    cache = destination / 'source-cache'
    cache.mkdir()
    index = {} if local_source else download_sources(name, cache)
    sources = []
    for record in records:
        if 'inline' in record:
            content = base64.b64decode(record['inline'])
            if len(content) != record['size'] or hashlib.sha256(content).hexdigest() != record['sha256']:
                raise RuntimeError(f"Inline content mismatch: {record['path']}")
            sources.append(content)
        else:
            path = local_source / record['path'] if local_source else index.get(record['sha256'])
            if path is None or path.stat().st_size != record['size'] or digest_file(path) != record['sha256']:
                raise RuntimeError(f"Public source does not match the local file: {record['path']}")
            sources.append(path)
    print(f'All {len(records):,} source files match their local SHA-256 hashes.', flush=True)

    compressor = subprocess.Popen(['zstd', '-T2', '-3', '--no-progress', '-c'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    writer_errors = []

    def write_tar():
        try:
            with gzip.open(recipe_dir / f'{name}.headers.gz', 'rb') as headers:
                for record, source in zip(records, sources):
                    prefix = headers.read(record['header_bytes'])
                    if len(prefix) != record['header_bytes']:
                        raise RuntimeError('Truncated archive headers.')
                    compressor.stdin.write(prefix)
                    if isinstance(source, bytes):
                        compressor.stdin.write(source)
                    else:
                        with source.open('rb') as content:
                            shutil.copyfileobj(content, compressor.stdin, 4 * 1024 * 1024)
                shutil.copyfileobj(headers, compressor.stdin)
        except BaseException as error:
            writer_errors.append(error)
        finally:
            compressor.stdin.close()

    writer = threading.Thread(target=write_tar)
    writer.start()
    complete_hash = hashlib.sha256()
    try:
        for part in expected['parts']:
            digest = hashlib.sha256()
            remaining = part['size_bytes']
            with (destination / part['name']).open('wb') as output:
                while remaining:
                    block = compressor.stdout.read(min(4 * 1024 * 1024, remaining))
                    if not block:
                        raise RuntimeError('Reconstructed archive ended too early.')
                    output.write(block)
                    digest.update(block)
                    complete_hash.update(block)
                    remaining -= len(block)
            if digest.hexdigest() != part['sha256']:
                raise RuntimeError(f"Reconstructed part does not match: {part['name']}")
            print(f"Exact archive part verified: {part['name']}", flush=True)
        if compressor.stdout.read(1):
            raise RuntimeError('Reconstructed archive has unexpected extra bytes.')
        writer.join()
        if writer_errors:
            raise writer_errors[0]
        if compressor.wait() or complete_hash.hexdigest() != expected['archive_sha256']:
            raise RuntimeError('Complete archive checksum mismatch.')
    finally:
        if compressor.poll() is None:
            compressor.terminate()
        writer.join()
        compressor.wait()
    print('Reconstructed archive is byte-for-byte identical to the local snapshot.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dataset', choices=sorted(SOURCES))
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--local-source', type=Path, help='Verify reconstruction with local files instead of downloading.')
    args = parser.parse_args()
    rebuild(args.dataset, args.output, args.local_source)
