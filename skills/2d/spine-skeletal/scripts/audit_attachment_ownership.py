"""Audit native atlas exports against an explicitly authored ownership map.

Does not infer anatomy, paint art, approve source views or validate animation.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image


def pma(rgba):
    a=rgba.astype(np.int32)
    return np.dstack([(a[:,:,:3]*a[:,:,3,None]+127)//255,a[:,:,3]])


def pinned_file(root, entry):
    raw=Path(entry['path'])
    path=(root/raw).resolve()
    if raw.is_absolute() or not path.is_relative_to(root):
        raise ValueError('Asset path escapes the declared package')
    if hashlib.sha256(path.read_bytes()).hexdigest()!=entry['sha256']:
        raise ValueError('Pinned asset bytes changed: '+entry['path'])
    return path


def audit(contract_path):
    contract_path=Path(contract_path).resolve();root=contract_path.parent
    data=json.loads(contract_path.read_text())
    if data.get('schema')!='ogs.attachment-ownership/1':raise ValueError('Unsupported ownership contract')
    atlas=np.array(Image.open(pinned_file(root,data['atlas'])).convert('RGBA'))
    ownership=np.array(Image.open(pinned_file(root,data['ownership'])))
    if ownership.ndim!=2 or ownership.shape!=atlas.shape[:2] or ownership.dtype.kind not in 'iu':
        raise ValueError('Ownership must be a same-size integer ID image')
    threshold=data.get('alphaThreshold',32)
    if not isinstance(threshold,int) or isinstance(threshold,bool) or not 0<=threshold<255:
        raise ValueError('Invalid alpha threshold')
    parts=data.get('parts',[])
    if not parts:raise ValueError('No declared attachments')
    ids=[p['id'] for p in parts];owners=[p['ownerId'] for p in parts]
    if len(set(ids))!=len(ids) or any(not isinstance(i,str) or not i for i in ids):raise ValueError('Duplicate/invalid attachment IDs')
    if len(set(owners))!=len(owners) or any(not isinstance(i,int) or isinstance(i,bool) or i<=0 for i in owners):raise ValueError('Duplicate/invalid owner IDs')
    core=atlas[:,:,3]>threshold;unknown=core&~np.isin(ownership,owners)
    failures=[];results=[];coverage=np.zeros(core.shape,np.uint32)
    if unknown.any():failures.append({'kind':'unowned-source-core','pixels':int(unknown.sum())})
    for part in parts:
        bounds=part['bounds']
        if len(bounds)!=4 or any(not isinstance(v,int) or isinstance(v,bool) for v in bounds):raise ValueError('Invalid native crop bounds')
        x0,y0,x1,y1=bounds
        if not (0<=x0<x1<=atlas.shape[1] and 0<=y0<y1<=atlas.shape[0]):raise ValueError('Native crop outside atlas')
        exported=np.array(Image.open(pinned_file(root,part['image'])).convert('RGBA'))
        if exported.shape!=(y1-y0,x1-x0,4):raise ValueError('Export dimensions differ from native crop')
        owned=ownership[y0:y1,x0:x1]==part['ownerId'];active=exported[:,:,3]>0
        expected=np.where(owned[:,:,None],atlas[y0:y1,x0:x1],0)
        difference=np.any(pma(exported)!=pma(expected),axis=2)
        foreign=active&~owned
        missing=(expected[:,:,3]>threshold)&~(exported[:,:,3]>threshold)
        empty=not active.any()
        item={'id':part['id'],'foreignAlphaPixels':int(foreign.sum()),'nativePMAMismatchPixels':int(difference.sum()),'missingOwnedCorePixels':int(missing.sum()),'empty':empty}
        for key in ['foreignAlphaPixels','nativePMAMismatchPixels','missingOwnedCorePixels']:
            if item[key]:failures.append({'kind':key,'part':part['id'],'pixels':item[key]})
        if empty:failures.append({'kind':'empty-export','part':part['id']})
        coverage[y0:y1,x0:x1]+=exported[:,:,3]>threshold
        results.append(item)
    missing=int(np.count_nonzero(core&(coverage==0)));duplicate=int(np.count_nonzero(core&(coverage>1)))
    if missing:failures.append({'kind':'missing-source-core-in-exports','pixels':missing})
    if duplicate:failures.append({'kind':'duplicated-source-core-in-exports','pixels':duplicate})
    omitted=(atlas[:,:,3]>0)&(ownership==0)&~core
    return {'schema':'ogs.attachment-ownership-report/1','status':'FAIL' if failures else 'PASS-NATIVE-OWNERSHIP',
            'partCount':len(parts),'sourceCorePixels':int(core.sum()),'missingSourceCorePixels':missing,
            'duplicatedSourceCorePixels':duplicate,'unownedLowAlphaPixels':int(omitted.sum()),
            'unownedLowAlphaMaximum':int(atlas[:,:,3][omitted].max()) if omitted.any() else 0,
            'parts':results,'failures':failures,'artAccepted':False,'runtimeValidated':False,
            'scope':'Declared native source ownership/pixel preservation only. Semantic anatomy, source views, transformed seams, draw order and full action coverage require independent evidence.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('contract',type=Path);parser.add_argument('--out',type=Path);args=parser.parse_args()
    try:result=audit(args.contract)
    except (ValueError,KeyError,OSError,TypeError) as error:
        result={'schema':'ogs.attachment-ownership-report/1','status':'FAIL-INPUT','error':str(error),'artAccepted':False,'runtimeValidated':False}
    text=json.dumps(result,indent=2)+'\n'
    if args.out:args.out.write_text(text)
    print(text,end='')
    return 0 if result['status']=='PASS-NATIVE-OWNERSHIP' else 2


if __name__=='__main__':raise SystemExit(main())
