"""Static packaging/ownership regressions; not agent or game evaluations."""
from pathlib import Path
import tempfile
import unittest
import yaml

from tools.install import install
from tools.skill_quality import markdown_errors

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'skills'


class PackBoundaryTests(unittest.TestCase):
    def test_copy_install_keeps_all_markdown_references_resolvable(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = install(PACK, Path(tmp) / 'agent skills', copy=True)
            errors = []
            for path in sorted(target.rglob('*.md')):
                errors.extend(markdown_errors(path, path.read_text(encoding='utf-8'), target))
            self.assertEqual(errors, [])

    def test_legacy_docs_are_redirects_to_bundled_reference_owner(self):
        for name in ('sprite-image-catalog.md', 'vfx-image-prompts.md'):
            with self.subTest(name=name):
                text = (ROOT / 'docs' / name).read_text(encoding='utf-8')
                self.assertIn(f'../skills/references/{name}', text)
                self.assertNotIn('```', text, 'do not maintain a second prompt pack')

    def test_vfx_prompt_is_a_compatibility_entry(self):
        text = (PACK / 'disciplines/vfx-prompt/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('../../assets/vfx-generate/SKILL.md', text)
        self.assertNotIn('## Image 2.5 contract', text)
        self.assertNotIn('model=gpt-image-2.5-*', text)

    def test_sprite_catalog_and_atlas_have_distinct_output_owners(self):
        inventory = (PACK / '2d/sprite-catalog/SKILL.md').read_text(encoding='utf-8')
        packing = (PACK / '2d/sprite-atlas/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('asset manifest', inventory)
        self.assertIn('../sprite-atlas/SKILL.md', inventory)
        for field in ('source_size', 'trim_offset', 'pivot', 'duration_ms'):
            self.assertIn(field, packing)

    def test_generic_planning_and_validation_support_noncombat(self):
        for name in ('game-planning', 'gameplay-validation'):
            text = (PACK / f'disciplines/{name}/SKILL.md').read_text(encoding='utf-8')
            with self.subTest(name=name):
                self.assertIn('core challenge', text)
                self.assertIn('noncombat', text)
                self.assertNotIn('Finish one meaningful fight', text)
                self.assertNotIn('teach first verb → first fight', text)

    def test_failed_ci_preserves_diagnostics_without_masking_failures(self):
        # SafeLoader uses YAML 1.1 for 'on'; this test inspects jobs only.
        workflow = yaml.safe_load((ROOT / '.github/workflows/skill-quality.yml').read_text())
        self.assertEqual(workflow['permissions'], {'contents': 'read'})
        steps = workflow['jobs']['quality']['steps']
        checkout = next(s for s in steps if s.get('id') == 'checkout')
        self.assertIs(checkout['with']['persist-credentials'], False)
        for step in steps:
            self.assertNotIn('continue-on-error', step)
        archive = next(s for s in steps if s.get('name', '').startswith('Archive'))
        self.assertIn("steps.checkout.outcome == 'success'", archive['if'])
        self.assertIn('!cancelled()', archive['if'])
        self.assertIn('git archive', archive['run'])


if __name__ == '__main__':
    unittest.main()
