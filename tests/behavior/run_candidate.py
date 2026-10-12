"""Run two supplied implementation modules with fixed oracles in offline WebGL.

No LLM provider is invoked here. Use only reviewed/trusted generated candidates:
separate module ownership is not an adversarial-code security sandbox.
"""
from __future__ import annotations
import argparse
import base64
from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path
import shutil
import time
import traceback
from urllib.parse import urlsplit

from acquire_inputs import verify as verify_inputs
from evidence_gate import (TRUSTED_FILES, SKILLS, digest, evaluate_runtime,
                           scoped_assessments, verify as verify_evidence)
from offline_transport import HERE, INSTALL_MODULES, build_modules, offline_html, read_candidate
from run_browser import prepare_fixture

ROOT = HERE.parents[1]


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def run(args) -> int:
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    report = {'schema_version': 2, 'suite': 'combat-and-asset-lifetime-v2', 'status': 'not-run',
        'build_ref': args.build_ref, 'started_at': datetime.now(timezone.utc).isoformat(),
        'llm_comparison': 'not-run', 'human_playtest': 'not-run', 'cross_engine': 'not-run',
        'generator': {'kind': 'supplied-candidate-unattributed' if args.candidate_dir else 'repository-reference-specimen',
                      'candidate_label': args.candidate_label, 'provider_call_count': 0,
                      'model_api_id': None, 'provider_run_id': None, 'token_usage': None, 'cost': None},
        'driver': {'mode': 'replay-input + scripted-scene', 'project_tick_hz': 60,
                   'schedules': [30, 60, 144], 'oracles': 'repository-owned',
                   'negative_controls': 'repository-reference; not candidate-owned'},
        'transport': {'mode': 'offline-blob-modules',
                      'changes': ['module import specifiers', 'GLB bytes via GLTFLoader.parseAsync'],
                      'browser_network_policy_changed': False},
        'scope': 'Supplied example execution only. No independent LLM generation, A/B, human, or hardware-performance claim.',
        'trusted_sources': {}, 'candidate_sources': {}, 'skill_sources': [], 'skill_assessments': []}
    save(out / 'report.json', report)
    execution_started = False
    code = 2
    try:
        report['trusted_sources'] = {name: digest(HERE / name) for name in TRUSTED_FILES}
        report['skill_sources'] = [{'path': 'skills/' + name + '/SKILL.md',
                                   'sha256': digest(ROOT / 'skills' / name / 'SKILL.md')} for name in SKILLS]
        runtime = args.runtime.resolve()
        acquisition = verify_inputs(runtime)
        save(out / 'runtime-inputs.json', acquisition)
        candidate_dir = args.candidate_dir or HERE
        candidate = read_candidate(candidate_dir)
        for name in candidate:
            # Capture the exact UTF-8 bytes loaded by the browser, including newline normalization.
            path = out / ('candidate-' + name)
            path.write_text(candidate[name], encoding='utf-8')
            report['candidate_sources'][name] = digest(path)
        report['asset_preparation'] = prepare_fixture(runtime, out)
        shutil.copyfile(runtime / 'fixtures/banner_blue.gltf.glb', out / 'fixture.glb')
        shutil.copyfile(runtime / 'fixtures/LICENSE.txt', out / 'fixture-license.txt')
        save(out / 'generation-request.json', {
            'kind': 'execution-request-not-provider-transcript', 'candidate_label': args.candidate_label,
            'candidate_sources': report['candidate_sources'],
            'interface': ['CombatWorld: tick, actor(id), events, step(inputs)', 'AssetPool: acquire(key,isCurrent), stats'],
            'excluded_candidate_exports': ['replay', 'normalChecks'], 'provider_call_count': 0})
        modules = build_modules(runtime, candidate)
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            options = {'headless': True, 'args': ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader',
                       '--enable-unsafe-swiftshader', '--disable-dev-shm-usage']}
            if args.browser: options['executable_path'] = args.browser
            browser = pw.chromium.launch(**options)
            try:
                context = browser.new_context(viewport={'width': 1280, 'height': 1000},
                                               device_scale_factor=1, service_workers='block')
                errors, console, network = [], [], []
                def no_network(route):
                    if urlsplit(route.request.url).scheme in {'data', 'blob'}:
                        route.continue_()
                    else:
                        network.append(route.request.url)
                        route.abort()
                context.route('**/*', no_network)
                page = context.new_page()
                page.on('pageerror', lambda error: errors.append(str(error)))
                page.on('console', lambda msg: console.append({'type': msg.type, 'text': msg.text}))
                page.set_content(offline_html())
                report['browser_version'] = browser.version
                report['playwright_version'] = importlib.metadata.version('playwright')
                execution_started = True
                page.evaluate(INSTALL_MODULES, {'modules': modules,
                    'fixture': base64.b64encode((out / 'fixture.glb').read_bytes()).decode()})
                page.wait_for_function('window.__lab && window.__lab.ready', timeout=90000)
                result = page.evaluate('window.__lab.result')
                # Candidate load/execution errors are failures, not setup skips.
                if result.get('status') == 'blocked':
                    raise RuntimeError('candidate or harness execution failed: ' + result.get('error', 'unknown'))
                page.evaluate('window.__lab.armInput()')
                page.keyboard.down('Space'); page.keyboard.down('Space')
                first = page.evaluate('window.__lab.stepInput(13)')
                page.keyboard.up('Space'); page.keyboard.press('Space')
                second = page.evaluate('window.__lab.stepInput(3)')
                hits = [len([event for event in state['events'] if event['type'] == 'hit']) for state in (first, second)]
                result['scenarios'].append({'id': 'native-keyboard-edge-deduplication',
                    'status': 'pass' if hits == [1, 2] else 'fail', 'expected': [1, 2], 'observed': hits,
                    'driver': 'Playwright browser keyboard events, not a human player'})
                save(out / 'native-input-trace.json', {'first': first, 'second': second})
                report.update(runtime=result, browser_errors=errors, console=console, network_requests=network)
                failures = evaluate_runtime(result)
                if errors or network or any(msg['type'] == 'error' for msg in console):
                    failures.append('browser/network diagnostics failed')
                if report['asset_preparation']['status'] != 'pass': failures.append('asset preparation failed')
                report['oracle_errors'] = failures
                report['status'] = 'fail' if failures else 'pass'
                code = 1 if failures else 0
                # Screenshot labels reflect the Python-owned verdict and native check,
                # not only the browser's preliminary pass flags.
                page.evaluate('''({status, count, controls, native}) => {
                    document.querySelector('#badge').textContent = `${count} CHECKS / ${controls} CONTROLS / GATE ${status.toUpperCase()}`;
                    const row = document.createElement('div'); row.className = 'row';
                    const label = document.createElement('span'); label.textContent = native.id;
                    const value = document.createElement('b'); value.className = native.status;
                    value.textContent = native.status.toUpperCase(); row.append(label, value);
                    document.querySelector('#checks').append(row);
                }''', {'status': report['status'], 'count': len(result['scenarios']),
                       'controls': len(result['negative_controls']), 'native': result['scenarios'][-1]})
                page.screenshot(path=str(out / 'engine-screenshot.png'), full_page=True)
                context.close()
            finally:
                browser.close()
    except Exception as exc:
        report.update(status='fail' if execution_started else 'blocked', reason=str(exc),
                      attribution='candidate-or-harness' if execution_started else 'setup',
                      traceback=traceback.format_exc())
        code = 1 if execution_started else 2
    report['elapsed_seconds'] = round(time.monotonic() - started, 3)
    report['completed_at'] = datetime.now(timezone.utc).isoformat()
    report['skill_assessments'] = scoped_assessments(report)
    save(out / 'report.json', report)
    save(out / 'artifact-hashes.json', {path.name: digest(path) for path in sorted(out.iterdir()) if path.is_file()})
    if code == 0:
        gate_errors = verify_evidence(out)
        if gate_errors:
            # Do not leave a pass record when evidence consistency fails.
            report.update(status='fail', oracle_errors=gate_errors, skill_assessments=[])
            save(out / 'report.json', report)
            save(out / 'artifact-hashes.json', {path.name: digest(path) for path in sorted(out.iterdir())
                                              if path.is_file() and path.name != 'artifact-hashes.json'})
            code = 1
    print(json.dumps({'status': report['status'], 'checks': len(report.get('runtime', {}).get('scenarios', [])),
        'controls': len(report.get('runtime', {}).get('negative_controls', [])), 'report': str(out / 'report.json'),
        'reason': report.get('reason'), 'oracle_errors': report.get('oracle_errors', [])}, indent=2))
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--browser')
    parser.add_argument('--candidate-dir', type=Path)
    parser.add_argument('--candidate-label', default='unattributed')
    parser.add_argument('--build-ref', default='local-uncommitted-see-source-hashes')
    args = parser.parse_args()
    try: return run(args)
    except FileExistsError:
        parser.exit(2, 'Output already exists; previous evidence was left unchanged.\n')


if __name__ == '__main__': raise SystemExit(main())
