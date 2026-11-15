"""GPT asset -> native-grid layers -> actual animation and evidence. Pillow + numpy."""
from pathlib import Path
import json, math, colorsys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from model import leaf_offset
D=Path(__file__).parent/'docs'; L=D/'layers'; L.mkdir(exist_ok=True)
N=128
source=Image.open(D/'gpt-tree-source.png').convert('RGBA')
a=np.array(source.resize((N,N),Image.Resampling.NEAREST));a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0]=0
native=Image.fromarray(a);native.save(L/'native.png')
solid=a[:,:,3]>0
leaf=solid & (a[:,:,1].astype(int)>a[:,:,0].astype(int)*1.05) & (a[:,:,1]>a[:,:,2])
# Artist-selected centers after inspecting GPT source; this is NOT automatic watershed.
seeds=[(35,29),(63,23),(89,29),(27,49),(62,45),(98,49),(29,69),(63,65),(96,69)]
y,x=np.indices((N,N)); dist=np.stack([(x-sx)**2+(y-sy)**2 for sx,sy in seeds]); labels=np.argmin(dist,axis=0)
def layer(mask):
 b=a.copy();b[~mask]=0;return Image.fromarray(b)
wood=layer(solid & ~leaf);wood.save(L/'wood.png')
clumps=[layer(leaf & (labels==i)) for i in range(len(seeds))]
for i,im in enumerate(clumps):im.save(L/f'leaf-{i:02d}.png')
# Static opaque dark interior preserves every original silhouette pixel under foliage.
inside=layer(leaf);b=np.array(inside);b[:,:,:3]=(b[:,:,:3]*.55).astype('uint8');inside=Image.fromarray(b);inside.save(L/'inside.png')
def stack(offsets):
 out=inside.copy();out.alpha_composite(wood)
 for im,(dx,dy) in zip(clumps,offsets):out.alpha_composite(im,(dx,dy))
 return out
assert stack([(0,0)]*9).tobytes()==native.tobytes()
colors=[tuple(round(v*255) for v in colorsys.hsv_to_rgb(i/9,.7,.9)) for i in range(9)]
seg=np.zeros_like(a)
for i,c in enumerate(colors):seg[leaf & (labels==i)]=(*c,255)
seg=Image.fromarray(seg);seg.alpha_composite(wood)
board=Image.new('RGB',(1024,300),'#15202d'); bd=ImageDraw.Draw(board)
for i,(im,title) in enumerate([(native,'GPT -> native 128px'),(wood,'Fixed wood'),(inside,'Dark seam coverage'),(seg,'9 assigned leaf groups')]):
 board.paste(im.resize((256,256),Image.Resampling.NEAREST),(i*256,30),im.resize((256,256),Image.Resampling.NEAREST));bd.text((i*256+8,8),title,fill='white')
board.save(D/'gpt-layers.png')
frames=[]; debug=[];trace=[]; hole_count=0;root_errors=0;max_move=0
lean=velocity=0.;previous_t=0
for n in range(120):
 t=n/10
 # Finite traveling gust; explicit calm outside support.
 def gust(px,tm):
  z=(px-(tm-1)*65)/75
  return (1-z*z)**2 if abs(z)<1 else 0.
 # Fixed 120Hz spring, independent from presentation sample rate.
 for j in range(12):
  tm=previous_t+j/120
  force=gust(64,tm)*1.8
  velocity+=(25*(force-lean)-7*velocity)/120;lean+=velocity/120
 previous_t=t+.1
 offsets=[]
 for sx,sy in seeds:
  edge=.35+.65*min(1,math.hypot(sx-64,sy-50)/43)
  dx,dy=leaf_offset(t,sx,2.5*gust(sx,t),edge)
  offsets.append((dx+round(lean*edge),dy))
 for part,(dx,dy) in zip(clumps,offsets):
  bx,by,ex,ey=part.getbbox()
  assert 0 <= bx+dx < ex+dx <= N and 0 <= by+dy < ey+dy <= N, 'clipped leaf'
 im=stack(offsets); arr=np.array(im)
 hole_count+=int(np.count_nonzero(solid & (arr[:,:,3]==0)))
 root_errors+=int(np.count_nonzero(arr[92:]!=a[92:]))
 max_move=max(max_move,max(abs(v) for pair in offsets for v in pair))
 trace.append({'t':t,'gust':round(gust(64,t),4),'lean':round(lean,4),'offsets':offsets})
 scene=Image.new('RGBA',(160,152),'#a7c6cf');q=ImageDraw.Draw(scene);q.rectangle((0,136,160,152),fill='#354c36');scene.alpha_composite(im,(16,8))
 q.text((5,140),f't={t:04.1f}s  '+('GUST' if gust(64,t)>.01 else 'CALM'),fill='white')
 frames.append(scene.convert('RGB').resize((640,608),Image.Resampling.NEAREST))
 db=scene.copy();q=ImageDraw.Draw(db)
 for i,((sx,sy),(dx,dy)) in enumerate(zip(seeds,offsets)):
  q.line((sx+16,sy+8,sx+16+dx*4,sy+8+dy*4),fill='red',width=1);q.text((sx+16,sy+8),str(i),fill='white')
 q.line((int((t-1)*65)+16,0,int((t-1)*65)+16,135),fill='#ffdf50',width=1)
 debug.append(db.convert('RGB').resize((640,608),Image.Resampling.NEAREST))
assert hole_count==0 and root_errors==0
assert stack(trace[-1]['offsets']).tobytes()==native.tobytes()
assert len({f.tobytes() for f in [stack(v['offsets']) for v in trace]})>10
for name,seq in [('gpt-wind.gif',frames),('gpt-debug.gif',debug)]:
 seq[0].save(D/name,save_all=True,append_images=seq[1:],duration=100,loop=0,optimize=False)
 with Image.open(D/name) as gif:
  total=0
  for k in range(gif.n_frames):gif.seek(k);total+=gif.info['duration']
  assert total==12000
# Exact pixel-grid replication and a negative control using linear resampling.
r=np.array(native.resize((512,512),Image.Resampling.NEAREST));expected=np.repeat(np.repeat(a,4,axis=0),4,axis=1)
assert np.array_equal(r,expected)
assert not np.array_equal(np.array(native.resize((512,512),Image.Resampling.BILINEAR)),expected)
# Haze comparison uses the actual normalized GPT tree, retaining alpha.
hazy=a.copy();hazy[:,:,:3]=np.rint(a[:,:,:3]*.35+np.array([167,198,207])*.65).astype('uint8'); assert np.array_equal(hazy[:,:,3],a[:,:,3])
compare=Image.new('RGB',(768,290),'#a7c6cf');q=ImageDraw.Draw(compare)
for i,(im,title) in enumerate([(native,'NEAR: original'),(Image.fromarray(hazy),'FAR: 65% sky blend'),(native,'PLAY AREA: unchanged')]):
 large=im.resize((256,256),Image.Resampling.NEAREST);compare.paste(large,(i*256,30),large);q.text((i*256+5,8),title,fill='#15202d')
compare.save(D/'gpt-depth.png')
report={'source':'gpt-tree-source.png','normalization':'nearest 128x128; binary alpha threshold 128; no claim of native grid in GPT output','leaf_groups':9,'segmentation':'manual centers + nearest-center assignment, green-mask ownership','frames':120,'duration_ms':12000,'root_pixel_errors':root_errors,'uncovered_original_pixels':hole_count,'rest_reconstruction_exact':True,'calm_restored_exact':True,'max_axis_offset_px':max_move,'leaf_bounds_inside_canvas':True,'integer_4x_replication':True,'bilinear_negative_control_rejected':True,'haze_alpha_preserved':True,'limitations':['Static interior preserves silhouette; does not synthesize unseen branches','Pillow rendering; no engine integration','Pixel checks refer to normalized input, not raw GPT source']}
(D/'gpt-report.json').write_text(json.dumps(report,indent=2)+'\n');(D/'gpt-trace.json').write_text(json.dumps(trace)+'\n');print(json.dumps(report,indent=2))
