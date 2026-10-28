"""Anonymous overlapping-bound fixtures: exact rectangle copies can be wrong exports."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
from PIL import Image

from audit_attachment_ownership import audit


class OwnershipTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name).resolve()
        atlas=np.zeros((8,9,4),np.uint8);owners=np.zeros((8,9),np.uint16)
        owners[1,1:6]=1;owners[1:6,1]=1
        owners[4,3:7]=2;owners[2:5,6]=2
        atlas[owners==1]=[44,88,190,253];atlas[owners==2]=[220,164,230,252]
        self.atlas=atlas;self.owners=owners
        self.data={'schema':'ogs.attachment-ownership/1','atlas':self.save('atlas.png',atlas),'ownership':self.save('owners.png',owners),'parts':[]}
        for name,owner,bounds in [('near',1,[1,1,6,6]),('far',2,[3,2,7,5])]:
            x0,y0,x1,y1=bounds;mask=owners[y0:y1,x0:x1]==owner;pixels=np.where(mask[:,:,None],atlas[y0:y1,x0:x1],0)
            self.data['parts'].append({'id':name,'ownerId':owner,'bounds':bounds,'image':self.save(name+'.png',pixels)})
        self.path=self.root/'contract.json'

    def save(self,name,array):
        path=self.root/name;Image.fromarray(array).save(path)
        return {'path':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

    def run_audit(self):
        self.path.write_text(json.dumps(self.data));return audit(self.path)

    def test_disjoint_sources_with_overlapping_rectangles_pass_only_when_owned(self):
        r=self.run_audit();self.assertEqual(r['status'],'PASS-NATIVE-OWNERSHIP');self.assertFalse(r['artAccepted']);self.assertFalse(r['runtimeValidated'])

    def test_pixel_identical_rectangle_still_fails_foreign_alpha_and_duplicate_coverage(self):
        self.data['parts'][0]['image']=self.save('near.png',self.atlas[1:6,1:6])
        np.testing.assert_array_equal(np.array(Image.open(self.root/'near.png')),self.atlas[1:6,1:6])
        r=self.run_audit();self.assertEqual(r['status'],'FAIL');self.assertEqual(r['parts'][0]['foreignAlphaPixels'],3);self.assertEqual(r['duplicatedSourceCorePixels'],3)

    def test_missing_real_source_pixels_fail(self):
        a=np.array(Image.open(self.root/'near.png'));a[0,0]=0;self.data['parts'][0]['image']=self.save('near.png',a)
        self.assertGreater(self.run_audit()['missingSourceCorePixels'],0)

    def test_low_alpha_foreign_paint_is_not_silently_allowed(self):
        a=np.array(Image.open(self.root/'near.png'));a[2,2]=[255,0,0,1];self.data['parts'][0]['image']=self.save('near.png',a)
        self.assertEqual(self.run_audit()['parts'][0]['foreignAlphaPixels'],1)

    def test_stale_source_bytes_are_rejected(self):
        (self.root/'atlas.png').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'Pinned'):self.run_audit()

    def test_owner_ids_cannot_be_reused(self):
        self.data['parts'][1]['ownerId']=1
        with self.assertRaisesRegex(ValueError,'owner IDs'):self.run_audit()

    def test_unassigned_visible_owner_is_not_ignored(self):
        owners=self.owners.copy();owners[1,1]=3;self.data['ownership']=self.save('owners.png',owners)
        self.assertTrue(any(x['kind']=='unowned-source-core' for x in self.run_audit()['failures']))

    def test_asset_paths_cannot_escape_package(self):
        self.data['atlas']['path']='../elsewhere.png'
        with self.assertRaisesRegex(ValueError,'escapes'):self.run_audit()


if __name__=='__main__':unittest.main()
