import unittest
import numpy as np
from core import Instance, build_demo, infer_transition, make_mask
class TrackerTests(unittest.TestCase):
 def test_demo_exercises_one_split_and_merge(self):
  d=build_demo();self.assertEqual(d['summary']['splits'],1);self.assertEqual(d['summary']['merges'],1)
  self.assertEqual([e['kind'] for e in d['events']],['split','merge'])
 def test_split_iou_is_mean_pair_iou(self):
  old=np.zeros((10,10),bool);old[2:8,2:8]=1
  a=np.zeros_like(old);a[2:8,2:5]=1;b=np.zeros_like(old);b[2:8,5:8]=1
  e=infer_transition([Instance('whole','whole',old)],[Instance('a','a',a),Instance('b','b',b)])
  self.assertEqual(e[0]['kind'],'split');self.assertEqual(e[0]['score'],0.5)
 def test_merge_overlap(self):
  a=np.zeros((10,10),bool);a[2:8,2:5]=1;b=np.zeros_like(a);b[2:8,5:8]=1
  e=infer_transition([Instance('a','a',a),Instance('b','b',b)],[Instance('whole','whole',a|b)])
  self.assertEqual(e[0]['kind'],'merge');self.assertEqual(len(e[0]['from']),2)
 def test_masks(self):
  self.assertEqual(set(np.unique(make_mask(0))),{0,1});self.assertEqual(set(np.unique(make_mask(4))),{0,1})
 def test_bad_frame(self):
  with self.assertRaises(ValueError):make_mask(8)
if __name__=='__main__':unittest.main()
