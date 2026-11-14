"""Render an original layered pixel fixture; no generated-sheet slicing."""
from pathlib import Path
import math,json
from PIL import Image,ImageDraw
from model import leaf_offset
OUT=Path(__file__).parent/'docs'; OUT.mkdir(exist_ok=True)
W,H=160,120
wood=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(wood)
d.polygon([(73,108),(78,48),(84,48),(88,108)],fill='#775135')
d.line([(80,78),(57,48)],fill='#775135',width=5)
d.line([(83,69),(105,43)],fill='#775135',width=5)
centers=[(55,51),(75,34),(98,46),(43,67),(69,61),(95,65),(115,64)]
clumps=[]
for x,y in centers:
 im=Image.new('RGBA',(W,H)); q=ImageDraw.Draw(im)
 q.polygon([(x-19,y),(x-14,y-13),(x+5,y-18),(x+20,y-6),(x+17,y+10),(x-8,y+15)],fill='#286345')
 q.rectangle((x-11,y-9,x+8,y),fill='#4d9148');q.rectangle((x-5,y-13,x+9,y-7),fill='#8ebd56')
 clumps.append(im)
inside=Image.new('RGBA',(W,H));ImageDraw.Draw(inside).ellipse((35,27,126,83),fill='#183f35')
frames=[]; traces=[]; roots=[]; holes=[]
for n in range(100):
 t=n/10
 strength=3*max(0,math.sin(math.pi*(t-1)/5)) if 1<t<6 else 0
 scene=Image.new('RGBA',(W,H),'#a2bdc1'); ImageDraw.Draw(scene).rectangle((0,108,W,H),fill='#344d40')
 scene.alpha_composite(inside);scene.alpha_composite(wood)
 offsets=[]
 for im,(x,y) in zip(clumps,centers):
  dx,dy=leaf_offset(t,x,strength);offsets.append([dx,dy]);scene.alpha_composite(im,(dx,dy))
 roots.append(scene.crop((70,90,92,109)).tobytes())
 traces.append(offsets); frames.append(scene.convert('RGB').resize((640,480),Image.Resampling.NEAREST))
assert all(r==roots[0] for r in roots),'root moved'
assert frames[0].tobytes()==frames[-1].tobytes(),'calm did not restore'
assert len({f.tobytes() for f in frames})>10,'no visible animation'
frames[0].save(OUT/'wind.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=False)
with Image.open(OUT/'wind.gif') as gif:
 durations=[]
 for i in range(gif.n_frames):
  gif.seek(i);durations.append(gif.info['duration'])
 assert sum(durations)==10000
report={'rendered_frames':100,'logical_size':[W,H],'scale':4,'duration_ms':sum(durations),'distinct_frames':len({f.tobytes() for f in frames}),'root_pixels_unchanged':True,'calm_restored':True,'integer_offsets':all(isinstance(v,int) for f in traces for p in f for v in p),'scope':'Original procedural fixture, not generated art-direction image; Pillow renderer, not game engine.'}
(OUT/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
