"""Build the portable skills-only Open Game Assets plugin from canonical source."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_META = ROOT / "plugins" / "open-game-assets"
SKILL_SOURCE = ROOT / "skills" / "assets" / "open-asset-fixture"
SKILL_NAME = "open-asset-fixture"

IGNORED_NAMES = {"__pycache__", ".DS_Store"}


def _validate_sources() -> None:
    manifest = PLUGIN_META / "plugin.json"
    skill_manifest = SKILL_SOURCE / "SKILL.md"
    if not manifest.is_file():
        raise FileNotFoundError(f"missing plugin manifest: {manifest}")
    if not skill_manifest.is_file():
        raise FileNotFoundError(f"missing skill manifest: {skill_manifest}")
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if data.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        raise ValueError("plugin.json must use the Agent Plugins 1.0.0 schema")
    if data.get("name") != "open-game-assets":
        raise ValueError("plugin name must remain open-game-assets")


def _copy_skill(source: Path, destination: Path) -> None:
    def ignore(_dir: str, names: list[str]) -> set[str]:
        return {name for name in names if name in IGNORED_NAMES or name.endswith(".pyc")}

    shutil.copytree(source, destination, ignore=ignore, symlinks=False)
    for path in destination.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"submission package may not contain symlinks: {path}")


def build_directory(destination: Path) -> Path:
    _validate_sources()
    destination = destination.expanduser().resolve()
    if destination.exists():
        raise FileExistsError(f"refusing to overwrite existing output: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir()
    shutil.copy2(PLUGIN_META / "plugin.json", destination / "plugin.json")
    skill_destination = destination / "skills" / SKILL_NAME
    skill_destination.parent.mkdir()
    _copy_skill(SKILL_SOURCE, skill_destination)
    return destination


def _zip_tree(source: Path, archive: Path) -> Path:
    archive = archive.expanduser().resolve()
    if archive.exists():
        raise FileExistsError(f"refusing to overwrite existing archive: {archive}")
    archive.parent.mkdir(parents=True, exist_ok=True)
    files = sorted(path for path in source.rglob("*") if path.is_file())
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in files:
            relative = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(relative)
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return archive


def build_zip(archive: Path) -> Path:
    with tempfile.TemporaryDirectory(prefix="open-game-assets-build-") as temp:
        package = build_directory(Path(temp) / "package")
        return _zip_tree(package, archive)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    output = parser.add_mutually_exclusive_group(required=True)
    output.add_argument("--output", type=Path, help="Build an unpacked portable plugin directory")
    output.add_argument("--zip", dest="archive", type=Path, help="Build a submission-ready ZIP")
    args = parser.parse_args()
    try:
        built = build_directory(args.output) if args.output else build_zip(args.archive)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(1, f"Build failed: {exc}\n")
    print(built)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
