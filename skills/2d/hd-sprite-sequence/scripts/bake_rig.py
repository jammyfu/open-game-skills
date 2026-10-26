#!/usr/bin/env python3
"""Bake fixed approved sprite parts with rigid transforms; never redraw faces.

This is an offline sprite source compositor, not a game animation controller.
It deliberately has no per-frame scale, deformation, image replacement or
interpolated timeline. Numerical rig success is not visual/art acceptance.
"""
from __future__ import annotations
import argparse,hashlib,io,json,math,re,sys
from pathlib import Path
from PIL import Image

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def finite(x):
 if type(x)not in(int,float)or not math.isfinite(x):raise ValueError('finite number required')
 return float(x)
def pair(p):
 if not isinstance(p,list)or len(p)!=2:raise ValueError('[x,y] required')
 return [finite(x)for x in p]
def rotate(p,angle):
 a=math.radians(angle);return[p[0]*math.cos(a)-p[1]*math.sin(a),p[0]*math.sin(a)+p[1]*math.cos(a)]
def bake(root,recipe,out):
 root,recipe,out=map(lambda p:Path(p).resolve(),(root,recipe,out));recipe_bytes=recipe.read_bytes();rig=json.loads(recipe_bytes)
 if rig['schema']!='ogs.locked-sprite-rig/1':raise ValueError('unsupported rig schema')
 if out==root or out in root.parents or out in recipe.parents:raise ValueError('output may not contain source inputs')
 if out.exists()and any(out.iterdir()):raise ValueError('use a new empty output directory; previous source art is preserved')
 c=rig['canvas'];size=pair(c['size']);pivot=pair(c['pivot']);density=finite(c['density']);hz=finite(rig['logical_tick_hz'])
 if density<=0 or hz<=0 or any(x<=0 or x!=int(x)for x in size)or any(x*density!=int(x*density)for x in size)or any(p<0 or p>s for p,s in zip(pivot,size)):raise ValueError('invalid canvas/density/clock')
 nodes=rig['nodes'];parts=rig['parts'];frames=rig['frames'];clips=rig['clips']
 if not nodes or not parts or not frames or not clips:raise ValueError('nonempty rig and authored clips required')
 for name,node in nodes.items():
  if set(node)-{'parent','offset'}or node.get('parent')not in [None,*nodes]:raise ValueError('invalid rig node '+name)
  pair(node['offset'])
 images={};proof=[]
 for name,part in parts.items():
  if set(part)-{'image','sha256','density','pivot','scale','node','bind_angle','mirror_x'}:raise ValueError('unsupported part transform; no deformation allowed')
  p=(root/part['image']).resolve()
  if not p.is_relative_to(root)or p==out or out in p.parents:raise ValueError('part path leaves source root or enters output')
  image_bytes=p.read_bytes()
  if hashlib.sha256(image_bytes).hexdigest()!=part['sha256']:raise ValueError('source part changed: '+name)
  if part['node']not in nodes:raise ValueError('unknown attachment node')
  pd=finite(part['density']);scale=finite(part.get('scale',1));pp=pair(part['pivot'])
  if pd<=0 or scale<=0:raise ValueError('positive fixed part scale/density required')
  with Image.open(io.BytesIO(image_bytes))as opened:opened.load();im=opened.convert('RGBA')
  if not im.getbbox()or im.getchannel('A').getextrema()[0]!=0:raise ValueError('nonempty transparent source part required')
  if any(v<0 or v>bound for v,bound in zip(pp,im.size)):raise ValueError('part pivot outside source image')
  if type(part.get('mirror_x',False))is not bool:raise ValueError('fixed mirror_x must be boolean')
  if part.get('mirror_x',False):im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT);pp[0]=im.width-pp[0]
  factor=density/pd*scale;im=im.resize((max(1,round(im.width*factor)),max(1,round(im.height*factor))),Image.Resampling.LANCZOS)
  pp=[v*factor for v in pp];radius=math.ceil(max(math.dist(pp,corner)for corner in [(0,0),(im.width,0),(0,im.height),im.size]))+3
  tile=Image.new('RGBA',(radius*2,radius*2));tile.alpha_composite(im,(round(radius-pp[0]),round(radius-pp[1])))
  images[name]=(tile,radius,finite(part.get('bind_angle',0)));proof.append(dict(part=name,sha256=part['sha256'],fixed_scale=scale,source_density=pd,fixed_bind_angle=finite(part.get('bind_angle',0)),fixed_mirror_x=part.get('mirror_x',False)))
 used=set()
 for clip in clips.values():
  if not isinstance(clip['loop'],bool)or len(clip['frames'])!=len(clip['ticks'])or not clip['frames']or any(type(t)is not int or t<=0 for t in clip['ticks']):raise ValueError('invalid authored timeline')
  if any(fid not in frames for fid in clip['frames']):raise ValueError('clip references missing pose')
  used.update(clip['frames'])
 if used!=set(frames):raise ValueError('every frame must have an authored clip')
 output={};metadata={}
 for fid,frame in frames.items():
  if not re.fullmatch(r'[a-zA-Z0-9_-]+',fid):raise ValueError('unsafe frame ID')
  if set(frame)-{'angles','root','order','consumer_offset'}:raise ValueError('per-frame scale/image/deformation is forbidden')
  angles={k:finite(v)for k,v in frame['angles'].items()};consumer=pair(frame.get('consumer_offset',[0,0]));authored_root=pair(frame.get('root',[0,0]));offset=[authored_root[i]-consumer[i]for i in(0,1)]
  if not set(angles).issubset(nodes):raise ValueError('unknown animated node')
  order=frame.get('order',list(parts))
  if len(order)!=len(parts)or set(order)!=set(parts):raise ValueError('draw order must include every fixed part once')
  poses={};visiting=set()
  def pose(name):
   if name in poses:return poses[name]
   if name in visiting:raise ValueError('cyclic rig')
   visiting.add(name);node=nodes[name];parent=node.get('parent')
   if parent is None:xy=offset;angle=0
   else:xy,angle=pose(parent)
   delta=rotate(pair(node['offset']),angle);result=([xy[i]+delta[i]for i in(0,1)],angle+angles.get(name,0));poses[name]=result;visiting.remove(name);return result
  for name in nodes:pose(name)
  canvas=Image.new('RGBA',(int(size[0]*density),int(size[1]*density)))
  for name in order:
   part=parts[name];xy,angle=poses[part['node']];tile,radius,bind_angle=images[name];angle+=bind_angle
   # Same part pixels, fixed scale, only rotation and translation per pose.
   rotated=tile if angle%360==0 else tile.rotate(-angle,resample=Image.Resampling.BICUBIC)
   x,y=[round((xy[i]+pivot[i])*density-radius)for i in(0,1)];bb=rotated.getbbox()
   if bb and(x+bb[0]<0 or y+bb[1]<0 or x+bb[2]>canvas.width or y+bb[3]>canvas.height):raise ValueError('part clipped by fixed source canvas: '+fid+'/'+name)
   canvas.alpha_composite(rotated,(x,y))
  output[fid]=canvas;metadata[fid]=dict(file=fid+'.png',source_size=size,pivot=pivot,density=density,consumer_offset=consumer,nodes={k:dict(position=p[0],actor_position=[p[0][i]+consumer[i]for i in(0,1)],angle=p[1])for k,p in poses.items()})
 # Validate everything before writing the first output frame.
 out.mkdir(parents=True,exist_ok=True)
 for fid,im in output.items():im.save(out/(fid+'.png'));metadata[fid]['sha256']=sha(out/(fid+'.png'))
 report=dict(schema='ogs.locked-sprite-bake/1',status='baked-not-accepted',scope='rigid source-part geometry; independent visual/identity/sequence review still required',recipe_sha256=hashlib.sha256(recipe_bytes).hexdigest(),baker_sha256=sha(Path(__file__)),parts=proof,frames=metadata,clips=clips,logical_tick_hz=hz)
 (out/'bake.json').write_text(json.dumps(report,indent=2)+'\n');return report

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for key in ['root','rig','out']:p.add_argument('--'+key,required=True)
 a=p.parse_args()
 try:r=bake(a.root,Path(a.root)/a.rig,a.out)
 except(ValueError,KeyError,TypeError,OSError)as e:print(json.dumps(dict(status='blocked',error=str(e))));return 2
 print(json.dumps(dict(status=r['status'],frames=len(r['frames']))));return 0
if __name__=='__main__':sys.exit(main())
