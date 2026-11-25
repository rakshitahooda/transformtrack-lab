import unittest
from server import app

class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        r=self.client.get('/health')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json,{'status':'ok','mode':'synthetic-plus-real-footage'})

    def test_home_and_assets(self):
        home=self.client.get('/')
        self.assertEqual(home.status_code,200)
        self.assertIn(b'A branching state graph',home.data)
        self.assertIn(b'ILLUSTRATIVE',home.data)
        self.assertIn(b'A watch repair, captured on camera',home.data)
        self.assertIn(b'No masks, tracks, or measurements are computed on this footage',home.data)
        js=self.client.get('/static/app.js')
        self.assertEqual(js.status_code,200)
        self.assertIn(b'buildGraph',js.data)
        css=self.client.get('/static/style.css')
        self.assertEqual(css.status_code,200)
        js.close();css.close();home.close()

    def test_real_footage_source_and_range(self):
        info=self.client.get('/api/real-footage').get_json()
        self.assertEqual(info['creator'],'Tima Miroshnichenko')
        self.assertTrue(info['notes_are_manual'])
        self.assertFalse(info['computer_vision_runs_on_clip'])
        r=self.client.get('/media/pexels-clock-repair.mp4',headers={'Range':'bytes=0-63'})
        self.assertEqual(r.status_code,206)
        self.assertEqual(r.content_type,'video/mp4')
        self.assertEqual(len(r.data),64)
        r.close()
        demo=self.client.get('/media/transformtrack-demo.mp4',headers={'Range':'bytes=0-63'})
        self.assertEqual(demo.status_code,206)
        self.assertEqual(demo.content_type,'video/mp4')
        self.assertEqual(len(demo.data),64)
        demo.close()

    def test_api_graph_and_explanation(self):
        d=self.client.get('/api/demo').get_json()
        cases={c['id']:c for c in d['scenarios']}
        self.assertEqual(set(cases),{'mug','remote','usb'})
        mug=cases['mug']
        self.assertEqual(mug['summary'],{'frames':8,'events':2,'splits':1,'merges':1})
        self.assertEqual([e['kind'] for e in mug['events']],['split','merge'])
        self.assertTrue(all('iou' in link and 'from' in link and 'to' in link for e in mug['events'] for link in e['evidence']))
        self.assertEqual(len(mug['graph']['nodes']),6)
        self.assertEqual(len([e for e in mug['graph']['edges'] if e['type']=='alternative']),2)
        self.assertEqual(len(mug['graph']['branches']),4)
        self.assertEqual(cases['remote']['states'][2]['objects'][2]['label'],'AAA battery A')
        self.assertEqual(cases['usb']['states'][1]['objects'][1]['label'],'Protective cap')
        for case in cases.values():
            self.assertEqual(len(case['states']),8)
            self.assertTrue(all(o['mask_png'].startswith('data:image/png;base64,') for state in case['states'] for o in state['objects']))
            self.assertTrue(all(e['kind'] in ('split','merge') for e in case['events']))

if __name__=='__main__':unittest.main()
