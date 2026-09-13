"""Offline, deterministic discovery of open-licensed game-test asset candidates.

No network calls, archive extraction, engine execution or model calls occur here.
Pack-level metadata is not evidence that a particular file passes a game test.
"""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlsplit

PACK = Path(__file__).resolve().parents[1]
KINDS = {'sprite','tileset','model','animation','sfx','music','vfx','texture','hdri','ui'}
ATTRIBUTION = {'CC-BY-3.0','CC-BY-4.0'}
ALIASES = {
    '烟雾': 'smoke', '煙霧': 'smoke', '爆炸': 'explosion', '粒子': 'particle',
    '特效': 'vfx', '骨骼': 'skeletal', '动画': 'animation', '動畫': 'animation',
    '角色': 'character', '平台': 'platformer', '像素': 'pixel', '地牢': 'dungeon',
    '贴图': 'texture', '貼圖': 'texture', '材质': 'material', '材質': 'material',
    '天空': 'sky', '音效': 'sound', '音乐': 'music', '音樂': 'music',
    '按钮': 'button', '按鈕': 'button', '低多边形': 'low poly', '自然': 'nature',
}


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def strings(value: Any, label: str, *, nonempty: bool = False) -> list[str]:
    if (not isinstance(value, list) or any(not isinstance(s,str) or not s.strip() for s in value)
            or len(value) != len(set(value)) or (nonempty and not value)):
        raise ValueError(f'{label} must be a unique string list')
    return value


def https_url(value: Any) -> bool:
    if not isinstance(value, str) or any(c.isspace() for c in value):
        return False
    p = urlsplit(value)
    return p.scheme == 'https' and bool(p.hostname) and not p.username and not p.password


def validate_catalog(data: Any) -> dict[str, Any]:
    if not isinstance(data,dict) or data.get('schema_version') != 1 or not isinstance(data.get('revision'),str):
        raise ValueError('invalid catalog schema/revision')
    if not isinstance(data.get('assets'),list) or not data['assets']:
        raise ValueError('catalog needs asset candidates')
    seen = set()
    for a in data['assets']:
        if not isinstance(a,dict):
            raise ValueError('asset must be an object')
        for key in ('id','title','creator','edition','license','cost','access','inspection'):
            if not isinstance(a.get(key),str) or not a[key].strip():
                raise ValueError(f'asset missing {key}')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',a['id']) or a['id'] in seen:
            raise ValueError(f'invalid/duplicate asset id: {a["id"]}')
        seen.add(a['id'])
        for key in ('source_url','license_evidence_url','license_url'):
            if not https_url(a.get(key)):
                raise ValueError(f'{a["id"]}: {key} must be HTTPS without credentials')
        try:
            date.fromisoformat(a['checked_on'])
        except (KeyError,TypeError,ValueError) as exc:
            raise ValueError(f'{a["id"]}: invalid checked_on') from exc
        for key in ('kinds','formats','capabilities','tags'):
            strings(a.get(key), key, nonempty=(key == 'kinds'))
        if not set(a['kinds']) <= KINDS:
            raise ValueError(f'{a["id"]}: unknown kind')
        matrix=a.get('capability_formats',{})
        if not isinstance(matrix,dict) or not set(matrix)<=set(a['capabilities']):
            raise ValueError('capability_formats must refer to declared capabilities')
        for values in matrix.values():
            strings(values,'capability_formats',nonempty=True)
            if not set(values)<=set(a['formats']):
                raise ValueError('capability_formats must refer to declared formats')
    profiles = data.get('skill_profiles',{})
    if not isinstance(profiles,dict):
        raise ValueError('skill_profiles must be an object')
    for skill, roles in profiles.items():
        if not isinstance(skill,str) or not isinstance(roles,list) or not roles:
            raise ValueError('invalid skill profile')
        names = set()
        for role in roles:
            if not isinstance(role,dict) or set(role) != {'role','request'} or not isinstance(role['role'],str) or not role['role'] or role['role'] in names:
                raise ValueError('invalid/duplicate profile role')
            names.add(role['role'])
            validate_request(role['request'])
    no_assets = strings(data.get('no_asset_skills',[]),'no_asset_skills')
    if set(no_assets) & profiles.keys():
        raise ValueError('skill cannot require assets and be no-asset simultaneously')
    return data


def load_catalog(path: Path) -> dict[str, Any]:
    return validate_catalog(read_json(path))


def validate_request(request: Any) -> dict[str, Any]:
    allowed = {'kinds','requires','formats','query','allow_attribution','limit'}
    if not isinstance(request,dict) or set(request) - allowed:
        raise ValueError('unknown request fields')
    kinds = strings(request.get('kinds'),'kinds',nonempty=True)
    if not set(kinds) <= KINDS:
        raise ValueError('unknown requested kind')
    result = {'kinds':kinds, 'requires':strings(request.get('requires',[]),'requires'),
              'formats':strings(request.get('formats',[]),'formats'), 'query':request.get('query',''),
              'allow_attribution':request.get('allow_attribution',False), 'limit':request.get('limit',3)}
    if not isinstance(result['query'],str) or len(result['query']) > 2000:
        raise ValueError('query must be a string of at most 2000 characters')
    if type(result['allow_attribution']) is not bool:
        raise ValueError('allow_attribution must be a boolean')
    if type(result['limit']) is not int or not 1 <= result['limit'] <= 20:
        raise ValueError('limit must be an integer from 1 to 20')
    if any(not re.fullmatch('[a-z0-9]+', f) for f in result['formats']):
        raise ValueError('formats use lowercase names without dots')
    return result


def tokens(text: str) -> set[str]:
    text = text.casefold()
    for original, replacement in ALIASES.items():
        text = text.replace(original,' '+replacement+' ')
    return set(re.findall(r'[a-z0-9]+',text))


def credit(asset: dict[str, Any]) -> str:
    return f'{asset["title"]} — {asset["creator"]}; {asset["source_url"]}; {asset["license"]} ({asset["license_url"]}). Record modifications when adapting.'


def match_assets(catalog: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    validate_catalog(catalog)
    req = validate_request(request)
    query_tokens = tokens(req['query'])
    matches, rejected = [], []
    for a in catalog['assets']:
        reasons = []
        permitted = a['license']=='CC0-1.0' or (req['allow_attribution'] and a['license'] in ATTRIBUTION)
        if not permitted: reasons.append('license-policy')
        if a['cost'] != 'free': reasons.append('not-free')
        if not set(req['kinds']) & set(a['kinds']): reasons.append('kind')
        if not set(req['requires']) <= set(a['capabilities']): reasons.append('required-capability')
        compatible=set(a['formats'])
        for capability in req['requires']:
            if capability in a.get('capability_formats',{}):
                compatible &= set(a['capability_formats'][capability])
        if req['formats'] and not set(req['formats']) & compatible: reasons.append('format-unknown-or-incompatible')
        if reasons:
            rejected.append({'id':a['id'],'reasons':reasons})
            continue
        matched = sorted(query_tokens & tokens(a['title']+' '+' '.join(a['tags'])))
        row = dict(a, score=len(matched), matched_terms=matched,
                   attribution_required=a['license'] in ATTRIBUTION, credit=credit(a),
                   status='candidate-needs-file-inspection')
        matches.append(row)
    # Hard compatibility first; then CC0, relevance, easier access, and stable ID.
    access_rank = {'official-download':0,'official-api':1,'manual-download':2,'account-required':3}
    matches.sort(key=lambda a:(a['license']!='CC0-1.0', -a['score'],access_rank.get(a['access'],9), a['id']))
    return {'status':'matched' if matches else 'unmatched', 'catalog_revision':catalog['revision'],
            'matches':matches[:req['limit']], 'rejected':sorted(rejected,key=lambda a:a['id']),
            'ranking':'hard kind/capability/format/license gates, then CC0, query overlap, access, stable id',
            'runtime_validation':'not-run'}


def plan_for_skill(catalog: dict[str, Any], skill: str, allow_attribution: bool = False) -> dict[str, Any]:
    validate_catalog(catalog)
    if type(allow_attribution) is not bool:
        raise ValueError('allow_attribution must be a boolean')
    if skill in catalog.get('no_asset_skills',[]):
        return {'skill':skill,'status':'not-needed','reason':'Use synthetic state/event fixtures for logic regression; integration tests may request assets explicitly.','runtime_validation':'not-run'}
    roles = catalog.get('skill_profiles',{}).get(skill)
    if not roles:
        return {'skill':skill,'status':'needs-requirements','reason':'No curated profile. Specify kinds and required capabilities; do not substitute unrelated assets.','runtime_validation':'not-run'}
    rows=[]
    for role in roles:
        request=dict(role['request'],allow_attribution=allow_attribution)
        rows.append({'role':role['role'],'request':request,'selection':match_assets(catalog,request)})
    return {'skill':skill,'status':'planned' if all(r['selection']['status']=='matched' for r in rows) else 'unmatched',
            'roles':rows,'runtime_validation':'not-run'}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog',type=Path,default=PACK/'assets/catalog.json')
    sub=parser.add_subparsers(dest='command',required=True)
    match=sub.add_parser('match'); match.add_argument('--request',type=Path,required=True)
    plan=sub.add_parser('plan'); plan.add_argument('--skill',required=True); plan.add_argument('--allow-attribution',action='store_true')
    args=parser.parse_args()
    try:
        catalog=load_catalog(args.catalog)
        result=match_assets(catalog,read_json(args.request)) if args.command=='match' else plan_for_skill(catalog,args.skill,args.allow_attribution)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 2 if result['status'] in {'unmatched','needs-requirements'} else 0
    except (OSError,ValueError,TypeError,KeyError) as exc:
        print(f'Asset selection failed: {exc}',file=__import__('sys').stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
