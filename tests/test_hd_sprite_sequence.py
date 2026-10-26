"""Synthetic asset-harness behavior tests; no model, engine or user study claims."""
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'skills/2d/hd-sprite-sequence/scripts/validate_sequence.py'
spec=importlib.util.spec_from_file_location('hd_sequence',SCRIPT);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)

def dump(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def fixture(root):
    points={'crown':[0,-60],'chin':[0,-50],'head_left':[-5,-55],'head_right':[5,-55],'cheek_left':[-3,-54],'cheek_right':[3,-54],'brow':[0,-57],'neck':[0,-48],'hip':[0,-28],'shoulder_left':[-8,-46],'shoulder_right':[8,-46],'elbow':[-12,-36],'wrist':[-8,-26],'knee':[-5,-14],'ankle':[-6,0]}
    segments={'head_height':['crown','chin'],'head_width':['head_left','head_right'],'face_width':['cheek_left','cheek_right'],'face_height':['brow','chin'],'torso':['neck','hip'],'shoulders':['shoulder_left','shoulder_right'],'upper_arm':['shoulder_left','elbow'],'forearm':['elbow','wrist'],'thigh':['hip','knee'],'calf':['knee','ankle']}
    lengths={k:math.dist(points[a],points[b])for k,(a,b)in segments.items()}
    def art(path):
        im=Image.new('RGBA',(512,448));d=ImageDraw.Draw(im);d.ellipse((236,80,276,120),fill='#eeaa88');d.rectangle((226,128,286,210),fill='#00aa66');d.line((240,210,232,320),fill='#2255aa',width=16);d.line((272,210,280,320),fill='#2255aa',width=16);im.save(path)
    art(root/'model.png');dump(root/'rig.json',points)
    lock={'schema':'ogs.hd-sprite-lock/1','anatomy_scope':'full-body','logical_tick_hz':60,'model':{'density':4,'landmarks':{k:[(p[0]+64)*4,(p[1]+80)*4]for k,p in points.items()},'image':'model.png','sha256':digest(root/'model.png'),'review':'approved','reviewer':'synthetic-fixture'},'limits':{'length_rel':.025,'ratio_rel':.025,'position_px':.5,'delta_px':.5},'canvas':{'width':128,'height':112,'pivot':[64,80]},'segments':segments,'lengths':lengths,'ratios':{'face_head':['face_width','head_width'],'head_torso':['head_height','torso']},'frames':{},'clips':{'idle':{'frames':['a','b'],'ticks':[6,6],'loop':True,'track':['neck','ankle']}}}
    obs={'schema':'ogs.hd-sprite-observations/1','lock_sha256':'','build':'synthetic-v1','frames':{}}
    for fid in ['a','b']:
        art(root/(fid+'.png'));asset=digest(root/(fid+'.png'))
        lock['frames'][fid]={'landmarks':copy.deepcopy(points),'projection':{},'occluded':{},'view':'front','reference_evidence':{'path':'rig.json','sha256':digest(root/'rig.json')}}
        obs['frames'][fid]={'image':fid+'.png','sha256':asset,'density':4,'source_size':[128,112],'pivot':[64,80],'trim_offset':[0,0],'landmarks':{k:[(p[0]+64)*4,(p[1]+80)*4]for k,p in points.items()},'review':{'image_sha256':asset,'reviewer':'synthetic-fixture','identity':True,'pose':True,'alpha':True,'temporal':True}}
    dump(root/'lock.json',lock);obs['lock_sha256']=digest(root/'lock.json');dump(root/'observations.json',obs);return lock,obs

class HDSequenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.lock,self.obs=fixture(self.root)
    def run_case(self,update_lock=False):
        if update_lock:dump(self.root/'lock.json',self.lock);self.obs['lock_sha256']=digest(self.root/'lock.json')
        dump(self.root/'observations.json',self.obs)
        return h.validate(self.root,self.root/'lock.json',self.root/'observations.json',self.root/'review')
    def codes(self,r):return {v['code']for v in r['issues']}
    def test_valid_synthetic_sequence_and_visual_evidence(self):
        r=self.run_case();self.assertEqual(r['status'],'pass',r);self.assertEqual(len(r['edges']),2);self.assertTrue((self.root/'review/overlay.png').is_file());self.assertTrue((self.root/'review/clip-0-idle.gif').is_file())
    def test_same_canvas_and_alpha_bounds_but_face_grows(self):
        # The silhouette, PNG size and body bounds remain byte-identical.
        f=self.obs['frames']['b'];f['landmarks']['cheek_left'][0]-=4;f['landmarks']['cheek_right'][0]+=4
        r=self.run_case();self.assertEqual(r['status'],'fail');self.assertIn('anatomy-ratio',self.codes(r))
    def test_head_grows_while_torso_shrinks(self):
        f=self.obs['frames']['b'];f['landmarks']['crown'][1]-=8;f['landmarks']['neck'][1]+=8
        r=self.run_case();self.assertIn('anatomy-length',self.codes(r));self.assertIn('anatomy-ratio',self.codes(r))
    def test_whole_frame_scale_cannot_hide_head_torso_change(self):
        f=self.obs['frames']['b'];f['landmarks']['crown'][1]-=12
        f['landmarks']={k:[256+(p[0]-256)*.9,320+(p[1]-320)*.9]for k,p in f['landmarks'].items()}
        self.assertIn('anatomy-ratio',self.codes(self.run_case()))
    def test_loop_residual_fails_even_with_individually_tolerable_positions(self):
        for fid,delta in [('a',-1.6),('b',1.6)]:
            for p in self.obs['frames'][fid]['landmarks'].values():p[0]+=delta
        r=self.run_case();self.assertNotIn('pose-landmark',self.codes(r));self.assertIn('temporal-residual',self.codes(r));self.assertEqual(len(r['edges']),2)
    def test_authored_root_motion_is_not_jitter(self):
        for p in self.lock['frames']['b']['landmarks'].values():p[0]+=3
        for p in self.obs['frames']['b']['landmarks'].values():p[0]+=12
        self.assertEqual(self.run_case(True)['status'],'pass')
    def test_trim_keeps_source_coordinates(self):
        for fid in self.obs['frames']:
            file=self.root/(fid+'.png');im=Image.open(file).crop((80,40,400,400));im.save(file);f=self.obs['frames'][fid];f['trim_offset']=[20,10];f['landmarks']={k:[p[0]-80,p[1]-40]for k,p in f['landmarks'].items()};f['sha256']=digest(file);f['review']['image_sha256']=digest(file)
        self.assertEqual(self.run_case()['status'],'pass')
    def test_wrong_pivot_fails_even_when_points_recentered(self):
        self.obs['frames']['a']['pivot']=[65,80];self.assertIn('source-geometry',self.codes(self.run_case()))
    def test_resampled_image_invalidates_annotations(self):
        p=self.root/'a.png';im=Image.open(p);im.putpixel((20,20),(255,0,0,255));im.save(p)
        self.assertIn('image-changed',self.codes(self.run_case()));self.assertNotEqual(self.run_case()['status'],'pass')
    def test_stale_visual_review_blocks(self):
        self.obs['frames']['a']['review']['image_sha256']='0'*64;self.assertIn('unreviewed-image',self.codes(self.run_case()))
    def test_missing_face_points_cannot_pass_body_extent(self):
        del self.obs['frames']['b']['landmarks']['cheek_right'];self.assertEqual(self.run_case()['status'],'blocked')
    def test_missing_pose_blocks(self):
        del self.obs['frames']['b'];self.assertIn('missing-frame',self.codes(self.run_case()))
    def test_lock_cannot_resize_reference_head_between_frames(self):
        self.lock['frames']['b']['landmarks']['crown'][1]-=3;self.assertIn('invalid-reference-proportion',self.codes(self.run_case(True)))
    def test_new_lock_invalidates_old_observations(self):
        self.lock['limits']['ratio_rel']=.03;dump(self.root/'lock.json',self.lock);self.assertIn('lock-changed',self.codes(self.run_case()))
    def test_border_clipping_is_independent_failure(self):
        p=self.root/'a.png';im=Image.open(p);im.putpixel((0,20),(255,0,0,255));im.save(p);f=self.obs['frames']['a'];f['sha256']=digest(p);f['review']['image_sha256']=digest(p);self.assertIn('clipped-border',self.codes(self.run_case()))
    def test_nonfinite_and_projection_zoom_rejected(self):
        self.obs['frames']['a']['density']=float('nan');self.assertNotEqual(self.run_case()['status'],'pass')
        self.lock,self.obs=fixture(self.root);self.lock['frames']['a']['projection']['head_width']=1.2;self.assertNotEqual(self.run_case(True)['status'],'pass')
    def test_negative_and_zero_ticks_rejected(self):
        self.lock['clips']['idle']['ticks']=[6,0];self.assertIn('contract-invalid',self.codes(self.run_case(True)))
    def test_image_path_cannot_escape_root(self):
        self.obs['frames']['a']['image']='../secret.png';self.assertIn('frame-evidence-invalid',self.codes(self.run_case()))
    def test_required_frame_not_played_blocks(self):
        self.lock['clips']['idle']['frames']=['a'];self.lock['clips']['idle']['ticks']=[6];self.assertIn('unplayed-frames',self.codes(self.run_case(True)))
    def test_missing_model_measurements_cannot_pass(self):
        del self.lock['model']['landmarks'];self.assertIn('contract-invalid',self.codes(self.run_case(True)))
    def test_canonical_dimensions_must_match_pinned_model(self):
        self.lock['lengths']['head_height']*=1.1;self.assertEqual(self.run_case(True)['status'],'blocked')
    def test_source_pose_bytes_are_pinned(self):
        dump(self.root/'rig.json',{'different':True});self.assertIn('frame-evidence-invalid',self.codes(self.run_case()))
    def test_ratio_cannot_compare_face_to_itself(self):
        self.lock['ratios']['face_head']=['face_width','face_width'];self.assertEqual(self.run_case(True)['status'],'blocked')
    def test_no_invented_default_game_clock(self):
        del self.lock['logical_tick_hz'];self.assertEqual(self.run_case(True)['status'],'blocked')
    def test_nonloop_preview_does_not_add_loop(self):
        self.lock['clips']['idle']['loop']=False;self.assertEqual(self.run_case(True)['status'],'pass')
        with Image.open(self.root/'review/clip-0-idle.gif')as im:self.assertNotIn('loop',im.info)
    def test_cli_pass_fail_and_blocked_exit_codes(self):
        for status,code in [('pass',0),('fail',1),('blocked',2)]:
            self.lock,self.obs=fixture(self.root)
            if status=='fail':self.obs['frames']['b']['landmarks']['cheek_right'][0]+=8
            if status=='blocked':del self.obs['frames']['b']['landmarks']['cheek_right']
            dump(self.root/'observations.json',self.obs)
            p=subprocess.run([sys.executable,str(SCRIPT),'--root',str(self.root),'--lock','lock.json','--observations','observations.json','--out',str(self.root/'cli')],capture_output=True,text=True)
            self.assertEqual(p.returncode,code,p.stdout+p.stderr);self.assertEqual(json.loads(p.stdout)['status'],status)
    def test_unsafe_output_never_overwrites_input(self):
        self.obs['frames']['a']['image']='review/report.json';out=self.root/'review';out.mkdir();image=out/'report.json';image.write_bytes((self.root/'a.png').read_bytes());original=image.read_bytes();self.obs['frames']['a']['sha256']=digest(image)
        self.run_case();self.assertEqual(image.read_bytes(),original)
    def test_report_binds_only_current_artifacts(self):
        r=self.run_case();self.assertEqual(len(r['artifacts']),2)
        for item in r['artifacts']:self.assertEqual(digest(self.root/'review'/item['path']),item['sha256'])
        del self.lock['model']['landmarks'];r=self.run_case(True);self.assertEqual(r['artifacts'],[])
    def test_renderer_step_offset_is_not_lost_at_import(self):
        for point in self.lock['frames']['b']['landmarks'].values():point[0]-=2;point[1]+=1
        self.obs['frames']['b']['render_offset']=[-2,1]
        self.assertEqual(self.run_case(True)['status'],'pass')
        del self.obs['frames']['b']['render_offset']
        self.assertIn('temporal-residual',self.codes(self.run_case()))
    def test_full_body_cannot_omit_legs(self):
        del self.lock['segments']['thigh'];self.assertEqual(self.run_case(True)['status'],'blocked')
    def test_torso_only_scope_is_explicitly_narrower(self):
        self.lock['anatomy_scope']='face-torso';del self.lock['segments']['thigh'];r=self.run_case(True);self.assertEqual(r['status'],'pass');self.assertEqual(r['anatomy_scope'],'face-torso')
    def test_leg_change_affects_head_body_ratio_with_unchanged_face_torso(self):
        self.lock['limits'].update(length_rel=.05,ratio_rel=.01,position_px=1)
        f=self.obs['frames']['b']['landmarks'];hip=f['hip'][:];knee=f['knee'][:];ankle=f['ankle'][:]
        f['knee']=[hip[i]+.97*(knee[i]-hip[i])for i in(0,1)];f['ankle']=[f['knee'][i]+.97*(ankle[i]-knee[i])for i in(0,1)]
        r=self.run_case(True);self.assertIn('head-body-ratio',self.codes(r));self.assertNotIn('anatomy-ratio',self.codes(r))
    def test_null_or_nonstring_reviewers_do_not_accept_art(self):
        for invalid in [None,False,0,{}]:
            self.lock,self.obs=fixture(self.root);self.obs['frames']['a']['review']['reviewer']=invalid;self.assertEqual(self.run_case()['status'],'blocked')
            self.lock,self.obs=fixture(self.root);self.lock['model']['reviewer']=invalid;self.assertEqual(self.run_case(True)['status'],'blocked')
    def test_duplicate_json_key_rejected(self):
        (self.root/'lock.json').write_text('{"schema":1,"schema":2}');self.assertEqual(self.run_case()['status'],'blocked')

if __name__=='__main__':unittest.main()
