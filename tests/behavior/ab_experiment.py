"""Independent, single-task Skill A/B collection and blind engine evaluation.

Generation never executes model code. Evaluation never receives an API secret.
This is an exploratory task-level experiment, not all-Skill certification.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import random
import signal
import subprocess
import sys
import time
from urllib.error import HTTPError
from urllib.request import Request, build_opener, HTTPRedirectHandler

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PLAN = HERE / 'experiments/asset-runtime-ab-v1/plan.json'
ENDPOINT = 'https://api.openai.com/v1/responses'
ARMS = ('without-skill', 'with-skill')
SKILL_SEPARATOR = '\n\nSupplementary Skill guidance (apply where relevant to the task above):\n'
SYSTEM = 'Implement the requested production module. Follow the interface and requirements. Return only the specified JSON object. You have no tools or access to files beyond this request.'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def now():
    return datetime.now(timezone.utc).isoformat()


def load_plan(path=PLAN):
    p=json.loads(Path(path).read_text(encoding='utf-8'))
    if (p['schema_version']!=1 or p['experiment_id']!='asset-runtime-ab-v1'
        or p['model']!='gpt-4.1-mini-2025-04-14' or p['pairs']!=6
        or p['max_output_tokens']!=4096 or p['temperature']!=0.5
        or p['estimated_budget_usd']!=0.5):
        raise ValueError('unreviewed experiment/model/budget: create a new preregistration rather than silently changing this one')
    for rel,digest in p['source_pins'].items():
        path=(ROOT/rel)
        if path.is_symlink() or not path.resolve().is_relative_to(ROOT) or sha(path)!=digest:
            raise ValueError('preregistered input drift: '+rel)
    if reserve_cost(p)>p['estimated_budget_usd']:
        raise ValueError('estimated worst-case request reserve exceeds budget')
    return p


def payload(plan, arm):
    if arm not in ARMS:raise ValueError('unknown experimental arm')
    text=(ROOT/plan['task_path']).read_text(encoding='utf-8')
    if arm=='with-skill':text+=SKILL_SEPARATOR+(ROOT/plan['skill_path']).read_text(encoding='utf-8')
    request={'model':plan['model'],'instructions':SYSTEM,'input':text,'store':False,
        'tools':[], 'temperature':plan['temperature'],'max_output_tokens':plan['max_output_tokens'],
        'text':{'format':{'type':'json_schema','name':'asset_pool_module','strict':True,
            'schema':{'type':'object','properties':{'asset_pool_mjs':{'type':'string'}},
                      'required':['asset_pool_mjs'],'additionalProperties':False}}}}
    if len(json.dumps(request).encode())>32000:raise ValueError('request exceeds predeclared byte limit')
    return request


def reserve_cost(plan):
    # Conservative UTF-8 byte count plus framing reserve, not an invoice guarantee.
    return round(sum(((len(json.dumps(payload(plan,a)).encode())+1024)*0.4
                  +plan['max_output_tokens']*1.6)/1_000_000 for a in ARMS)*plan['pairs'],6)


def allocate(plan):
    rng=random.Random(plan['order_seed']);rows=[]
    for pair in range(plan['pairs']):
        arms=list(ARMS);rng.shuffle(arms)
        for arm in arms:
            opaque=hashlib.sha256(f"{plan['experiment_id']}|{pair}|{arm}".encode()).hexdigest()[:14]
            rows.append({'id':'s-'+opaque,'pair':pair,'arm':arm})
    return rows


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise OSError('provider redirect refused')


def call_provider(request, key):
    """Exactly one HTTPS request, no implicit retries or alternative providers."""
    req=Request(ENDPOINT,data=json.dumps(request).encode(),method='POST',
        headers={'Authorization':'Bearer '+key,'Content-Type':'application/json',
                 'User-Agent':'open-game-skills-ab/1.0'})
    try:
        with build_opener(NoRedirect()).open(req,timeout=120) as response:
            data=response.read(1_000_001)
            if len(data)>1_000_000:raise OSError('provider response exceeds limit')
            metadata={'request_id':response.headers.get('x-request-id'),'http_status':response.status}
            return json.loads(data),metadata
    except HTTPError as exc:
        # Error bodies can echo parts of credentials; never persist or print them.
        raise OSError('provider HTTP '+str(exc.code)) from None


def extract_candidate(response, plan):
    if (not isinstance(response,dict) or response.get('status')!='completed'
        or response.get('model')!=plan['model'] or not str(response.get('id','')).startswith('resp_')):
        raise ValueError('response is incomplete, refused, unidentified, or from another model')
    usage=response.get('usage')
    if not isinstance(usage,dict) or any(type(usage.get(k)) is not int or usage[k]<0 for k in ('input_tokens','output_tokens','total_tokens')):
        raise ValueError('missing observed token usage')
    texts=[c['text'] for item in response.get('output',[]) if item.get('type')=='message'
           for c in item.get('content',[]) if c.get('type')=='output_text']
    if len(texts)!=1:raise ValueError('expected exactly one code response')
    result=json.loads(texts[0])
    if not isinstance(result,dict) or set(result)!={'asset_pool_mjs'}:
        raise ValueError('response violates the single-module schema')
    code=result['asset_pool_mjs']
    if not isinstance(code,str) or not 0<len(code.encode())<=200_000:
        raise ValueError('empty or oversized module')
    return code


def generate(plan, output, execute=False):
    output=Path(output)
    if output.is_symlink():raise ValueError('output must not be a symlink')
    output.mkdir(parents=True,exist_ok=False)
    samples=[{**r,'status':'not-run','response_id':None,'usage':None} for r in allocate(plan)]
    result={'schema_version':1,'experiment_id':plan['experiment_id'],'status':'planned',
        'started_at':now(),'provider_calls':0,'samples':samples,'planned_samples':len(samples),
        'plan_sha256':hashlib.sha256(json.dumps(plan,sort_keys=True).encode()).hexdigest(),
        'estimated_reserve_usd':reserve_cost(plan),'observed_cost_estimate_usd':None,
        'scope':'single-task randomized paired pilot; no human repairs, no retries, no universal Skill claim'}
    save(output/'plan.json',plan)
    save(output/'allocation.json',allocate(plan))
    for row in samples:
        folder=output/'samples'/row['id'];folder.mkdir(parents=True)
        save(folder/'request.json',payload(plan,row['arm']))
    save(output/'collection.json',result)
    key=os.environ.get('OPENAI_API_KEY','')
    if execute and not key:
        result.update(status='blocked',reason='OPENAI_API_KEY is not configured')
    elif execute:
        result['status']='collected';total_cost=0.0;cost_complete=True
        for row in samples:
            folder=output/'samples'/row['id']
            row['started_at']=now();result['provider_calls']+=1
            save(output/'collection.json',result)
            try:
                response,meta=call_provider(payload(plan,row['arm']),key)
            except (OSError,ValueError) as exc:
                cost_complete=False
                row.update(status='provider-error',error=str(exc),completed_at=now())
                result.update(status='blocked',reason='provider request failed; remaining samples not attempted')
                break
            save(folder/'response.json',response);save(folder/'provider.json',meta)
            row.update(response_id=response.get('id'),usage=response.get('usage'),response_sha256=sha(folder/'response.json'))
            usage=response.get('usage') or {}
            if all(type(usage.get(k)) is int for k in ('input_tokens','output_tokens')):
                # No cache discount assumed. Estimate, not the provider invoice.
                total_cost+=(usage['input_tokens']*0.4+usage['output_tokens']*1.6)/1_000_000
            else:
                cost_complete=False
            try:
                code=extract_candidate(response,plan)
                candidate=folder/'candidate';candidate.mkdir()
                (candidate/'asset-pool.mjs').write_bytes(code.encode('utf-8'))
                (candidate/'simulation.mjs').write_bytes((ROOT/plan['fixed_simulation']).read_bytes())
                row.update(status='generated',candidate_sha256=sha(candidate/'asset-pool.mjs'))
            except (ValueError,KeyError,TypeError) as exc:
                row.update(status='generation-failed',error=str(exc))
            row['completed_at']=now();save(output/'collection.json',result)
        result['observed_cost_estimate_usd']=round(total_cost,6) if cost_complete else None
    result['completed_at']=now()
    save(output/'collection.json',result)
    # The scorer does not receive condition labels or pair IDs.
    save(output/'blinded.json',{'experiment_id':plan['experiment_id'],'samples':[
        {k:r[k] for k in ('id','status','candidate_sha256') if k in r} for r in samples]})
    return result


def analyse(rows):
    arms={}
    for arm in ARMS:
        selected=[r for r in rows if r['arm']==arm]
        passed=sum(r.get('outcome')=='pass' for r in selected)
        failed=sum(r.get('outcome')=='fail' for r in selected)
        arms[arm]={'planned':len(selected),'passed':passed,'failed':failed,
            'unobserved':len(selected)-passed-failed,
            'success_rate':passed/(passed+failed) if passed+failed else None}
    paired=[]
    for pair in sorted({r['pair'] for r in rows}):
        match={r['arm']:r.get('outcome') for r in rows if r['pair']==pair}
        if set(match)==set(ARMS) and all(v in {'pass','fail'} for v in match.values()):paired.append(match)
    wins=sum(p['with-skill']=='pass' and p['without-skill']=='fail' for p in paired)
    losses=sum(p['with-skill']=='fail' and p['without-skill']=='pass' for p in paired)
    n=wins+losses
    pvalue=min(1,2*sum(math.comb(n,k) for k in range(min(wins,losses)+1))/2**n) if n else (1.0 if paired else None)
    return {'arms':arms,'complete_pairs':len(paired),'skill_only_wins':wins,'control_only_wins':losses,
        'paired_difference':(wins-losses)/len(paired) if paired else None,'exact_mcnemar_p':pvalue,
        'scope':'Exploratory single-task pilot with six pairs; includes extra-context effects; not multi-task or all-Skill proof.'}


def child(command, timeout=150):
    # No credentials reach generated JavaScript or the browser driver subprocess.
    allowed={'PATH','HOME','TMPDIR','TMP','TEMP','DISPLAY','XAUTHORITY','LANG','LC_ALL','LD_LIBRARY_PATH','PLAYWRIGHT_BROWSERS_PATH'}
    env={k:v for k,v in os.environ.items() if k in allowed}
    proc=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,
                          env=env,start_new_session=True)
    try:
        text,_=proc.communicate(timeout=timeout)
        return proc.returncode,text
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid,signal.SIGKILL);text,_=proc.communicate()
        return 124,text+'\nOuter execution deadline exceeded.\n'


def evaluate(collection, runtime, output, browser=None):
    collection=Path(collection);output=Path(output);output.mkdir(parents=True,exist_ok=False)
    plan=load_plan();stored=json.loads((collection/'plan.json').read_text())
    if stored!=plan:raise ValueError('collection differs from current preregistration')
    generation=json.loads((collection/'collection.json').read_text())
    rows=generation['samples'];allocation=allocate(plan)
    if [{k:r[k] for k in ('id','pair','arm')} for r in rows]!=allocation:raise ValueError('allocation differs')
    result={'schema_version':1,'status':'not-run','experiment_id':plan['experiment_id'],'samples':[],
        'provider_calls':generation['provider_calls'],'started_at':now(),'outcome_scope':'AssetPool only; other modules fixed'}
    def command(candidate, destination, label):
        args=[sys.executable,str(HERE/'run_candidate.py'),'--runtime',str(Path(runtime).resolve()),
              '--output',str(destination.resolve()),'--candidate-label',label]
        if candidate:args+=['--candidate-dir',str(candidate.resolve())]
        if browser:args+=['--browser',browser]
        return args
    if not any(r['status']=='generated' for r in rows):
        result.update(status='evaluated' if all(r['status']=='generation-failed' for r in rows) else 'blocked',
                      reason='no generated candidates; no engine A/B was executed')
        for r in rows:result['samples'].append({**r,'outcome':'fail' if r['status']=='generation-failed' else 'not-run'})
    else:
        # Same-machine reference readiness protects against calling infrastructure failure a model failure.
        code,text=child(command(None,output/'reference','reference-readiness'))
        (output/'reference.log').write_text(text)
        if code!=0:
            result.update(status='blocked',reason='reference engine readiness failed')
            result['samples']=[{**r,'outcome':'not-run'} for r in rows]
        else:
            result['status']='evaluated'
            import evidence_gate
            for row in rows:
                scored={**row,'outcome':'not-run'}
                folder=collection/'samples'/row['id']
                if row['status']=='generation-failed':scored['outcome']='fail'
                elif row['status']=='generated':
                    request=json.loads((folder/'request.json').read_text())
                    response=json.loads((folder/'response.json').read_text())
                    code_source=extract_candidate(response,plan)
                    candidate=folder/'candidate'
                    if (request!=payload(plan,row['arm']) or sha(folder/'response.json')!=row['response_sha256']
                        or (candidate/'asset-pool.mjs').read_bytes()!=code_source.encode()
                        or sha(candidate/'asset-pool.mjs')!=row['candidate_sha256']
                        or sha(candidate/'simulation.mjs')!=plan['source_pins'][plan['fixed_simulation']]):
                        raise ValueError('candidate/request/provider provenance differs; never auto-repair')
                    dest=output/row['id']
                    rc,text=child(command(candidate,dest,row['id']))
                    (output/(row['id']+'.log')).write_text(text)
                    report=json.loads((dest/'report.json').read_text()) if (dest/'report.json').exists() else {}
                    if rc==2:
                        scored.update(outcome='not-run',reason='candidate setup blocked')
                    else:
                        errors=evidence_gate.verify(dest) if rc==0 else ['engine candidate execution failed']
                        scored.update(outcome='pass' if rc==0 and not errors else 'fail',
                            exit_code=rc,oracle_errors=report.get('oracle_errors',errors),
                            engine_status=report.get('status','incomplete'),evidence_path=row['id'])
                    # This is API output evaluation, not proof of global Skill reliability.
                result['samples'].append(scored)
                save(output/'result.json',result)
    result['analysis']=analyse(result['samples']);result['completed_at']=now()
    save(output/'result.json',result)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='action',required=True)
    g=sub.add_parser('generate');g.add_argument('--output',type=Path,required=True);g.add_argument('--execute',action='store_true')
    e=sub.add_parser('evaluate');e.add_argument('--collection',type=Path,required=True);e.add_argument('--runtime',type=Path,required=True);e.add_argument('--output',type=Path,required=True);e.add_argument('--browser')
    args=parser.parse_args()
    try:
        result=generate(load_plan(),args.output,args.execute) if args.action=='generate' else evaluate(args.collection,args.runtime,args.output,args.browser)
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print(json.dumps({'status':'blocked','reason':str(exc)}));return 2
    print(json.dumps({k:v for k,v in result.items() if k not in {'samples'}},indent=2))
    return 2 if result['status']=='blocked' else 0

if __name__=='__main__':raise SystemExit(main())
