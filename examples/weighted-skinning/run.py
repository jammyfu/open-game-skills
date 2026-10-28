"""Run a redistributable real-runtime trace case; the rejected build must FAIL."""
import argparse
import gzip
import importlib.util
import json
import shutil
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def run(output):
    output=Path(output).resolve();output.mkdir(parents=True,exist_ok=True)
    script=ROOT/'skills/2d/spine-skeletal/scripts/audit_skin.py'
    spec=importlib.util.spec_from_file_location('case_skin_audit',script);audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
    results={}
    for name,expected in [('current','PASS'),('narrow','FAIL')]:
        trace=output/(name+'.trace.json')
        trace.write_bytes(gzip.decompress((HERE/'cases'/(name+'.trace.json.gz')).read_bytes()))
        shutil.copyfile(HERE/'source/arm-setup.png',output/'arm-setup.png')
        result=audit.audit(trace)
        (output/(name+'.report.json')).write_text(json.dumps(result,indent=2)+'\n')
        if result['technicalStatus']!=expected:raise RuntimeError(f'{name}: expected {expected}, got {result["technicalStatus"]}')
        if result['characterAccepted']:raise RuntimeError('Technical case approved a character')
        results[name]={'expected':expected,'actual':result['technicalStatus'],'samples':result['samples'],
                       'visibleBadUVPixels':result['meshes']['arm']['visibleBadUVPixels']}
    summary={'result':'PASS: both expected outcomes reproduced','cases':results,
             'scope':'A real evaluated limb sweep; no full-character, gameplay or LLM improvement claim.'}
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True)
    print(json.dumps(run(parser.parse_args().out),indent=2))
