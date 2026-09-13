"""Synthetic orchestration tests, never independent model-evaluation evidence."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent / 'behavior'

def module():
    path = HERE / 'ab_experiment.py'
    if not path.is_file():
        raise AssertionError('Missing independent A/B experiment runner')
    spec = importlib.util.spec_from_file_location('ab_experiment_under_test', path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

class ABExperimentTests(unittest.TestCase):
    def test_snapshot_and_budget_are_bounded(self):
        m=module();p=m.load_plan()
        self.assertEqual(p['pairs'],6)
        self.assertEqual(p['model'],'gpt-4.1-mini-2025-04-14')
        self.assertLessEqual(m.reserve_cost(p),p['estimated_budget_usd'])
        self.assertEqual(p['max_output_tokens'],4096)

    def test_only_treatment_gets_exact_skill_text(self):
        m=module();p=m.load_plan();a=m.payload(p,'without-skill');b=m.payload(p,'with-skill')
        skill=(m.ROOT/p['skill_path']).read_text()
        self.assertNotIn(skill,a['input'])
        self.assertEqual(b['input'],a['input']+m.SKILL_SEPARATOR+skill)
        for key in a:
            if key!='input':self.assertEqual(a[key],b[key])
        self.assertNotIn('previous_response_id',a)
        self.assertNotIn('conversation',a)
        self.assertFalse(a['store']);self.assertEqual(a['tools'],[])
        self.assertNotIn('class AssetPool',a['input'])
        self.assertNotIn('cancel-a:B',a['input'])

    def test_balanced_pairs_and_blinded_sample_ids(self):
        m=module();rows=m.allocate(m.load_plan())
        self.assertEqual(len(rows),12)
        self.assertEqual(len({r['id'] for r in rows}),12)
        for pair in range(6):
            self.assertEqual({r['arm'] for r in rows if r['pair']==pair},{'with-skill','without-skill'})
        self.assertEqual({rows[i]['arm'] for i in range(0,12,2)},{'with-skill','without-skill'})
        self.assertTrue(all('skill' not in r['id'] for r in rows))

    def test_missing_key_retains_all_slots_and_makes_no_requests(self):
        m=module()
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ,{},clear=True), patch.object(m,'call_provider') as call:
            out=Path(temp)/'run'
            result=m.generate(m.load_plan(),out,execute=True)
            self.assertEqual(result['status'],'blocked');self.assertEqual(result['provider_calls'],0)
            self.assertEqual(len(result['samples']),12)
            self.assertTrue(all(r['status']=='not-run' for r in result['samples']))
            self.assertEqual(result['reason'],'OPENAI_API_KEY is not configured')
            call.assert_not_called()
            self.assertTrue((out/'blinded.json').is_file())

    def test_plan_only_never_calls_provider_even_with_key(self):
        m=module()
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ,{'OPENAI_API_KEY':'synthetic-not-a-real-key'}), patch.object(m,'call_provider') as call:
            result=m.generate(m.load_plan(),Path(temp)/'run',execute=False)
            self.assertEqual(result['status'],'planned');call.assert_not_called()

    def test_existing_evidence_is_not_overwritten(self):
        m=module()
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/'existing';out.mkdir();(out/'keep').write_text('original')
            with self.assertRaises(FileExistsError):m.generate(m.load_plan(),out,execute=False)
            self.assertEqual((out/'keep').read_text(),'original')

    def test_provider_metadata_and_exact_decoded_code(self):
        m=module();p=m.load_plan();code='export class AssetPool { /* synthetic */ }\n'
        response={'id':'resp_synthetic','model':p['model'],'status':'completed',
          'usage':{'input_tokens':100,'output_tokens':25,'total_tokens':125},
          'output':[{'type':'message','role':'assistant','content':[{'type':'output_text','text':json.dumps({'asset_pool_mjs':code})}]}]}
        self.assertEqual(m.extract_candidate(response,p),code)
        response['model']='different-model'
        with self.assertRaises(ValueError):m.extract_candidate(response,p)

    def test_refusal_truncation_and_invented_metadata_not_passed(self):
        m=module();p=m.load_plan()
        for response in [{},{'id':'x','status':'incomplete','model':p['model']},
                         {'id':'resp_x','status':'completed','model':p['model'],'output':[],'usage':{}}]:
            with self.subTest(response=response), self.assertRaises(ValueError):m.extract_candidate(response,p)

    def test_extra_output_file_cannot_be_smuggled(self):
        m=module();p=m.load_plan()
        r={'id':'resp_synthetic','model':p['model'],'status':'completed','usage':{'input_tokens':1,'output_tokens':1,'total_tokens':2},
          'output':[{'type':'message','content':[{'type':'output_text','text':json.dumps({'asset_pool_mjs':'export {};','oracle.mjs':'bad'})}]}]}
        with self.assertRaises(ValueError):m.extract_candidate(r,p)

    def test_only_twelve_calls_no_regeneration_on_bad_output(self):
        m=module();p=m.load_plan()
        invalid={'id':'resp_synthetic','model':p['model'],'status':'incomplete','usage':{'input_tokens':1,'output_tokens':1,'total_tokens':2},'output':[]}
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ,{'OPENAI_API_KEY':'synthetic-not-a-real-key'}), patch.object(m,'call_provider',return_value=(invalid,{'request_id':'req_synthetic'})) as call:
            result=m.generate(p,Path(temp)/'run',execute=True)
            self.assertEqual(call.call_count,12)
            self.assertEqual(result['provider_calls'],12)
            self.assertTrue(all(r['status']=='generation-failed' for r in result['samples']))
            self.assertNotEqual(result['status'],'pass')

    def test_network_failure_stops_more_billable_attempts(self):
        m=module()
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ,{'OPENAI_API_KEY':'synthetic-not-a-real-key'}), patch.object(m,'call_provider',side_effect=OSError('synthetic transport error')) as call:
            result=m.generate(m.load_plan(),Path(temp)/'run',execute=True)
            self.assertEqual(call.call_count,1);self.assertEqual(result['status'],'blocked')
            self.assertEqual(result['samples'][0]['status'],'provider-error')
            self.assertTrue(all(r['status']=='not-run' for r in result['samples'][1:]))

    def test_zero_completed_samples_is_not_zero_percent_success(self):
        m=module();rows=m.allocate(m.load_plan())
        for r in rows:r['outcome']='not-run'
        result=m.analyse(rows)
        self.assertIsNone(result['paired_difference'])
        self.assertIsNone(result['exact_mcnemar_p'])
        self.assertEqual(result['complete_pairs'],0)
        self.assertIsNone(result['arms']['with-skill']['success_rate'])

    def test_analysis_paired_denominator_and_exact_test(self):
        m=module();rows=m.allocate(m.load_plan())
        for r in rows:r['outcome']='pass' if r['arm']=='with-skill' else 'fail'
        result=m.analyse(rows)
        self.assertEqual(result['complete_pairs'],6)
        self.assertEqual(result['paired_difference'],1)
        self.assertEqual(result['exact_mcnemar_p'],0.03125)
        rows[0]['outcome']='not-run';result=m.analyse(rows)
        self.assertEqual(result['complete_pairs'],5)
        self.assertEqual(result['arms'][rows[0]['arm']]['unobserved'],1)
        self.assertIn('single-task',result['scope'])

    def test_generation_preserves_code_without_repairs(self):
        m=module();p=m.load_plan();code='export class AssetPool { /* deliberately incomplete synthetic */ }\n'
        r={'id':'resp_synthetic','model':p['model'],'status':'completed','usage':{'input_tokens':1,'output_tokens':1,'total_tokens':2},
          'output':[{'type':'message','content':[{'type':'output_text','text':json.dumps({'asset_pool_mjs':code})}]}]}
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ,{'OPENAI_API_KEY':'synthetic-not-a-real-key'}), patch.object(m,'call_provider',return_value=(r,{})):
            out=Path(temp)/'run';result=m.generate(p,out,execute=True)
            for row in result['samples']:
                self.assertEqual((out/'samples'/row['id']/'candidate'/'asset-pool.mjs').read_bytes(),code.encode())
            blinded=json.loads((out/'blinded.json').read_text())
            self.assertTrue(all('arm' not in row and 'pair' not in row for row in blinded['samples']))

class ABFailureAccountingTests(unittest.TestCase):
    def test_transport_failure_cost_is_unknown_not_zero(self):
        m=module()
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ,{'OPENAI_API_KEY':'synthetic-not-a-real-key'}), patch.object(m,'call_provider',side_effect=OSError('transport')):
            result=m.generate(m.load_plan(),Path(temp)/'run',execute=True)
            self.assertIsNone(result['observed_cost_estimate_usd'])

    def test_all_generation_failures_are_observed_failures_not_missing_engine_setup(self):
        m=module();p=m.load_plan()
        invalid={'id':'resp_synthetic','model':p['model'],'status':'incomplete','usage':{'input_tokens':1,'output_tokens':1,'total_tokens':2},'output':[]}
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ,{'OPENAI_API_KEY':'synthetic-not-a-real-key'}), patch.object(m,'call_provider',return_value=(invalid,{})), patch.object(m,'child') as child:
            folder=Path(temp);m.generate(p,folder/'collection',execute=True)
            report=m.evaluate(folder/'collection',folder/'runtime-not-needed',folder/'out')
            self.assertEqual(report['status'],'evaluated')
            self.assertEqual(report['analysis']['complete_pairs'],6)
            self.assertEqual(report['analysis']['arms']['with-skill']['success_rate'],0)
            child.assert_not_called()

if __name__=='__main__':unittest.main()
