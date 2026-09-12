import json
from pathlib import Path
import tempfile
import unittest

from tools.skill_quality import collect, markdown_errors, write_catalog, check_catalog


class SkillQualityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def skill(self, name='sample', content=None, folder=None):
        path = self.root / 'skills' / (folder or name) / 'SKILL.md'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content or f'---\nname: {name}\ndescription: Use when testing a skill.\n---\n\n# Sample\n\nDo the task.\n', encoding='utf-8')
        return path

    def test_empty_pack_fails(self):
        self.assertTrue(collect(self.root)[1])

    def test_valid_skill(self):
        self.skill()
        records, errors = collect(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(records[0]['name'], 'sample')

    def test_duplicate_yaml_key_rejected(self):
        self.skill(content='---\nname: sample\nname: other\ndescription: valid\n---\n# Body\n')
        self.assertIn('duplicate', ' '.join(collect(self.root)[1]))

    def test_missing_frontmatter(self):
        self.skill(content='# No frontmatter\n')
        self.assertTrue(collect(self.root)[1])

    def test_bad_name_variants(self):
        for name in ['Bad', '-bad', 'bad-', 'bad--name', 'x' * 65]:
            with self.subTest(name=name):
                self.skill(name=name, folder='sample')
                self.assertTrue(collect(self.root)[1])

    def test_wrong_directory_name(self):
        self.skill(folder='wrong')
        self.assertTrue(collect(self.root)[1])

    def test_distribution_root_uses_installed_name(self):
        path = self.root / 'skills' / 'SKILL.md'
        path.parent.mkdir()
        path.write_text('---\nname: open-game-skills\ndescription: Entry.\n---\n# Entry\n')
        self.assertEqual(collect(self.root)[1], [])

    def test_empty_nonstring_and_overlong_description(self):
        for desc in ['""', '123', 'x' * 1025]:
            with self.subTest(desc=desc[:12]):
                self.skill(content=f'---\nname: sample\ndescription: {desc}\n---\n# Body\n')
                self.assertTrue(collect(self.root)[1])

    def test_description_limit_is_not_total_frontmatter_limit(self):
        self.skill(content='---\nname: sample\ndescription: ' + 'x' * 1024 + '\nmetadata:\n  note: ' + 'y' * 100 + '\n---\n# Body\n')
        self.assertEqual(collect(self.root)[1], [])

    def test_multiline_and_crlf(self):
        self.skill(content='---\r\nname: sample\r\ndescription: >\r\n  Use when this happens.\r\n  More detail.\r\n---\r\n# Body\r\n')
        self.assertEqual(collect(self.root)[1], [])

    def test_metadata_must_be_string_map(self):
        self.skill(content='---\nname: sample\ndescription: valid\nmetadata:\n  version: 1\n---\n# Body\n')
        self.assertTrue(collect(self.root)[1])

    def test_duplicate_skill_names(self):
        self.skill(folder='a/sample')
        self.skill(folder='b/sample')
        self.assertIn('duplicate skill', ' '.join(collect(self.root)[1]))

    def test_missing_link(self):
        p = self.skill()
        self.assertTrue(markdown_errors(p, '[broken](missing.md)\n', self.root))

    def test_valid_relative_and_external_links(self):
        p = self.skill()
        (p.parent / 'guide.md').write_text('# Guide\n')
        self.assertEqual(markdown_errors(p, '[guide](guide.md#guide) [web](https://example.org)\n', self.root), [])

    def test_fenced_examples_not_checked(self):
        p = self.skill()
        self.assertEqual(markdown_errors(p, '```md\n[example](missing.md)\n| a | b |\n|---|\n```\n', self.root), [])

    def test_table_column_mismatch(self):
        p = self.skill()
        self.assertTrue(markdown_errors(p, '| A | B |\n|---|---|\n| one |\n', self.root))

    def test_table_separator_mismatch(self):
        p = self.skill()
        self.assertTrue(markdown_errors(p, '| A | B |\n|---|---|---|\n| one | two |\n', self.root))

    def test_escaped_pipe(self):
        p = self.skill()
        self.assertEqual(markdown_errors(p, '| A | B |\n|---|---|\n| x\\|y | two |\n', self.root), [])

    def test_catalog_is_deterministic_and_detects_drift(self):
        self.skill('zebra'); self.skill('alpha')
        records, _ = collect(self.root)
        write_catalog(self.root, records)
        self.assertEqual(check_catalog(self.root, records), [])
        path = self.root / 'skills' / 'catalog.json'
        data = json.loads(path.read_text())
        self.assertEqual([row['name'] for row in data], ['alpha', 'zebra'])
        path.write_text('[]\n')
        self.assertTrue(check_catalog(self.root, records))


if __name__ == '__main__':
    unittest.main()
