"""Synthetic fixtures exercise validation, not an actual model evaluation."""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / 'tools/engineering_quality.py'


class EngineeringQualityTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(TOOL.is_file(), 'engineering validator is not implemented')
        spec = importlib.util.spec_from_file_location('engineering_quality_test', TOOL)
        self.tool = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.tool)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.pack = self.root / 'skills'
        self.folder = self.pack / 'disciplines/example'
        (self.folder / 'assets').mkdir(parents=True)
        (self.folder / 'SKILL.md').write_text('---\nname: example\ndescription: Use when testing.\n---\n# Example\n\n## Modes\n\n| Mode | Contract |\n|---|---|\n| alpha | one |\n| beta | two |\n\n## Procedure\n\nMention gamma in prose, not as a mode.\n', encoding='utf-8')
        self.registry = {'schema_version': 1, 'scope': 'engineering-core-v1', 'entries': {'example': {'owner': 'example', 'modes': ['alpha', 'beta'], 'optional_dependencies': []}}}
        self.write('engineering-registry.json', self.registry)
        self.cases = [{'id': 'example-' + k, 'skill': 'example', 'kind': k, 'prompt': 'Test a meaningful condition.', 'criteria': {'c1': 'Maintain ownership.', 'c2': 'Record evidence.'}} for k in ('normal', 'boundary', 'adversarial')]
        self.write('disciplines/example/assets/evals.json', self.cases)
        self.write('disciplines/example/assets/contract.example.json', {'schema_version': 1, 'skill': 'example', 'status': 'not-run', 'mode': 'alpha'})

    def write(self, path, data):
        (self.pack / path).write_text(json.dumps(data), encoding='utf-8')

    def suite(self):
        return self.tool.load_suite(self.root)

    def record(self, case_id='example-normal', status='pass'):
        suite = self.suite()
        response = self.root / 'response.txt'
        response.write_text('SYNTHETIC TEST FIXTURE, not a model invocation. Ownership is maintained.', encoding='utf-8')
        row = {'case_id': case_id, 'status': status, 'response': {'path': response.name, 'sha256': hashlib.sha256(response.read_bytes()).hexdigest()}, 'judgment': {'reviewer': 'synthetic-fixture', 'method': 'human-review', 'criteria': {k: {'status': 'pass', 'reason': 'Synthetic fixture assertion at line 1.'} for k in ('c1', 'c2')}}}
        return {'schema_version': 1, 'suite_sha256': suite['sha256'], 'subject': {'commit': 'a' * 40, 'model': 'synthetic-fixture', 'driver': 'fixture', 'configuration': 'unit test only', 'evaluated_at': '2026-09-13T00:00:00+00:00'}, 'results': [row]}

    def test_loads_suite_and_template_has_only_not_run(self):
        suite = self.suite()
        template = self.tool.result_template(suite)
        counts = self.tool.validate_results(template, suite, self.root)
        self.assertEqual(counts, {'pass': 0, 'fail': 0, 'blocked': 0, 'not-run': 3})

    def test_repository_registry_and_cases_validate(self):
        suite = self.tool.load_suite(ROOT)
        self.assertEqual(len(suite['entries']), 6)
        self.assertEqual(len(suite['cases']), 18)

    def test_declared_mode_cannot_be_just_a_prose_mention(self):
        self.registry['entries']['example']['modes'].append('gamma')
        self.write('engineering-registry.json', self.registry)
        with self.assertRaises(ValueError): self.suite()

    def test_unknown_or_duplicate_dependencies_and_owner_are_rejected(self):
        for patch in ({'owner': 'ghost'}, {'optional_dependencies': ['ghost']}, {'optional_dependencies': ['example']}, {'modes': ['alpha', 'alpha']}):
            with self.subTest(patch=patch):
                data = deepcopy(self.registry)
                data['entries']['example'].update(patch)
                self.write('engineering-registry.json', data)
                with self.assertRaises(ValueError): self.suite()

    def test_source_directory_name_is_not_a_valid_dependency(self):
        (self.pack / 'SKILL.md').write_text('---\nname: open-game-skills\n---\n# Entry\n')
        self.registry['entries']['example']['optional_dependencies'] = ['skills']
        self.write('engineering-registry.json', self.registry)
        with self.assertRaises(ValueError): self.suite()

    def test_example_mode_and_not_run_are_checked(self):
        for patch in ({'mode': 'gamma'}, {'status': 'pass'}):
            with self.subTest(patch=patch):
                data = {'schema_version': 1, 'skill': 'example', 'mode': 'alpha', 'status': 'not-run', **patch}
                self.write('disciplines/example/assets/contract.example.json', data)
                with self.assertRaises(ValueError): self.suite()

    def test_duplicate_case_missing_class_or_empty_criteria_rejected(self):
        for cases in ([self.cases[0]] * 3, self.cases[:2], [{**self.cases[0], 'criteria': {}}] + self.cases[1:]):
            with self.subTest(cases=cases):
                self.write('disciplines/example/assets/evals.json', cases)
                with self.assertRaises(ValueError): self.suite()

    def test_duplicate_json_keys_are_not_silently_accepted(self):
        path = self.pack / 'engineering-registry.json'
        path.write_text('{"schema_version":1,"schema_version":2}')
        with self.assertRaises(ValueError): self.suite()

    def test_malformed_registry_shapes_are_errors(self):
        for data in ([], None, {'schema_version': True, 'scope': 'engineering-core-v1', 'entries': {}}, {**self.registry, 'entries': []}):
            with self.subTest(data=data):
                self.write('engineering-registry.json', data)
                with self.assertRaises(ValueError): self.suite()

    def test_partial_results_keep_missing_cases_in_denominator(self):
        counts = self.tool.validate_results(self.record(), self.suite(), self.root)
        self.assertEqual(counts, {'pass': 1, 'fail': 0, 'blocked': 0, 'not-run': 2})

    def test_missing_evidence_or_tampered_hash_rejected(self):
        for mode in ('absent', 'hash', 'empty'):
            data = self.record()
            response = self.root / 'response.txt'
            if mode == 'absent': response.unlink()
            if mode == 'hash': data['results'][0]['response']['sha256'] = '0' * 64
            if mode == 'empty': response.write_text('')
            with self.subTest(mode=mode):
                with self.assertRaises(ValueError): self.tool.validate_results(data, self.suite(), self.root)

    def test_absolute_and_escape_evidence_paths_rejected(self):
        for path in ('../outside.txt', '/etc/passwd', 'https://example.org/response.txt', 'C:\\response.txt'):
            data = self.record()
            data['results'][0]['response']['path'] = path
            with self.subTest(path=path):
                with self.assertRaises(ValueError): self.tool.validate_results(data, self.suite(), self.root)

    def test_symlink_to_external_evidence_rejected(self):
        data = self.record()
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp) / 'outside.txt'
            outside.write_text('outside')
            (self.root / 'link.txt').symlink_to(outside)
            data['results'][0]['response']['path'] = 'link.txt'
            with self.assertRaises(ValueError): self.tool.validate_results(data, self.suite(), self.root)

    def test_pass_requires_all_criteria_and_nonempty_reasons(self):
        for mutation in ('missing', 'fail', 'no-reason'):
            data = self.record()
            criteria = data['results'][0]['judgment']['criteria']
            if mutation == 'missing': del criteria['c2']
            if mutation == 'fail': criteria['c2']['status'] = 'fail'
            if mutation == 'no-reason': criteria['c2']['reason'] = ''
            with self.subTest(mutation=mutation):
                with self.assertRaises(ValueError): self.tool.validate_results(data, self.suite(), self.root)

    def test_fail_requires_a_failing_criterion(self):
        data = self.record(status='fail')
        with self.assertRaises(ValueError): self.tool.validate_results(data, self.suite(), self.root)
        data['results'][0]['judgment']['criteria']['c1']['status'] = 'fail'
        self.assertEqual(self.tool.validate_results(data, self.suite(), self.root)['fail'], 1)

    def test_blocked_and_not_run_need_reason_and_cannot_contain_a_judgment(self):
        template = self.tool.result_template(self.suite())
        template['results'][0] = {'case_id': template['results'][0]['case_id'], 'status': 'blocked', 'reason': 'No configured model runner.'}
        self.assertEqual(self.tool.validate_results(template, self.suite(), self.root)['blocked'], 1)
        template['results'][0]['judgment'] = {}
        with self.assertRaises(ValueError): self.tool.validate_results(template, self.suite(), self.root)

    def test_duplicate_unknown_and_invalid_result_rows_rejected(self):
        for mode in ('duplicate', 'unknown', 'shape', 'status'):
            data = self.record()
            if mode == 'duplicate': data['results'].append(deepcopy(data['results'][0]))
            if mode == 'unknown': data['results'][0]['case_id'] = 'unknown'
            if mode == 'shape': data['results'] = 'not-a-list'
            if mode == 'status': data['results'][0]['status'] = 'maybe'
            with self.subTest(mode=mode):
                with self.assertRaises(ValueError): self.tool.validate_results(data, self.suite(), self.root)

    def test_run_metadata_and_timezone_required_for_executed_results(self):
        for key, value in (('model', ''), ('commit', 'main'), ('evaluated_at', '2026-09-13T00:00:00'), ('configuration', None)):
            data = self.record()
            data['subject'][key] = value
            with self.subTest(key=key):
                with self.assertRaises(ValueError): self.tool.validate_results(data, self.suite(), self.root)

    def test_changed_skill_or_case_invalidates_results(self):
        data = self.record()
        path = self.folder / 'SKILL.md'
        path.write_text(path.read_text() + '\nChanged contract.\n')
        with self.assertRaises(ValueError): self.tool.validate_results(data, self.suite(), self.root)

    def test_cli_unrun_gate_fails_and_template_never_overwrites(self):
        cmd = [sys.executable, str(TOOL), '--root', str(self.root)]
        run = subprocess.run(cmd + ['--require-passed'], capture_output=True, text=True)
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn('"not-run": 3', run.stdout)
        target = self.root / 'results.json'
        first = subprocess.run(cmd + ['--write-template', str(target)], capture_output=True, text=True)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        before = target.read_bytes()
        second = subprocess.run(cmd + ['--write-template', str(target)], capture_output=True, text=True)
        self.assertEqual(second.returncode, 2)
        self.assertEqual(target.read_bytes(), before)

    def test_complete_synthetic_record_passes_consistency_gate(self):
        data = self.record()
        data['results'] = [dict(deepcopy(data['results'][0]), case_id=c['id']) for c in self.cases]
        path = self.root / 'results.json'
        path.write_text(json.dumps(data))
        run = subprocess.run([sys.executable, str(TOOL), '--root', str(self.root), '--results', str(path), '--require-passed'], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertIn('not authenticity', run.stdout)


if __name__ == '__main__':
    unittest.main()
