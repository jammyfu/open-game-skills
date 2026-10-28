import math
import unittest
from bind_joint import bind_pair


class BindTests(unittest.TestCase):
    def setUp(self):
        self.bones=[dict(name='upper',world=[1,0,0,1,0,0]),dict(name='lower',world=[0,-1,1,0,5,0])]
        self.envelope=dict(origin=[0,0],axis=[1,0],start=3,end=7)

    def test_midpoint_has_normalized_named_weights(self):
        weights=bind_pair([5,2],self.bones,self.envelope)
        self.assertEqual([(b['bone'],b['weight']) for b in weights],[('upper',.5),('lower',.5)])

    def test_setup_reconstruction_with_rotated_child(self):
        for point in [[1,2],[3,0],[4,3],[5,2],[6,-1],[8,2]]:
            reconstructed=[0.,0.]
            for binding in bind_pair(point,self.bones,self.envelope):
                bone=next(b for b in self.bones if b['name']==binding['bone'])
                a,b,c,d,x,y=bone['world'];lx,ly,w=binding['x'],binding['y'],binding['weight']
                reconstructed[0]+=(a*lx+b*ly+x)*w;reconstructed[1]+=(c*lx+d*ly+y)*w
            self.assertAlmostEqual(math.dist(point,reconstructed),0,places=12)

    def test_rigid_regions_do_not_gain_other_bone_weights(self):
        self.assertEqual(bind_pair([1,2],self.bones,self.envelope)[0]['bone'],'upper')
        self.assertEqual(len(bind_pair([1,2],self.bones,self.envelope)),1)
        self.assertEqual(bind_pair([9,2],self.bones,self.envelope)[0]['bone'],'lower')

    def test_axis_magnitude_does_not_change_physical_envelope(self):
        self.assertEqual(bind_pair([4,2],self.bones,self.envelope),bind_pair([4,2],self.bones,{**self.envelope,'axis':[4,0]}))

    def test_invalid_envelope_refused(self):
        for edit in [dict(axis=[0,0]),dict(end=3),dict(start=8)]:
            with self.assertRaises(ValueError):bind_pair([5,2],self.bones,{**self.envelope,**edit})

    def test_singular_setup_refused_even_outside_influence(self):
        self.bones[1]['world']=[0,0,0,0,0,0]
        with self.assertRaises(ValueError):bind_pair([1,2],self.bones,self.envelope)

    def test_duplicate_names_refused(self):
        self.bones[1]['name']='upper'
        with self.assertRaises(ValueError):bind_pair([5,2],self.bones,self.envelope)


if __name__=='__main__':unittest.main(verbosity=2)
