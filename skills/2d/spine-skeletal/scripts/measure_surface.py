"""Measure actual skin deformation, independently of bone lengths and fold checks.
Diagnostic only: no universal anatomy acceptance thresholds are inferred.
"""
from pathlib import Path
import argparse,json,hashlib
import numpy as np
from PIL import Image,ImageDraw

def stretches(rest,posed,triangles):
    r,p=rest[triangles],posed[triangles]
    rb=np.stack([r[:,1]-r[:,0],r[:,2]-r[:,0]],axis=-1)
    pb=np.stack([p[:,1]-p[:,0],p[:,2]-p[:,0]],axis=-1)
    jacobian=pb@np.linalg.inv(rb)
    return np.linalg.svd(jacobian,compute_uv=False),np.linalg.det(jacobian)

def visible_areas(uv,triangles,alpha,alpha_threshold=32):
    height,width=alpha.shape;pixels=uv*[width,height];areas=[]
    for ids in triangles:
        q=pixels[ids];x0,y0=np.maximum(np.floor(q.min(axis=0)).astype(int),0);x1,y1=np.minimum(np.ceil(q.max(axis=0)).astype(int)+1,[width,height])
        if x1<=x0 or y1<=y0:areas.append(0);continue
        mask=Image.new('L',(int(x1-x0),int(y1-y0)));ImageDraw.Draw(mask).polygon([tuple(v-[x0,y0]) for v in q],fill=255)
        areas.append(int(((np.array(mask)>0)&(alpha[y0:y1,x0:x1]>alpha_threshold)).sum()))
    return np.array(areas)

def weighted_quantile(values,weights,q):
    order=np.argsort(values);v,w=values[order],weights[order];return float(v[np.searchsorted(np.cumsum(w),q*w.sum(),side='left')])

def measure(path):
    from audit_skin import audit
    audit(path)  # Validate portable trace/source evidence; a fold FAIL is still measurable.
    raw=path.read_bytes();trace=json.loads(raw);result={}
    for name,m in trace['meshes'].items():
        tri=np.array(m['triangles']).reshape(-1,3);rest=np.array(m['setupVertices']).reshape(-1,2);uv=np.array(m['uvs']).reshape(-1,2)
        source=path.parent/m['image'];assert hashlib.sha256(source.read_bytes()).hexdigest()==m['sha256']
        alpha=np.array(Image.open(source).convert('RGBA'))[:,:,3];weights=visible_areas(uv,tri,alpha,trace['tolerances']['alphaThreshold']);visible=weights>0
        if not visible.any():raise ValueError(name+': mesh UVs cover no visible source pixels')
        low=[];high=[];areas=[]
        for frame in trace['frames']:
            singular,area=stretches(rest,np.array(frame['meshes'][name]).reshape(-1,2),tri)
            if not np.isfinite(singular).all() or not np.isfinite(area).all():raise ValueError(name+': nonfinite computed surface deformation')
            low.append(singular[:,1]);high.append(singular[:,0]);areas.append(area)
        low=np.array(low)[:,visible];high=np.array(high)[:,visible];areas=np.array(areas)[:,visible];w=np.tile(weights[visible],len(low))
        result[name]={'minimumPrincipalScale':float(low.min()),'maximumPrincipalScale':float(high.max()),'visiblePixelWeightedP05Compression':weighted_quantile(low.ravel(),w,.05),'visiblePixelWeightedP95Stretch':weighted_quantile(high.ravel(),w,.95),'minimumSignedAreaRatio':float(areas.min()),'maximumSignedAreaRatio':float(areas.max()),'sourceSHA256':m['sha256']}
    return {'schema':'ogs.skin-surface/1','traceSHA256':hashlib.sha256(raw).hexdigest(),'scope':trace.get('provenance',{}).get('scope'),'meshes':result,'characterAccepted':False,'status':'MEASURED-NOT-ACCEPTED','limitations':'Source-visible local surface scales, not bone scales. Overlapping UV triangle raster samples are weighted independently. Numeric data cannot approve anatomy or imply universal allowed deformation.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('trace',type=Path);p.add_argument('--out',required=True,type=Path);a=p.parse_args();code=0
    try:report=measure(a.trace)
    except (ValueError,KeyError,TypeError,OSError,IndexError,OverflowError) as e:report={'status':'BLOCKED','errors':[str(e)],'characterAccepted':False};code=2
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');print(json.dumps(report,indent=2));raise SystemExit(code)
if __name__=='__main__':main()
