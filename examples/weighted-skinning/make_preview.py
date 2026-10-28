"""Compose actual renderer frames into a readable common-camera case preview."""
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont
import json
import numpy as np

root=Path(sys.argv[1]);frames=[]
source=Path(__file__).resolve().parent/'source'
rig=json.loads((source/'current.rig.json').read_text());mesh=rig['skins']['default']['arm']['arm']
with Image.open(source/'arm-setup.png') as asset:alpha=np.array(asset.getchannel('A'));width,height=asset.size
uv=np.array(mesh['uvs']).reshape(-1,2)*[width,height];ink=[]
for triangle in np.array(mesh['triangles']).reshape(-1,3):
    points=uv[triangle];x0,y0=np.floor(points.min(0)).astype(int);x1,y1=np.ceil(points.max(0)).astype(int)+1
    x0,y0=max(0,x0),max(0,y0);x1,y1=min(width,x1),min(height,y1)
    if x1<=x0 or y1<=y0:ink.append(False);continue
    mask=Image.new('L',(x1-x0,y1-y0));ImageDraw.Draw(mask).polygon([(float(x-x0),float(y-y0))for x,y in points],fill=255)
    ink.append(bool(((np.array(mask)>0)&(alpha[y0:y1,x0:x1]>32)).any()))
(Path(sys.argv[2]).parent/'ink-triangles.json').write_text(json.dumps(ink)+'\n')
font=ImageFont.load_default(size=31);small=ImageFont.load_default(size=22);label=ImageFont.load_default(size=25)
for index in list(range(12,24))+list(range(12)):
    canvas=Image.new('RGB',(1280,740),'#101827');d=ImageDraw.Draw(canvas)
    d.text((32,26),'Catch broken skinning before it ships.',font=font,fill='#f2f6ff')
    d.text((32,78),'Same source. Same bones. Different weights. Real pixel-aware checks.',font=small,fill='#a7b6cc')
    for name,x,color,title,caption in [('narrow',28,'#ff8d8d','NARROW ENVELOPE / FAIL','2,529 visible pixels in folded triangles'),('current',652,'#87e5b7','REVISED ENVELOPE / PASS','0 visible pixels in folded triangles')]:
        d.rounded_rectangle((x,135,x+600,695),radius=15,fill='#202d40')
        d.text((x+20,153),title,font=label,fill=color)
        image=Image.open(root/(name+'-render')/'bend'/f'f{index:04}.png').convert('RGB')
        image.thumbnail((560,470),Image.Resampling.LANCZOS)
        canvas.paste(image,(x+(600-image.width)//2,202+(470-image.height)//2))
        d.text((x+18,705),caption,font=small,fill=color)
    frames.append(canvas)
frames[0].save(sys.argv[2],save_all=True,append_images=frames[1:],duration=[83,83,84]*8,loop=0,quality=85)
frames[0].save(sys.argv[3],save_all=True,append_images=frames[1:],duration=[80,80,90]*8,loop=0,optimize=False)
