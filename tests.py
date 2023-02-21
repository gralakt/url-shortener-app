import unittest
from app import app, url_database, generate_short_url

class TestApp(unittest.TestCase):

    def test_generate_short_url(self):
        url = generate_short_url()
        self.assertEqual(len(url), 6)
        self.assertTrue(all(c.isalnum() for c in url))

    def test_create_short_url(self):
        with app.test_client() as client:
            resp = client.post('/long/', json={'long_url': 'http://example.com'})
            data = resp.get_json()
            self.assertIn('short_url', data)
            short_url = data['short_url']
            self.assertIn(short_url, url_database)

    def test_expand_url(self):
        url_database['abcd12'] = 'http://example.com'
        with app.test_client() as client:
            resp = client.get('/short/abcd12/')
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.headers['Location'], 'http://example.com')

    def test_expand_unknown_url(self):
        with app.test_client() as client:
            resp = client.get('/short/unknown/')
            self.assertEqual(resp.status_code, 404)

if __name__ == '__main__':
    unittest.main()
