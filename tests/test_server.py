import unittest
from server import app

class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        r = self.client.get('/health')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json, {'status': 'ok', 'mode': 'synthetic'})

    def test_home_and_assets(self):
        home = self.client.get('/')
        self.assertEqual(home.status_code, 200)
        home.close()
        js = self.client.get('/static/app.js')
        self.assertEqual(js.status_code, 200)
        js.close()

    def test_api_graph_has_one_split_and_merge(self):
        d = self.client.get('/api/demo').get_json()
        self.assertEqual(d['summary'], {'frames': 8, 'events': 2, 'splits': 1, 'merges': 1})
        self.assertEqual([e['kind'] for e in d['events']], ['split', 'merge'])
        self.assertTrue(all('iou' in link for e in d['events'] for link in e['evidence']))

if __name__ == '__main__':
    unittest.main()
