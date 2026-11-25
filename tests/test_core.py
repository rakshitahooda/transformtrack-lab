import unittest
import numpy as np
from core import Instance, build_demo, infer_transition, make_mask

class TrackerTests(unittest.TestCase):
    def test_demo_exercises_one_split_and_merge(self):
        d=build_demo()
        self.assertEqual(d['summary']['splits'],1)
        self.assertEqual(d['summary']['merges'],1)
        self.assertEqual([e['kind'] for e in d['events']],['split','merge'])

    def test_split_iou_is_mean_pair_iou(self):
        old=np.zeros((10,10),bool);old[2:8,2:8]=1
        a=np.zeros_like(old);a[2:8,2:5]=1
        b=np.zeros_like(old);b[2:8,5:8]=1
        e=infer_transition([Instance('whole','whole',old)],[Instance('a','a',a),Instance('b','b',b)])
        self.assertEqual(e[0]['kind'],'split')
        self.assertEqual(e[0]['score'],0.5)

    def test_merge_overlap(self):
        a=np.zeros((10,10),bool);a[2:8,2:5]=1
        b=np.zeros_like(a);b[2:8,5:8]=1
        e=infer_transition([Instance('a','a',a),Instance('b','b',b)],[Instance('whole','whole',a|b)])
        self.assertEqual(e[0]['kind'],'merge')
        self.assertEqual(len(e[0]['from']),2)

    def test_demo_has_temporal_track_ids_and_branch_alternatives(self):
        d=build_demo();states=d['states']
        self.assertEqual([o['id'] for o in states[0]['objects']],['T01'])
        self.assertEqual({o['id'] for o in states[3]['objects']},{'T01','T02'})
        self.assertEqual([o['id'] for o in states[7]['objects']],['T03'])
        branches=d['graph']['branches']
        self.assertEqual(sum(b['kind']=='split' and b['selected'] for b in branches),1)
        self.assertEqual(sum(b['kind']=='merge' and b['selected'] for b in branches),1)
        self.assertEqual(sum(not b['selected'] for b in branches),2)
        self.assertTrue(all(n['x'] is not None and n['y'] is not None for n in d['graph']['nodes']))

    def test_event_evidence_names_linked_tracks(self):
        d=build_demo()
        split=next(e for e in d['events'] if e['kind']=='split')
        self.assertEqual({x['to'] for x in split['evidence']},{'T01','T02'})
        self.assertTrue(all(x['pixels']>0 and 0<=x['iou']<=1 for x in split['evidence']))

    def test_masks(self):
        self.assertEqual(set(np.unique(make_mask(0))),{0,1})
        self.assertEqual(set(np.unique(make_mask(4))),{0,1})
        self.assertEqual(len(np.unique(make_mask(4))),2)

    def test_bad_frame(self):
        with self.assertRaises(ValueError):make_mask(8)

if __name__=='__main__':unittest.main()
