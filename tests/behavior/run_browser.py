"""Execute generated specimens in a real browser and retain scoped evidence.

Requires acquired inputs and Python Playwright. No external model call, network
asset discovery, Marketplace action or external game code is executed here.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from functools import partial
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import importlib.metadata
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import threading
import time
import traceback
from urllib.parse import urlsplit

from acquire_inputs import verify

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ASSET_SCRIPTS=ROOT/'skills/assets/open-asset-fixture/scripts'
SKILL_PATHS=['disciplines/action-feel/SKILL.md','disciplines/asset-runtime/SKILL.md',
             'disciplines/gameplay-harness/SKILL.md','engines/threejs/SKILL.md',
             'assets/open-asset-fixture/SKILL.md']


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path,data): path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def prepare_fixture(runtime:Path,output:Path)->dict:
    acquisition=verify(runtime)
    sys.path.insert(0,str(ASSET_SCRIPTS))
    from asset_fixture import load_catalog,match_assets
    from fixture_lock import make_lock,write_lock,verify_lock,select_assets
    catalog=load_catalog(ASSET_SCRIPTS.parent/'assets/catalog.json')
    request={'kinds':['model'],'requires':['static-geometry'],'query':'KayKit dungeon','limit':3}
    selection=match_assets(catalog,request)
    if not selection['matches'] or selection['matches'][0]['id']!='kaykit-dungeon-free':
        raise ValueError('curated requirement no longer selects the pinned fixture; review, do not silently substitute')
    asset=runtime/'fixtures/banner_blue.gltf.glb';data=asset.read_bytes()
    magic,version,length=struct.unpack('<4sII',data[:12]);n,chunk_type=struct.unpack('<II',data[12:20])
    if magic!=b'glTF' or version!=2 or length!=len(data) or chunk_type!=0x4E4F534A:
        raise ValueError('invalid GLB header')
    descriptor=json.loads(data[20:20+n])
    if any('uri' in r for r in descriptor.get('images',[])+descriptor.get('buffers',[])):
        raise ValueError('this minimal fixture must be self-contained; external dependencies need explicit review')
    pin={'asset_id':'kaykit-dungeon-free','acquired_from':next(r['url'] for r in acquisition['files'] if r['path'].endswith('.glb')),
         'files':['banner_blue.gltf.glb'],'license_file':'LICENSE.txt',
         'properties':{'kinds':['model'],'formats':['glb'],'capabilities':['static-geometry'],'capability_formats':{'static-geometry':['glb']}},
         'inspection_note':'Pinned KayKit banner: GLB 2.0, one mesh, embedded PNG/buffer, no external URI. Static descriptor inspected here; actual decoding and WebGL results are separately recorded by run_browser.py.'}
    lock=make_lock(catalog,runtime/'fixtures',pin);lockpath=output/'fixture.lock.json';write_lock(lockpath,lock)
    local=select_assets(catalog,runtime/'fixtures',[lockpath],dict(request,formats=['glb']),pinned_only=True)
    if not local['matches']:raise ValueError('the inspected GLB failed local fixture reuse')
    tamper_detected=False
    with tempfile.TemporaryDirectory(prefix='fixture-negative-') as tmp:
        root=Path(tmp);shutil.copytree(runtime/'fixtures',root/'fixtures');p=root/'fixtures/banner_blue.gltf.glb'
        p.write_bytes(p.read_bytes()[:-1]+bytes([p.read_bytes()[-1]^1]))
        try: verify_lock(catalog,root/'fixtures',lock)
        except ValueError: tamper_detected=True
    rig=select_assets(catalog,runtime/'fixtures',[lockpath],{'kinds':['model'],'requires':['skeletal-animation'],'formats':['glb'],'limit':1},pinned_only=True)
    report={'source_selection':selection,'local_selection':local,'integrity':verify_lock(catalog,runtime/'fixtures',lock),
            'negative_controls':{'tampered_bytes_rejected':tamper_detected,'static_model_not_accepted_as_rig':not rig['matches']},
            'status':'pass' if tamper_detected and not rig['matches'] else 'fail',
            'scope':'executed asset matcher and integrity checks; decoding occurs in the browser'}
    write(output/'asset-preparation.json',report)
    return report


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass


def run(runtime:Path,output:Path,browser_path:str|None,build_ref:str)->int:
    output.mkdir(parents=True,exist_ok=False)
    report={'schema_version':1,'suite':'combat-and-asset-lifetime-v1','status':'not-run',
            'started_at':datetime.now(timezone.utc).isoformat(),'build_ref':build_ref,
            'generator':{'kind':'current-conversation-assistant','declared_model':'GPT-6 Astra Pro',
                         'generation_sample_count':1,'external_api_run_id':None,'blinded_ab_test':'not-run'},
            'human_playtest':'not-run','cross_engine':'not-run','skill_sources':[],
            'scope':'Generated example execution, not universal certification or causal proof of Skill improvement.'}
    for name in SKILL_PATHS:
        p=ROOT/'skills'/name;report['skill_sources'].append({'path':'skills/'+name,'sha256':sha(p)})
    report['generated_sources']=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(HERE.iterdir()) if p.is_file()]
    write(output/'generation-request.json',{'request':'Build minimal behavior tests using gameplay-harness, open-asset-fixture and executable engine examples.',
          'selected_requirements':['actor-local hitstop','contact deduplication','deterministic replay','shared resource leases','stale scene suppression','real GLB and PNG decode','WebGL resource cleanup'],
          'input_kind':'requirements restatement plus the recorded skill source hashes; not an API conversation transcript',
          'outputs':report['generated_sources']})
    start=time.monotonic();code=2
    try:
        report['asset_preparation']=prepare_fixture(runtime,output)
        from playwright.sync_api import sync_playwright
        report['playwright_version']=importlib.metadata.version('playwright')
        with tempfile.TemporaryDirectory(prefix='behavior-web-') as temp:
            public=Path(temp)
            for name in ['index.html','browser.mjs','simulation.mjs','asset-pool.mjs']:
                shutil.copyfile(HERE/name,public/name)
            shutil.copytree(runtime,public/'runtime')
            server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(public)))
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            try:
                with sync_playwright() as p:
                    opts={'headless':True,'args':['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']}
                    if browser_path:opts['executable_path']=browser_path
                    browser=p.chromium.launch(**opts);report['browser_version']=browser.version
                    context=browser.new_context(viewport={'width':1280,'height':1000},device_scale_factor=1)
                    origin=f'http://127.0.0.1:{server.server_port}'
                    def route(req):
                        if req.request.url.startswith(origin+'/') or urlsplit(req.request.url).scheme in {'data','blob'}:req.continue_()
                        else:req.abort()
                    context.route('**/*',route)
                    page=context.new_page();errors=[];console=[];network=[]
                    page.on('pageerror',lambda e:errors.append(str(e)))
                    page.on('console',lambda m:console.append({'type':m.type,'text':m.text}))
                    page.on('requestfailed',lambda r:network.append({'url':r.url,'failure':r.failure}))
                    page.goto(origin+'/index.html',wait_until='load',timeout=30000)
                    page.wait_for_function('window.__lab && window.__lab.ready',timeout=90000)
                    result=page.evaluate('window.__lab.result')
                    if result.get('status')=='blocked':raise RuntimeError(result.get('error','browser initialization failed'))
                    # Native browser events go through the same semantic input map, not a debug attack setter.
                    page.evaluate('window.__lab.armInput()');page.keyboard.down('Space');page.keyboard.down('Space')
                    first=page.evaluate('window.__lab.stepInput(13)');page.keyboard.up('Space');page.keyboard.press('Space')
                    second=page.evaluate('window.__lab.stepInput(3)')
                    hits1=len([e for e in first['events'] if e['type']=='hit']);hits2=len([e for e in second['events'] if e['type']=='hit'])
                    native={'id':'native-keyboard-edge-deduplication','status':'pass' if (hits1,hits2)==(1,2) else 'fail',
                            'expected':[1,2],'observed':[hits1,hits2],'driver':'Playwright Chromium keyboard events; not human input'}
                    result['scenarios'].append(native);write(output/'native-input-trace.json',{'first':first,'second':second})
                    report['runtime']=result;report['browser_errors']=errors;report['console']=console;report['network_failures']=network
                    page.screenshot(path=str(output/'engine-screenshot.png'),full_page=True)
                    failures=[r for r in result['scenarios'] if r['status']!='pass']
                    survived=[r for r in result['negative_controls'] if r['status']!='detected']
                    good=result['status']=='pass' and not failures and not survived and not errors and not network and not any(m['type']=='error' for m in console) and report['asset_preparation']['status']=='pass'
                    report['status']='pass' if good else 'fail';code=0 if good else 1
                    context.close();browser.close()
            finally:server.shutdown();server.server_close();thread.join(timeout=3)
    except Exception as exc:
        report['status']='blocked';report['reason']=str(exc);report['traceback']=traceback.format_exc();code=2
    report['elapsed_seconds']=round(time.monotonic()-start,3)
    report['completed_at']=datetime.now(timezone.utc).isoformat()
    report['artifacts']=[{'path':p.name,'sha256':sha(p)} for p in sorted(output.iterdir()) if p.is_file()]
    write(output/'report.json',report)
    print(json.dumps({'status':report['status'],'checks':len(report.get('runtime',{}).get('scenarios',[])),
                      'negative_controls':len(report.get('runtime',{}).get('negative_controls',[])),
                      'report':str(output/'report.json'),'reason':report.get('reason')},indent=2))
    return code


def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--browser');parser.add_argument('--build-ref',default='local-uncommitted-see-source-hashes')
    a=parser.parse_args()
    return run(a.runtime.resolve(),a.output.resolve(),a.browser,a.build_ref)

if __name__=='__main__':raise SystemExit(main())
