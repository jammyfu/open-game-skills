"""Offline module/byte transport. Never changes browser network policy.

Only the reviewed engine import specifiers and fixture byte transport change.
Candidates provide two implementation modules, never browser drivers or oracles.
"""
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
CANDIDATE_FILES = ('simulation.mjs', 'asset-pool.mjs')
ENGINE_FILES = {
    'three': 'vendor/three/build/three.module.js',
    'ogs/three-core': 'vendor/three/build/three.core.js',
    'ogs/gltf-loader': 'vendor/three/examples/jsm/loaders/GLTFLoader.js',
    'ogs/buffer-utils': 'vendor/three/examples/jsm/utils/BufferGeometryUtils.js',
}


def read_candidate(directory: Path) -> dict[str, str]:
    directory = Path(directory)
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError('candidate must be a local directory, not a symlink')
    if directory.resolve() != HERE and {p.name for p in directory.iterdir()} != set(CANDIDATE_FILES):
        raise ValueError('candidate directory must contain exactly simulation.mjs and asset-pool.mjs')
    result = {}
    for name in CANDIDATE_FILES:
        path = directory / name
        if path.is_symlink() or not path.is_file() or not 0 < path.stat().st_size <= 200_000:
            raise ValueError('missing, linked, empty or oversized candidate module: ' + name)
        result[name] = path.read_text(encoding='utf-8')
    return result


def build_modules(runtime: Path, candidate: dict[str, str]) -> dict[str, str]:
    modules = {alias: (runtime / rel).read_text(encoding='utf-8') for alias, rel in ENGINE_FILES.items()}
    modules['three'] = modules['three'].replace("'./three.core.js'", "'ogs/three-core'")
    modules['ogs/gltf-loader'] = modules['ogs/gltf-loader'].replace("'../utils/BufferGeometryUtils.js'", "'ogs/buffer-utils'")
    for name, text in candidate.items():
        modules['candidate/' + name] = text
    for name in CANDIDATE_FILES:
        modules['reference/' + name] = (HERE / name).read_text(encoding='utf-8')
    modules['ogs/oracle'] = (HERE / 'oracle.mjs').read_text(encoding='utf-8')
    browser = (HERE / 'browser.mjs').read_text(encoding='utf-8')
    replacements = {
        "'/runtime/vendor/three/examples/jsm/loaders/GLTFLoader.js'": "'ogs/gltf-loader'",
        "'./simulation.mjs'": "'ogs/oracle'",
        "'./asset-pool.mjs'": "'ogs/oracle'",
        'return loader.loadAsync(assetUrl);': "return loader.parseAsync(globalThis.__ogsFixture.slice(0), '');",
    }
    for before, after in replacements.items():
        if browser.count(before) != 1:
            raise ValueError('unreviewed browser transport shape: ' + before)
        browser = browser.replace(before, after)
    modules['ogs/browser'] = browser
    return modules


def offline_html() -> str:
    # Strip only script tags; the existing viewport and diagnostic layout remain.
    return re.sub(r'<script\b[^>]*>.*?</script>', '', (HERE / 'index.html').read_text(), flags=re.S)


INSTALL_MODULES = """async ({modules, fixture}) => {
  const bytes = Uint8Array.from(atob(fixture), ch => ch.charCodeAt(0));
  globalThis.__ogsFixture = bytes.buffer;
  const imports = {};
  for (const [key, source] of Object.entries(modules)) {
    imports[key] = URL.createObjectURL(new Blob([source], {type: 'text/javascript'}));
  }
  const map = document.createElement('script'); map.type = 'importmap';
  map.textContent = JSON.stringify({imports}); document.head.append(map);
  await import('ogs/browser');
}"""
