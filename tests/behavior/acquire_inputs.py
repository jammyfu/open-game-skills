"""Fetch seven explicitly pinned runtime/asset files, or verify an acquired set.

Network is used only with --download. Does not run downloaded code or import a
third-party game's implementation. Acquisition is not an engine-test result.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_spec() -> dict:
    return json.loads((HERE / 'inputs.json').read_text(encoding='utf-8'))


def validate_entry(row: dict) -> None:
    p = PurePosixPath(row['path'])
    if p.is_absolute() or '..' in p.parts or '\\' in row['path'] or not p.parts:
        raise ValueError('input path escapes fixture directory')
    u = urlsplit(row['url'])
    if (u.scheme != 'https' or u.netloc != 'raw.githubusercontent.com' or u.query or u.fragment
            or not re.fullmatch(r'/[\w.-]+/[\w.-]+/[a-f0-9]{40}/.+', u.path)):
        raise ValueError('only commit-pinned official raw GitHub inputs are supported')
    if not isinstance(row['max_bytes'], int) or not 1 <= row['max_bytes'] <= 4_000_000:
        raise ValueError('download must have a bounded byte size')


def verify_file(root: Path, row: dict) -> None:
    path = root / row['path']
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('input path is not a local regular file')
    data = path.read_bytes()
    if len(data) != row['size'] or digest(data) != row['sha256']:
        raise ValueError(f'input hash/size mismatch: {row["path"]}')


def verify(root: Path) -> dict:
    spec = read_spec()
    report = json.loads((root / 'acquisition.json').read_text(encoding='utf-8'))
    if report['spec_sha256'] != digest((HERE / 'inputs.json').read_bytes()):
        raise ValueError('acquisition uses a different input specification')
    if {r['path'] for r in report['files']} != {r['path'] for r in spec['files']}:
        raise ValueError('acquisition file set does not match specification')
    for row in report['files']:
        verify_file(root, row)
    return report


def download(root: Path) -> dict:
    spec = read_spec()
    if not 1 <= len(spec['files']) <= 10:
        raise ValueError('unexpected input count')
    for row in spec['files']: validate_entry(row)
    if root.exists():
        return verify(root)
    root.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='behavior-acquire-', dir=root.parent) as tmp:
        staging = Path(tmp) / 'runtime'; staging.mkdir()
        results = []
        for row in spec['files']:
            req = Request(row['url'], headers={'User-Agent': 'open-game-skills-behavior-tests/0.1'})
            with urlopen(req, timeout=45) as response:
                if urlsplit(response.url).hostname != 'raw.githubusercontent.com':
                    raise ValueError('unexpected download redirect')
                data = response.read(row['max_bytes'] + 1)
            if len(data) > row['max_bytes']:
                raise ValueError('download exceeds declared limit')
            if row.get('git_blob_sha'):
                git_sha = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
                if git_sha != row['git_blob_sha']:
                    raise ValueError('download differs from reviewed Git blob')
            target = staging / row['path']; target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            results.append({**row, 'size':len(data), 'sha256':digest(data)})
        report = {'schema_version':1, 'status':'acquired-not-imported',
                  'spec_sha256':digest((HERE/'inputs.json').read_bytes()), 'files':results}
        (staging/'acquisition.json').write_text(json.dumps(report,indent=2)+'\n', encoding='utf-8')
        # Destination was not reused; original data remains byte-for-byte.
        if root.exists(): raise FileExistsError(root)
        shutil.move(str(staging), str(root))
    return verify(root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--download',action='store_true')
    args = parser.parse_args()
    try:
        report = download(args.root.resolve()) if args.download else verify(args.root.resolve())
    except (OSError,ValueError,KeyError) as exc:
        parser.exit(1, f'Input preparation failed: {exc}\n')
    print(json.dumps(report,indent=2))
    return 0

if __name__ == '__main__': raise SystemExit(main())
