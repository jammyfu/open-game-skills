from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
P=Path(__file__).parent;A=P/'assets'
source=Image.open(A/'parts-source.png').convert('RGBA')
atlas=source.resize((256,128),Image.Resampling.NEAREST)
a=np.array(atlas);a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0]=0
atlas=Image.fromarray(a);atlas.save(A/'atlas.png')
names=['head','torso','upper','forearm','thigh','shin','boot','scarf'];out={}
for i,name in enumerate(names):
 box=(i%4*64,i//4*64,i%4*64+64,i//4*64+64);part=atlas.crop(box);bounds=part.getbbox();assert bounds
 part=part.crop(bounds);part.save(A/(name+'.png'))
 out[name]={'cell':box,'bounds':bounds,'size':part.size,'sha256':hashlib.sha256((A/(name+'.png')).read_bytes()).hexdigest()}
 print(name,part.size)
Image.open(P.parent/'lantern-grove/assets/grove-source.png').resize((480,270),Image.Resampling.NEAREST).save(A/'grove.png')
(A/'parts.json').write_text(json.dumps(out,indent=2)+'\n')

# Exact source paint ownership uses the normalized atlas, not the raw GPT master.
owners=np.zeros((128,256),np.uint16);parts=[]
def pinned(name):return {'path':name,'sha256':hashlib.sha256((A/name).read_bytes()).hexdigest()}
for i,name in enumerate(names):
 x0,y0,x1,y1=out[name]['cell'];b=out[name]['bounds'];mask=a[y0:y1,x0:x1,3]>0;owners[y0:y1,x0:x1][mask]=i+1
 parts.append({'id':name,'ownerId':i+1,'bounds':[x0+b[0],y0+b[1],x0+b[2],y0+b[3]],'image':pinned(name+'.png')})
Image.fromarray(owners).save(A/'owners.png')
(A/'ownership.json').write_text(json.dumps({'schema':'ogs.attachment-ownership/1','atlas':pinned('atlas.png'),'ownership':pinned('owners.png'),'parts':parts},indent=2)+'\n')
