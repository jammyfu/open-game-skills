"""Create a lossless APNG and integer-scale storyboard from captured browser PNGs."""
from pathlib import Path
import sys
from PIL import Image
P=Path(__file__).parent;source=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/pixel-rig-frames')
frames=[Image.open(source/f'scene-{i:03}.png').convert('RGBA').resize((480,270),Image.Resampling.NEAREST) for i in range(48)]
frames[0].save(P/'docs/rig-lossless.png',save_all=True,append_images=frames[1:],duration=[83,83,84]*16,loop=0)
board=Image.new('RGBA',(960,540))
for i,n in enumerate([0,10,24,36]):board.paste(frames[n],((i%2)*480,(i//2)*270))
board.save(P/'docs/sequence.png')
with Image.open(P/'docs/rig-lossless.png') as result:
 assert result.n_frames==48
 for i in range(48):
  result.seek(i);assert result.convert('RGBA').tobytes()==frames[i].tobytes()
print('48 lossless browser frames verified; duration 4 seconds')
