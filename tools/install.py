"""Install the complete pack into a caller-selected agent skills directory."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys


def install(source: Path, target: Path, *, copy: bool = False, dry_run: bool = False) -> Path:
    source = source.expanduser().resolve()
    target = target.expanduser().resolve()
    if not (source / 'SKILL.md').is_file() or not (source / 'dispatcher' / 'SKILL.md').is_file():
        raise FileNotFoundError(f'Incomplete skill pack: {source}')
    destination = target / 'open-game-skills'
    if destination.is_relative_to(source):
        raise ValueError('Destination must not be inside the source pack')
    if destination.is_symlink() and destination.resolve() == source and not copy:
        return destination
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f'Refusing to overwrite {destination}; move it aside explicitly first')
    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)
        if copy:
            shutil.copytree(source, destination, symlinks=True)
        else:
            destination.symlink_to(source, target_is_directory=True)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, required=True, help='The agent skills directory, not the pack subdirectory')
    parser.add_argument('--copy', action='store_true', help='Copy instead of creating a symlink; updates are manual')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        path = install(Path(__file__).resolve().parents[1] / 'skills', args.target, copy=args.copy, dry_run=args.dry_run)
    except (OSError, ValueError) as exc:
        print(f'Install failed: {exc}', file=sys.stderr)
        if isinstance(exc, OSError) and not args.copy:
            print('If symlinks are unavailable, use --copy with an unused destination.', file=sys.stderr)
        return 1
    print(f'{"Would install/check" if args.dry_run else "Installed/verified"}: {path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
