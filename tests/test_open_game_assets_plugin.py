import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SRC = ROOT / 'plugins' / 'open-game-assets'
BUILDER = ROOT / 'tools' / 'build_open_game_assets_plugin.py'
SKILL_SRC = ROOT / 'skills' / 'assets' / 'open-asset-fixture'


class OpenGameAssetsPluginTests(unittest.TestCase):
    def test_portable_manifest_exists_and_is_skills_only(self):
        manifest_path = PLUGIN_SRC / 'plugin.json'
        self.assertTrue(manifest_path.is_file(), 'missing portable plugin.json')
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        self.assertEqual(manifest['$schema'], 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json')
        self.assertEqual(manifest['name'], 'open-game-assets')
        self.assertRegex(manifest['version'], r'^\d+\.\d+\.\d+$')
        self.assertEqual(manifest['repository'], 'https://github.com/jammyfu/open-game-skills')
        self.assertEqual(manifest['license'], 'MIT')
        self.assertNotIn('skills', manifest, 'portable plugins discover skills from root skills/')
        openai = manifest.get('extensions', {}).get('com.openai', {})
        self.assertNotIn('apps', openai)
        self.assertNotIn('hooks', openai)
        self.assertIn('interface', openai)
        interface = openai['interface']
        self.assertEqual(interface['displayName'], 'Open Game Assets')
        self.assertGreaterEqual(len(interface['defaultPrompt']), 2)

    def test_builder_outputs_flat_self_contained_skill_package(self):
        self.assertTrue(BUILDER.is_file(), 'missing plugin build tool')
        with tempfile.TemporaryDirectory(prefix='open-game-assets-plugin-') as td:
            out = Path(td) / 'open-game-assets'
            result = subprocess.run(
                [sys.executable, str(BUILDER), '--output', str(out)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((out / 'plugin.json').is_file())
            skill = out / 'skills' / 'open-asset-fixture'
            self.assertTrue((skill / 'SKILL.md').is_file())
            self.assertEqual((skill / 'SKILL.md').read_bytes(), (SKILL_SRC / 'SKILL.md').read_bytes())
            for rel in [
                'assets/catalog.json',
                'assets/request.example.json',
                'assets/pin.request.example.json',
                'reference/sources.md',
                'reference/usage.md',
                'scripts/asset_fixture.py',
                'scripts/fixture_lock.py',
                'scripts/prepare_assets.py',
            ]:
                self.assertEqual((skill / rel).read_bytes(), (SKILL_SRC / rel).read_bytes(), rel)
            nested = list((out / 'skills').glob('*/*/SKILL.md'))
            self.assertEqual(nested, [], f'nested skill manifests are not submission-compatible: {nested}')
            self.assertFalse((out / '.agents').exists())
            self.assertFalse((out / 'mcp.json').exists())
            self.assertFalse((out / '.mcp.json').exists())
            self.assertFalse((out / '.app.json').exists())

    def test_builder_can_emit_submission_zip_without_wrapping_directory(self):
        with tempfile.TemporaryDirectory(prefix='open-game-assets-plugin-') as td:
            archive = Path(td) / 'open-game-assets.zip'
            result = subprocess.run(
                [sys.executable, str(BUILDER), '--zip', str(archive)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(archive.is_file())
            with zipfile.ZipFile(archive) as zf:
                names = set(zf.namelist())
                self.assertIn('plugin.json', names)
                self.assertIn('skills/open-asset-fixture/SKILL.md', names)
                self.assertFalse(any(name.startswith('open-game-assets/') for name in names))
                self.assertFalse(any('/.git/' in name or name.startswith('.git/') for name in names))
                self.assertFalse(any('__pycache__' in name for name in names))


if __name__ == '__main__':
    unittest.main()
