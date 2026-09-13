"""Pin/revalidate selected local data; never download, extract, decode or execute it."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any

from asset_fixture import (PACK, ATTRIBUTION, KINDS, credit, https_url, load_catalog,
                           match_assets, read_json, strings, validate_request)

DATA = {'png','jpg','jpeg','webp','svg','glb','gltf','bin','obj','mtl','fbx','blend',
        'wav','ogg','mp3','flac','hdr','exr','ktx2','efk','efkefc','efkproj','efkmodel'}
LIMIT = 128 * 1024 * 1024


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()


def asset_record(catalog: dict, asset_id: str, allow_attribution: bool) -> dict:
    if type(allow_attribution) is not bool:
        raise ValueError('attribution opt-in must be boolean')
    matches=[a for a in catalog['assets'] if a['id']==asset_id]
    if len(matches)!=1:
        raise ValueError('unknown or duplicate asset id')
    a=matches[0]
    if a['cost']!='free' or not (a['license']=='CC0-1.0' or (allow_attribution and a['license'] in ATTRIBUTION)):
        raise ValueError('asset excluded by license/cost policy')
    return a


def checked_path(root: Path, name: Any) -> Path:
    if (not isinstance(name,str) or not name or '\\' in name or ':' in name
            or any(ord(c)<32 for c in name) or name.startswith('/')
            or any(p in {'','.', '..'} for p in name.split('/'))):
        raise ValueError('invalid relative data path')
    root=root.absolute()
    if any(p.is_symlink() for p in (root,*root.parents)):
        raise ValueError('symlink fixture root is not allowed')
    p=root
    for part in PurePosixPath(name).parts:
        p=p/part
        if p.is_symlink():
            raise ValueError('symlink data is not allowed')
    if not p.is_file() or not p.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'missing or external file: {name}')
    return p


def file_record(root: Path, name: str, *, evidence: bool=False, max_bytes: int=LIMIT) -> dict:
    p=checked_path(root,name)
    allowed={'txt','md','json','html'} if evidence else DATA
    if p.suffix.lower().lstrip('.') not in allowed:
        raise ValueError(f'unsupported data/evidence extension: {name}')
    if type(max_bytes) is not int or max_bytes<=0:
        raise ValueError('max_bytes must be a positive integer')
    size=p.stat().st_size
    if not 0<size<=max_bytes:
        raise ValueError(f'empty or oversized file: {name}')
    h=hashlib.sha256();count=0
    with p.open('rb') as f:
        while block:=f.read(1024*1024):
            count+=len(block)
            if count>max_bytes:
                raise ValueError('file grew beyond byte limit')
            h.update(block)
    if count!=size:
        raise ValueError('file changed size during hashing')
    return {'path':name,'size':count,'sha256':h.hexdigest()}


def inspected_properties(value: Any, files: list[str]) -> dict:
    if not isinstance(value,dict) or set(value)!={'kinds','capabilities','formats'}:
        raise ValueError('explicit inspected kinds/capabilities/formats required')
    for key in value:
        strings(value[key],key,nonempty=key!='capabilities')
    if not set(value['kinds'])<=KINDS:
        raise ValueError('unknown inspected kind')
    extensions={PurePosixPath(p).suffix.lower().lstrip('.') for p in files}
    if not set(value['formats'])<=extensions:
        raise ValueError('inspected format has no corresponding selected file')
    return value


def make_lock(catalog: dict, root: Path, request: dict, *, allow_attribution: bool=False, max_bytes: int=LIMIT) -> dict:
    keys={'asset_id','acquired_from','files','license_file','properties','inspection_note'}
    if not isinstance(request,dict) or set(request)!=keys:
        raise ValueError('pin request fields do not match the documented schema')
    a=asset_record(catalog,request['asset_id'],allow_attribution)
    if not https_url(request['acquired_from']):
        raise ValueError('acquired_from must be a credential-free HTTPS URL')
    names=strings(request['files'],'files',nonempty=True)
    if len(names)>1000 or request['license_file'] in names:
        raise ValueError('too many files or license evidence mixed with data')
    note=request['inspection_note']
    if not isinstance(note,str) or not note.strip():
        raise ValueError('file-level inspection note required')
    props=inspected_properties(request['properties'],names)
    files=[]; remaining=max_bytes
    for name in sorted(names):
        record=file_record(root,name,max_bytes=remaining)
        files.append(record); remaining-=record['size']
    evidence=file_record(root,request['license_file'],evidence=True,max_bytes=remaining)
    return {'schema_version':1,'asset_id':a['id'],'metadata_sha256':digest(a),
            'acquired_from':request['acquired_from'],'properties':props,'inspection_note':note,
            'files':files,'license_evidence':evidence,'credit':credit(a),'runtime_validation':'not-run'}


def verify_lock(catalog: dict, root: Path, lock: Any, *, allow_attribution: bool=False) -> dict:
    keys={'schema_version','asset_id','metadata_sha256','acquired_from','properties','inspection_note',
          'files','license_evidence','credit','runtime_validation'}
    if not isinstance(lock,dict) or set(lock)!=keys or type(lock['schema_version']) is not int or lock['schema_version']!=1:
        raise ValueError('invalid lock schema')
    if lock['runtime_validation']!='not-run' or not isinstance(lock['files'],list) or not lock['files']:
        raise ValueError('invalid lock status/files')
    rows=[*lock['files'],lock['license_evidence']]
    for row in rows:
        if (not isinstance(row,dict) or set(row)!={'path','size','sha256'} or type(row['size']) is not int
                or not isinstance(row['sha256'],str) or not re.fullmatch('[0-9a-f]{64}',row['sha256'])):
            raise ValueError('invalid file record')
    request={'asset_id':lock['asset_id'],'acquired_from':lock['acquired_from'],
             'files':[f['path'] for f in lock['files']], 'license_file':lock['license_evidence']['path'],
             'properties':lock['properties'],'inspection_note':lock['inspection_note']}
    expected=make_lock(catalog,root,request,allow_attribution=allow_attribution)
    if expected!=lock:
        raise ValueError('lock metadata, credit or local bytes changed; inspect and explicitly repin')
    return {'status':'integrity-verified','asset_id':lock['asset_id'],
            'scope':'local byte/metadata consistency, not authenticity, decoding, dependency completeness or engine behavior',
            'runtime_validation':'not-run'}


def write_lock(path: Path, lock: dict) -> None:
    # Parent must exist. Exclusive creation prevents replacing a reviewed lock.
    with path.open('x',encoding='utf-8') as f:
        f.write(json.dumps(lock,ensure_ascii=False,indent=2)+'\n')


def select_assets(catalog: dict, root: Path, lock_paths: list[Path], request: dict, *, pinned_only: bool=False) -> dict:
    req=validate_request(request)
    remote=match_assets(catalog,dict(req,limit=20))
    local=[];invalid=[];seen=set()
    for path in sorted(set(lock_paths),key=str):
        try:
            if path.stat().st_size>1024*1024:
                raise ValueError('oversized lock')
            lock=read_json(path)
            verify_lock(catalog,root,lock,allow_attribution=req['allow_attribution'])
            props=lock['properties']
            if (not set(req['kinds'])&set(props['kinds']) or not set(req['requires'])<=set(props['capabilities'])
                    or (req['formats'] and not set(req['formats'])&set(props['formats']))):
                continue
            identity=digest(lock)
            if identity in seen: continue
            seen.add(identity)
            a=asset_record(catalog,lock['asset_id'],req['allow_attribution'])
            local.append({'id':a['id'],'status':'local-integrity-verified','lock':str(path),
                          'properties':props,'credit':lock['credit'],'runtime_validation':'not-run'})
        except (OSError,ValueError,TypeError,KeyError) as exc:
            invalid.append({'lock':str(path),'reason':str(exc)})
    local.sort(key=lambda a:(a['id'],a['lock']))
    local_ids={a['id'] for a in local}
    matches=(local+([] if pinned_only else [a for a in remote['matches'] if a['id'] not in local_ids]))[:req['limit']]
    return {'status':'matched' if matches else 'unmatched','matches':matches,'invalid_locks':invalid,
            'catalog_rejections':remote['rejected'],'mode':'pinned-only' if pinned_only else 'library-first',
            'runtime_validation':'not-run'}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog',type=Path,default=PACK/'assets/catalog.json')
    parser.add_argument('--root',type=Path,required=True,help='Explicit read-only asset directory')
    sub=parser.add_subparsers(dest='command',required=True)
    pin=sub.add_parser('pin');pin.add_argument('--request',type=Path,required=True);pin.add_argument('--output',type=Path,required=True);pin.add_argument('--allow-attribution',action='store_true')
    verify=sub.add_parser('verify');verify.add_argument('--lock',type=Path,required=True);verify.add_argument('--allow-attribution',action='store_true')
    select=sub.add_parser('select');select.add_argument('--request',type=Path,required=True);select.add_argument('--locks',type=Path,nargs='*',default=[]);select.add_argument('--pinned-only',action='store_true')
    args=parser.parse_args()
    try:
        catalog=load_catalog(args.catalog)
        if args.command=='pin':
            result=make_lock(catalog,args.root,read_json(args.request),allow_attribution=args.allow_attribution);write_lock(args.output,result)
        elif args.command=='verify': result=verify_lock(catalog,args.root,read_json(args.lock),allow_attribution=args.allow_attribution)
        else: result=select_assets(catalog,args.root,args.locks,read_json(args.request),pinned_only=args.pinned_only)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 2 if result.get('status')=='unmatched' else 0
    except (OSError,ValueError,TypeError,KeyError) as exc:
        print(f'Fixture operation failed: {exc}',file=sys.stderr);return 1


if __name__=='__main__': raise SystemExit(main())
