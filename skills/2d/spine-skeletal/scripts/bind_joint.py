"""Author named two-bone bindings for a reviewed joint patch in setup world space.

Input: vertices:[[x,y],...], bones:[{name,world:[a,b,c,d,x,y]},...],
envelope:{origin:[x,y],axis:[x,y],start:number,end:number}.
This is a local joint tool, not an automatic whole-character rig or anatomy solver.
"""
import argparse
import json
import math
from pathlib import Path


def finite(values, size):
    if not isinstance(values, (list, tuple)) or len(values)!=size or not all(type(v) in (int,float) and math.isfinite(v) for v in values):
        raise ValueError(f'Expected {size} finite numbers')
    return values


def bind_pair(point, bones, envelope):
    px,py=finite(point,2)
    if len(bones)!=2 or len({b['name'] for b in bones})!=2 or not all(isinstance(b['name'],str) and b['name'] for b in bones):
        raise ValueError('Exactly two distinct named setup bones required')
    ox,oy=finite(envelope['origin'],2);ax,ay=finite(envelope['axis'],2)
    start,end=finite([envelope['start'],envelope['end']],2)
    magnitude=math.hypot(ax,ay)
    if magnitude==0 or end<=start:raise ValueError('Nonzero axis and increasing envelope bounds required')
    along=((px-ox)*ax+(py-oy)*ay)/magnitude
    t=max(0,min(1,(along-start)/(end-start)));t=t*t*(3-2*t)
    result=[]
    for bone,weight in zip(bones,[1-t,t]):
        a,b,c,d,x,y=finite(bone['world'],6)
        det=a*d-b*c
        if not math.isfinite(det) or abs(det)<1e-12:raise ValueError('Singular setup bone matrix')
        if weight>0:
            dx,dy=px-x,py-y
            local_x,local_y=(d*dx-b*dy)/det,(-c*dx+a*dy)/det
            if not math.isfinite(local_x) or not math.isfinite(local_y):raise ValueError('Nonfinite bind coordinate')
            result.append(dict(bone=bone['name'],x=local_x,y=local_y,weight=weight))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path);parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args();data=json.loads(args.input.read_text())
    weights=[bind_pair(p,data['bones'],data['envelope']) for p in data['vertices']]
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps({'weights':weights,'status':'authored-bindings-not-accepted'},indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
