"""Reproduce overlapping-atlas-rectangle pollution with anonymous native fixtures."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'skills/2d/spine-skeletal/scripts'))
from audit_attachment_ownership import audit


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    def save(name,pixels):
        file=out/name;Image.fromarray(pixels).save(file)
        return {'path':name,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}
    owner=np.zeros((8,9),np.uint16);owner[1,1:6]=1;owner[1:6,1]=1;owner[4,3:7]=2;owner[2:5,6]=2
    atlas=np.zeros((8,9,4),np.uint8);atlas[owner==1]=[44,88,190,253];atlas[owner==2]=[220,164,230,252]
    source=save('atlas.png',atlas);mapping=save('owners.png',owner)
    near=np.where((owner[1:6,1:6]==1)[:,:,None],atlas[1:6,1:6],0);far=np.where((owner[2:5,3:7]==2)[:,:,None],atlas[2:5,3:7],0)
    correct=save('near-owned.png',near);wrong=save('near-rectangle.png',atlas[1:6,1:6]);other=save('far-owned.png',far)
    results={}
    for label,image in [('rectangle',wrong),('owned',correct)]:
        data={'schema':'ogs.attachment-ownership/1','atlas':source,'ownership':mapping,'parts':[
            {'id':'near','ownerId':1,'bounds':[1,1,6,6],'image':image},
            {'id':'far','ownerId':2,'bounds':[3,2,7,5],'image':other}]}
        path=out/(label+'-contract.json');path.write_text(json.dumps(data,indent=2)+'\n');results[label]=audit(path);(out/(label+'-report.json')).write_text(json.dumps(results[label],indent=2)+'\n')
    # The rejected fixture must defeat the old rectangle-equality check.
    np.testing.assert_array_equal(np.array(Image.open(out/'near-rectangle.png')),atlas[1:6,1:6])
    assert results['rectangle']['status']=='FAIL' and results['rectangle']['duplicatedSourceCorePixels']==3
    assert results['owned']['status']=='PASS-NATIVE-OWNERSHIP'
    s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="400" viewBox="0 0 1080 400"><rect width="1080" height="400" rx="16" fill="#111827"/>']
    panels=[('Shared source',atlas,0),('Rectangle export A',atlas[1:6,1:6],1),('Owned export A',near,2)]
    for title,pixels,col in panels:
        x=25+col*355;s.append(f'<text x="{x}" y="36" fill="#f8fafc" font-size="22" font-family="sans-serif">{title}</text>')
        for y in range(8):
            for xx in range(9):
                s.append(f'<rect x="{x+xx*30}" y="{55+y*30}" width="29" height="29" fill="#243144"/>')
        for y,row in enumerate(pixels):
            for xx,p in enumerate(row):
                if p[3]:s.append(f'<rect x="{x+xx*30}" y="{55+y*30}" width="29" height="29" fill="rgb({p[0]},{p[1]},{p[2]})" fill-opacity="{p[3]/255}"/>')
        if col==0:
            s.append(f'<rect x="{x+30}" y="85" width="150" height="150" fill="none" stroke="#fbbf24" stroke-width="3" stroke-dasharray="6 4"/>')
            status='Two separate parts; overlapping bounds';color='#cbd5e1'
        elif col==1:
            status='FAIL: 3 foreign pixels copied';color='#fda4af'
        else:status='PASS: 0 foreign pixels';color='#86efac'
        s.append(f'<text x="{x}" y="326" fill="{color}" font-size="17" font-family="sans-serif">{status}</text>')
    s.append('<text x="25" y="368" fill="#cbd5e1" font-size="16" font-family="sans-serif">Same source paint. The rectangle copy is pixel-identical and still duplicates its neighbour.</text></svg>')
    (out/'preview.svg').write_text(''.join(s))
    summary={label:{key:r[key] for key in ['status','partCount','duplicatedSourceCorePixels','artAccepted','runtimeValidated']} for label,r in results.items()};print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
