"""Verify actual Godot capture traces and decoded outputs; no gameplay emulation."""
from pathlib import Path
import json,hashlib,wave,sys
import numpy as np
from PIL import Image,ImageDraw
D=Path(__file__).parent/'docs'
A=json.loads((D/'capture-trace.json').read_text());B=json.loads((D/'reduced-trace.json').read_text())
assert len(A)==len(B)==600
assert [r['logical'] for r in A]==[r['logical'] for r in B]
assert all(r['optional_particles']==0 for r in B)
assert any(r['optional_particles']>0 for r in A)
assert A[-1]['state']=='won' and A[-1]['score']==9
assert any(r['state']=='lost' for r in A)
assert A[260]['state']=='ready' and A[260]['score']==0
assert all(r['world_clock']==i+1 for i,r in enumerate(A))
assert any(r['pose_hold']>0 for r in A)
assert all(A[i+1]['world_clock']==A[i]['world_clock']+1 for i in range(599) if A[i]['pose_hold']>0)
source=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/tmp/lantern-capture')
files=sorted(source.glob('frame*.png')); assert len(files)==600
with wave.open(str(source/'frame.wav'),'rb') as audio:
 sound=np.frombuffer(audio.readframes(audio.getnframes()),dtype='<i2')
 assert np.max(np.abs(sound.astype(np.int32)))>0,'silent capture'
 audio_seconds=audio.getnframes()/audio.getframerate()
 assert abs(audio_seconds-10)<.1
for name in ['gameplay.gif','reduced.gif']:
 with Image.open(D/name) as gif:
  duration=0
  for i in range(gif.n_frames):gif.seek(i);duration+=gif.info['duration']
  assert abs(duration-10000)<100
board=Image.new('RGB',(1280,774),'#101f32');q=ImageDraw.Draw(board)
for idx,n in enumerate([20,138,241,261,438,560]):
 im=Image.open(files[n-1]); im.thumbnail((640,360));x=(idx%2)*640;y=(idx//2)*258
 im=im.resize((448,252),Image.Resampling.NEAREST)
 board.paste(im,(x+96,y))
 q.text((x+5,y+5),f'TICK {n}',fill='white')
board.save(D/'sequence.png')
report={'driver':'Godot Movie Maker actual frame+WAV capture','engine':'4.7.1-stable','frames_per_mode':600,'logical_rate':60,'seconds':10,'normal_reduced_logical_traces_equal':True,'reduced_optional_particles':0,'retry_resets_in_one_tick':True,'actor_pose_accent_does_not_stop_world':True,'score':9,'goal':8,'outcome':'won','audio_nonzero':True,'audio_seconds':audio_seconds,'gif_duration_checked':True,'source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.gd')},'evidence_class':'scripted engine integration, not human playtest or live-frame pacing benchmark'}
(D/'engine-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
