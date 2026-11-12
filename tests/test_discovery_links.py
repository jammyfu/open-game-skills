"""Keep agent discovery grounded in repository files, not invented skill paths."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

class DiscoveryLinks(unittest.TestCase):
    def test_every_local_index_target_exists(self):
        content = (ROOT / "llms.txt").read_text()
        targets = re.findall(r"\]\(([^)]+)\)", content)
        self.assertGreater(len(targets), 20)
        for target in targets:
            with self.subTest(target=target):
                self.assertNotIn("://", target)
                self.assertTrue((ROOT / target.split("#")[0]).is_file())

    def test_all_reader_languages_are_discoverable(self):
        content = (ROOT / "llms.txt").read_text()
        for filename in ["README.md", "README.zh.md", "README.zh-Hant.md", "README.ja.md", "README.ko.md"]:
            self.assertIn(f"({filename})", content)
