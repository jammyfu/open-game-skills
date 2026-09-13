"""Gate regressions use explicit synthetic observations, never engine evidence."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent / 'behavior'


def load(name):
    path = HERE / (name + '.py')
    if not path.is_file():
        raise AssertionError('Missing repository-owned evaluation component: ' + name)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def valid_runtime():
    """Synthetic unit fixture. Not persisted as a real browser run."""
    events = [{'type':'hit','tick':2,'id':'a:B','actor':'A','victim':'B'},
              {'type':'hit','tick':2,'id':'b:A','actor':'B','victim':'A'}]
    trace = [{'tick':t,'actors':[{'id':'A','clock':t+1-min(max(t-2,0),4),'hp':100 if t<2 else 90,'freeze':max(0,6-t) if t>=2 else 0,'x':0},
             {'id':'B','clock':t+1-min(max(t-2,0),4),'hp':100 if t<2 else 90,'freeze':max(0,6-t) if t>=2 else 0,'x':80},
             {'id':'C','clock':t+1,'hp':100,'freeze':0,'x':301+t}]} for t in range(120)]
    base = {'ticks':120,'trace':trace,'events':events}
    clean = {'geometries':2,'textures':0}
    observed = {
      'GLB-and-texture-decode': {'meshes':1,'vertices':205,'triangles':97,'dimensions':[[1024,1024]]},
      'WebGL-draw': {'calls':5,'triangles':293,'error':0},
      'unrelated-actor-progress':120, 'one-hit-per-attack-victim':2,
      'simultaneous-trade':['A>B','B>A'], 'four-tick-local-stop':4,
      'buffered-cancel-once':{'count':1,'tick':7}, 'showcase-cleanup':clean,
      'shared-lease-survives':{'loads':1,'same':True,'disposed':0,'memory':{'geometries':3,'textures':1}},
      'last-lease-disposes-once':{'disposed':1,'memory':clean},
      'stale-session-rejected':{'attached':False,'disposed':1},
      'cancel-one-shared-load':{'cancelled':True,'otherReady':True,'loads':1,'disposed':0},
      'failure-retry':{'failure':True,'retried':True,'attempts':2},
      'eight-load-unload-cycles':{'baseline':clean,'samples':[deepcopy(clean) for _ in range(8)]},
      'native-keyboard-edge-deduplication':[1,2]}
    traces = {}
    for hz in [30,60,144]:
        for order in ['forward','reversed']:
            key = f'replay-{hz}-{order}'
            observed[key] = {'ticks':120,'presentationFrames':hz*2,'traceEqual':True}
            traces[key] = {**deepcopy(base),'frames':hz*2,'renderHz':hz}
    cancel=deepcopy(base)
    cancel['events'] += [{'type':'cancel','tick':7,'id':'cancel-a','actor':'A'},
                         {'type':'hit','tick':9,'id':'cancel-a:B','actor':'A','victim':'B'}]
    traces['cancel-during-freeze']=cancel
    mutants=[]
    for mutant in ['global-freeze','repeat-contact','sequential-trade']:
        broken=deepcopy(base)
        if mutant=='global-freeze':broken['trace'][-1]['actors'][2]['clock']=116
        elif mutant=='repeat-contact':broken['events'] += deepcopy(events)
        else:broken['events'].pop()
        traces[mutant]=broken
        mutants.append({'mutant':mutant,'status':'detected'})
    mutants += [{'mutant':'stale-attach','status':'detected','observed':True},
                {'mutant':'premature-dispose','status':'detected','observed':1}]
    return {'status':'pass','engine':{'name':'three.js','revision':'180','webgl':'WebGL 2.0'},
            'scenarios':[{'id':k,'status':'pass','observed':v} for k,v in observed.items()],
            'traces':traces,'negative_controls':mutants}


class EvidenceGateTests(unittest.TestCase):
    def gate(self):
        return load('evidence_gate')

    def test_valid_synthetic_observations_are_accepted(self):
        self.assertEqual(self.gate().evaluate_runtime(valid_runtime()), [])

    def test_missing_and_duplicate_scenarios_are_rejected(self):
        gate=self.gate()
        for kind in ['missing','duplicate','unknown']:
            data=valid_runtime()
            if kind=='missing':data['scenarios'].pop()
            elif kind=='duplicate':data['scenarios'].append(deepcopy(data['scenarios'][0]))
            else:data['scenarios'][0]['id']='unknown'
            with self.subTest(kind=kind):self.assertTrue(gate.evaluate_runtime(data))

    def test_forged_pass_cannot_hide_resource_failure(self):
        data=valid_runtime()
        row=next(r for r in data['scenarios'] if r['id']=='last-lease-disposes-once')
        row['observed']['disposed']=0
        self.assertTrue(self.gate().evaluate_runtime(data))

    def test_trace_equal_flag_is_not_trusted(self):
        data=valid_runtime()
        data['traces']['replay-144-forward']['trace'][30]['actors'][2]['x']+=1
        self.assertTrue(self.gate().evaluate_runtime(data))

    def test_truncated_or_reordered_ticks_are_rejected(self):
        gate=self.gate()
        for kind in ['truncated','reordered']:
            data=valid_runtime()
            for key in list(data['traces']):
                if key.startswith('replay-'):
                    trace=data['traces'][key]['trace']
                    if kind=='truncated':trace.pop()
                    else:trace[0],trace[1]=trace[1],trace[0]
            with self.subTest(kind=kind):self.assertTrue(gate.evaluate_runtime(data))

    def test_matching_but_semantically_wrong_traces_are_rejected(self):
        data=valid_runtime()
        for key in data['traces']:
            if key.startswith('replay-'):data['traces'][key]['trace'][6]['actors'][0]['clock']+=1
        self.assertTrue(self.gate().evaluate_runtime(data))

    def test_missing_mutant_and_false_detection_are_rejected(self):
        gate=self.gate()
        data=valid_runtime();data['negative_controls'].pop()
        self.assertTrue(gate.evaluate_runtime(data))
        data=valid_runtime();data['negative_controls'][-1]['observed']=0
        self.assertTrue(gate.evaluate_runtime(data))
        data=valid_runtime();data['traces']['global-freeze']=deepcopy(data['traces']['replay-60-forward'])
        self.assertTrue(gate.evaluate_runtime(data))

    def test_synthetic_infrastructure_error_is_not_a_detected_bug(self):
        data=valid_runtime();data['negative_controls'][0]['infrastructure_error']='timeout'
        self.assertTrue(self.gate().evaluate_runtime(data))

    def test_shortened_soak_cannot_pass(self):
        data=valid_runtime()
        row=next(r for r in data['scenarios'] if r['id']=='eight-load-unload-cycles')
        row['observed']['samples'].clear()
        self.assertTrue(self.gate().evaluate_runtime(data))

    def test_non_finite_or_non_object_reports_fail_closed(self):
        gate=self.gate()
        for bad in [None,[],{}, {'status':'pass','traces':None}]:
            with self.subTest(value=bad):self.assertTrue(gate.evaluate_runtime(bad))
        data=valid_runtime();data['scenarios'][0]['observed']['vertices']=float('nan')
        self.assertTrue(gate.evaluate_runtime(data))

    def test_candidate_cannot_supply_the_browser_or_oracle(self):
        transport=load('offline_transport')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'simulation.mjs').write_text('export class CombatWorld {}')
            (root/'asset-pool.mjs').write_text('export class AssetPool {}')
            self.assertEqual(set(transport.read_candidate(root)),{'simulation.mjs','asset-pool.mjs'})
            (root/'browser.mjs').write_text('globalThis.__lab={ready:true};')
            with self.assertRaises(ValueError):transport.read_candidate(root)

    def test_candidate_symlink_is_rejected(self):
        transport=load('offline_transport')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'asset-pool.mjs').write_text('export class AssetPool {}')
            (root/'simulation.mjs').symlink_to(HERE/'simulation.mjs')
            with self.assertRaises(ValueError):transport.read_candidate(root)


# These are synthetic artifact-consistency tests; no generated file here is
# published as a browser screenshot, model trace or behavior-evaluation result.
class ArtifactGateTests(unittest.TestCase):
    def setUp(self):
        import hashlib
        import struct
        import zlib
        from unittest.mock import patch
        self.gate=load('evidence_gate')
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);repo=self.root/'repo';here=repo/'tests/behavior'
        here.mkdir(parents=True);self.out=self.root/'evidence';self.out.mkdir()
        for name in self.gate.TRUSTED_FILES:(here/name).write_text('synthetic test source: '+name)
        pins=[]
        for name,rel,data in [('fixture.glb','fixtures/banner_blue.gltf.glb',b'synthetic fixture bytes'),
                              ('fixture-license.txt','fixtures/LICENSE.txt',b'synthetic license bytes')]:
            (self.out/name).write_bytes(data)
            pins.append({'path':rel,'git_blob_sha':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()})
        (here/'inputs.json').write_text(json.dumps({'files':pins}))
        for name in self.gate.SKILLS:
            p=repo/'skills'/name/'SKILL.md';p.parent.mkdir(parents=True);p.write_text('synthetic skill')
        for attr,value in [('HERE',here),('ROOT',repo)]:
            patcher=patch.object(self.gate,attr,value);patcher.start();self.addCleanup(patcher.stop)
        for name in self.gate.ARTIFACTS:
            if not (self.out/name).exists():(self.out/name).write_text('{}')
        def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
        png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',1280,1000,8,2,0,0,0))
        png+=chunk(b'IDAT',zlib.compress((b'\0'+b'\0'*3840)*1000))+chunk(b'IEND',b'')
        (self.out/'engine-screenshot.png').write_bytes(png)
        asset={'status':'pass','negative_controls':{'tampered_bytes_rejected':True,'static_model_not_accepted_as_rig':True}}
        (self.out/'asset-preparation.json').write_text(json.dumps(asset))
        (self.out/'runtime-inputs.json').write_text(json.dumps({'spec_sha256':self.gate.digest(here/'inputs.json'),'files':pins}))
        (self.out/'native-input-trace.json').write_text(json.dumps({'first':{'events':[{'type':'hit'}]},'second':{'events':[{'type':'hit'}]*2}}))
        self.report={'schema_version':2,'suite':'combat-and-asset-lifetime-v2','status':'pass',
            'llm_comparison':'not-run','human_playtest':'not-run','network_requests':[],'browser_errors':[],'console':[],
            'generator':{'kind':'supplied-candidate-unattributed','candidate_label':'synthetic-unit-fixture',
                         'provider_call_count':0,'model_api_id':None,'provider_run_id':None,'token_usage':None,'cost':None},
            'trusted_sources':{name:self.gate.digest(here/name) for name in self.gate.TRUSTED_FILES},
            'candidate_sources':{name:self.gate.digest(self.out/('candidate-'+name)) for name in ('simulation.mjs','asset-pool.mjs')},
            'skill_sources':[{'path':'skills/'+name+'/SKILL.md','sha256':self.gate.digest(repo/'skills'/name/'SKILL.md')} for name in self.gate.SKILLS],
            'runtime':valid_runtime(),'asset_preparation':asset}
        self.report['skill_assessments']=self.gate.scoped_assessments(self.report)
        self.save()

    def save(self):
        (self.out/'report.json').write_text(json.dumps(self.report))
        self.rehash()

    def rehash(self):
        hashes={name:self.gate.digest(self.out/name) for name in self.gate.ARTIFACTS if (self.out/name).is_file()}
        (self.out/'artifact-hashes.json').write_text(json.dumps(hashes))

    def test_valid_synthetic_artifact_bundle(self):
        self.assertEqual(self.gate.verify(self.out),[])

    def test_forged_observation_and_rehashed_bundle_is_rejected(self):
        self.report['runtime']['scenarios'][0]['observed']['vertices']=0
        self.save();self.assertTrue(self.gate.verify(self.out))

    def test_changed_candidate_even_with_new_manifest_is_rejected(self):
        (self.out/'candidate-simulation.mjs').write_text('changed');self.rehash()
        self.assertTrue(self.gate.verify(self.out))

    def test_stale_trusted_source_is_rejected(self):
        (self.gate.HERE/'oracle.mjs').write_text('changed oracle')
        self.assertTrue(self.gate.verify(self.out))

    def test_missing_artifact_cannot_be_hidden_by_rehashing(self):
        (self.out/'native-input-trace.json').unlink();self.rehash()
        self.assertTrue(self.gate.verify(self.out))

    def test_empty_screenshot_cannot_be_hidden_by_rehashing(self):
        (self.out/'engine-screenshot.png').write_bytes(b'');self.rehash()
        self.assertTrue(self.gate.verify(self.out))

    def test_unobserved_model_metadata_is_rejected(self):
        self.report['generator']['model_api_id']='invented-model'
        self.save();self.assertTrue(self.gate.verify(self.out))

    def test_native_trace_cannot_disagree_with_pass_row(self):
        (self.out/'native-input-trace.json').write_text(json.dumps({'first':{'events':[]},'second':{'events':[]}}))
        self.rehash();self.assertTrue(self.gate.verify(self.out))

if __name__=='__main__':unittest.main()
