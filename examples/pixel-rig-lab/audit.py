"""Convert actual browser runtime matrices/vertices to the existing portable audit."""
from pathlib import Path
import json,hashlib,sys,subprocess
import numpy as np
from PIL import Image
P=Path(__file__).parent;R=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/pixel-rig-frames');raw=json.loads((R/'runtime.json').read_text());meta=raw['meta'];setup=meta['setup'];meshes={}
def record(name):return {'image':'../assets/'+name+'.png','sha256':hashlib.sha256((P/'assets'/(name+'.png')).read_bytes()).hexdigest()}
for bone,name,px,py in meta['attachments']:
 meshes[bone]={**record(name),'uvs':[0,0,1,0,1,1,0,1],'triangles':[0,1,2,0,2,3],'weights':[[{'bone':bone,'weight':1}] for _ in range(4)],'setupVertices':setup['meshes'][bone]}
meshes['scarf']={**record('scarf'),'uvs':meta['uv'],'triangles':[v for t in meta['tris'] for v in t],'weights':meta['weights'],'setupVertices':setup['meshes']['scarf']}
segments=[]
for a,b,length in [('lthigh','lk',25),('lshin','lboot',26),('rthigh','rk',25),('rshin','rboot',26),('lupper','le',22),('lfore','lw',28),('rupper','re',22),('rfore','rw',28),('cloth0','cloth1',14),('cloth1','cloth2',14)]:segments.append(dict(a=a,b=b,length=length))
for name in ['scene-000.png','scene-048.png']:
 Image.open(R/name).save(P/'docs'/name)
trace={'schema':'ogs.skin-trace/1','sampleRate':12,'tolerances':{'length':1e-6,'scale':1e-6,'loop':1e-6,'weights':1e-6,'area':1e-7,'alphaThreshold':32},'boneScales':{b:[1,1] for b in setup['bones']},'segments':segments,'meshes':meshes,'frames':raw['frames'],'loops':[{'first':0,'last':48,'firstImage':'scene-000.png','lastImage':'scene-048.png'}],'contacts':[{'bone':b,'first':0,'last':48,'target':xy,'tolerance':1e-6} for b,xy in [('lboot',[210,175]),('rboot',[241,175])]]}
(P/'docs'/'trace.json').write_text(json.dumps(trace)+'\n')
# Pixel exactness checked on browser-exported raster, independently from skeleton math.
a=np.array(Image.open(R/'native.png').convert('RGBA'));b=np.array(Image.open(R/'scene-000.png').convert('RGBA'));assert np.array_equal(b,np.repeat(np.repeat(a,2,0),2,1))
assert Image.open(R/'scene-000.png').tobytes()==Image.open(R/'scene-048.png').tobytes()
owner=json.loads((P/'assets'/'parts.json').read_text());assert len(owner)==8
report={'renderer':'Chrome Canvas2D','samples':49,'loop_seconds':4,'native':[480,270],'display':[960,540],'exact_2x_pixel_replication':True,'loop_rgba_exact':True,'attachments':8,'rigid_instances':12,'weighted_cloth_bones':3,'native_to_display_filter':'nearest','source_ownership':'Eight separate cell crops with binary alpha; semantic names visually inspected, not automatic anatomy recognition','max_contact_origin_error':max(np.hypot(f['bones'][b]['x']-xy[0],f['bones'][b]['y']-xy[1]) for f in raw['frames'] for b,xy in [('lboot',[210,175]),('rboot',[241,175])]),'claimed_acceptance':'technical checks plus recorded images, not independent character art acceptance'}
(P/'docs'/'pixel-report.json').write_text(json.dumps(report,indent=2)+'\n')
root=P.parents[1]
for script,out in [('audit_skin.py','skin-audit.json'),('measure_surface.py','surface.json')]:
 cmd=[sys.executable,str(root/'skills/2d/spine-skeletal/scripts'/script),str(P/'docs/trace.json'),'--out',str(P/'docs'/out)]
 subprocess.run(cmd,check=True)
print(json.dumps(report,indent=2))

# A deliberately broken observed contact must be rejected with unchanged gates.
negative=json.loads(json.dumps(trace));negative['frames'][24]['bones']['lboot']['x']+=3
npth=P/'docs/.negative-trace.json';npth.write_text(json.dumps(negative))
cmd=[sys.executable,str(root/'skills/2d/spine-skeletal/scripts/audit_skin.py'),str(npth),'--out',str(P/'docs/rejected-contact.json')]
r=subprocess.run(cmd,capture_output=True,text=True);npth.unlink();assert r.returncode==1,'negative contact was not rejected'
subprocess.run([sys.executable,str(root/'skills/2d/spine-skeletal/scripts/audit_attachment_ownership.py'),str(P/'assets/ownership.json'),'--out',str(P/'docs/ownership-report.json')],check=True)

# Compare actual rendered sole strips, not just the authored ankle target.
base=np.array(Image.open(R/'scene-000.png'))
for n in range(49):
 im=np.array(Image.open(R/f'scene-{n:03}.png'))
 for x0,x1 in [(204,228),(235,259)]:
  assert np.array_equal(im[184*2:188*2,x0*2:x1*2],base[184*2:188*2,x0*2:x1*2]), 'rendered sole drift'
report['rendered_sole_strips_unchanged']=True
(P/'docs'/'pixel-report.json').write_text(json.dumps(report,indent=2)+'\n')
subprocess.run([sys.executable,str(root/'skills/2d/skin-weights/scripts/motion_qa.py'),str(P/'docs/trace.json'),'--out',str(P/'docs/motion-qa.json'),'--still','lboot,rboot'],check=True)
