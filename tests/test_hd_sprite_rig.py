"""Synthetic rigid-source baking tests, not character-art acceptance."""
import importlib.util,json,math,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('rig_baker',ROOT/'skills/2d/hd-sprite-sequence/scripts/bake_rig.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
class RigTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  for name,color,size in [('head','#dd9977',(24,24)),('arm','#2277aa',(12,36))]:
   im=Image.new('RGBA',size);d=ImageDraw.Draw(im);d.rectangle((2,2,size[0]-3,size[1]-3),fill=color)
   if name=='head':d.point((14,9),fill='black');d.point((18,10),fill='white')
   im.save(self.root/(name+'.png'))
  self.rig=dict(schema='ogs.locked-sprite-rig/1',canvas=dict(size=[128,112],pivot=[64,80],density=4),logical_tick_hz=60,nodes=dict(root=dict(parent=None,offset=[0,0]),head=dict(parent='root',offset=[0,-36]),arm=dict(parent='root',offset=[-14,-20]),hand=dict(parent='arm',offset=[0,9])),parts={name:dict(image=name+'.png',sha256=h.sha(self.root/(name+'.png')),density=4,pivot=[12,12]if name=='head'else[6,4],scale=1,node=name)for name in ['head','arm']},frames=dict(a=dict(angles={'arm':-30}),b=dict(angles={'arm':30})),clips=dict(idle=dict(frames=['a','b'],ticks=[6,6],loop=True)))
 def run_bake(self):
  p=self.root/'rig.json';p.write_text(json.dumps(self.rig));return h.bake(self.root,p,self.root/'baked')
 def test_exact_same_face_pixels_across_arm_motion(self):
  r=self.run_bake();a=Image.open(self.root/'baked/a.png');b=Image.open(self.root/'baked/b.png');box=(240,160,272,192);self.assertEqual(a.crop(box).tobytes(),b.crop(box).tobytes());self.assertNotEqual(a.tobytes(),b.tobytes());self.assertEqual(r['status'],'baked-not-accepted')
 def test_fixed_bone_lengths_while_joint_rotates(self):
  r=self.run_bake()
  for f in r['frames'].values():self.assertAlmostEqual(math.dist(f['nodes']['arm']['position'],f['nodes']['hand']['position']),9)
 def test_frame_scale_is_rejected_before_any_output(self):
  self.rig['frames']['b']['scale']=1.1
  with self.assertRaises(ValueError):self.run_bake()
  self.assertFalse((self.root/'baked').exists())
 def test_different_face_image_per_frame_is_rejected(self):
  self.rig['frames']['b']['image']='other-face.png'
  with self.assertRaises(ValueError):self.run_bake()
 def test_source_part_tampering_rejected(self):
  (self.root/'head.png').write_bytes(b'changed')
  with self.assertRaises(ValueError):self.run_bake()
 def test_fixed_canvas_clipping_rejected(self):
  self.rig['frames']['b']['root']=[200,0]
  with self.assertRaises(ValueError):self.run_bake()
 def test_cycle_rejected(self):
  self.rig['nodes']['root']['parent']='hand'
  with self.assertRaises(ValueError):self.run_bake()
 def test_previous_output_is_preserved(self):
  self.run_bake()
  with self.assertRaises(ValueError):self.run_bake()
 def test_existing_renderer_offset_is_baked_once(self):
  self.rig['frames']['a']['consumer_offset']=[-2,-16];r=self.run_bake();p=r['frames']['a']['nodes']['head'];self.assertEqual(p['actor_position'],[0,-36]);self.assertEqual(p['position'],[2,-20])
 def test_bind_and_mirror_are_fixed_source_transforms(self):
  self.rig['parts']['arm']['bind_angle']=20;self.rig['parts']['arm']['mirror_x']=True;r=self.run_bake();part=next(p for p in r['parts']if p['part']=='arm');self.assertEqual(part['fixed_bind_angle'],20);self.assertTrue(part['fixed_mirror_x'])
 def test_timeline_keeps_authored_ticks(self):
  r=self.run_bake();self.assertEqual(r['clips']['idle']['ticks'],[6,6]);self.assertEqual(r['logical_tick_hz'],60)
if __name__=='__main__':unittest.main()
