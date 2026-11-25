import unittest
from server import app

class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        r=self.client.get('/health')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json,{'status':'ok','mode':'synthetic'})

    def test_home_and_assets(self):
        home=self.client.get('/')
        self.assertEqual(home.status_code,200)
        self.assertIn(b'A branching state graph',home.data)
        self.assertIn(b'ILLUSTRATIVE',home.data)
        self.assertIn(b'Not a reproduction of TIPO',home.data)
        js=self.client.get('/static/app.js')
        self.assertEqual(js.status_code,200)
        self.assertIn(b'buildGraph',js.data)
        css=self.client.get('/static/style.css')
        self.assertEqual(css.status_code,200)
        js.close();css.close();home.close()

    def test_api_graph_and_explanation(self):
        d=self.client.get('/api/demo').get_json()
        self.assertEqual(d['summary'],{'frames':8,'events':2,'splits':1,'merges':1})
        self.assertEqual([e['kind'] for e in d['events']],['split','merge'])
        self.assertTrue(all('iou' in link and 'from' in link and 'to' in link for e in d['events'] for link in e['evidence']))
        self.assertEqual(len(d['graph']['nodes']),6)
        self.assertEqual(len([e for e in d['graph']['edges'] if e['type']=='alternative']),2)
        self.assertEqual(len(d['graph']['branches']),4)
        self.assertTrue(all(o['mask_png'].startswith('data:image/png;base64,') for s in d['states'] for o in s['objects']))

if __name__=='__main__':unittest.main()
