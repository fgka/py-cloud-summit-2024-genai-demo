import unittest
from unittest.mock import patch
from front import app, format_duration
import time

class TestFront(unittest.TestCase):

    def test_main_route_with_empty_messages(self):
        with patch('requests.get') as mock_get:
            mock_get.return_value.text = '[]'
            response = app.test_client().get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'No messages yet', response.data)

    def test_main_route_with_messages(self):
        with patch('requests.get') as mock_get:
            mock_get.return_value.text = '[{"author": "Alice", "message": "Hello world!", "timestamp": 1678886400}]'
            response = app.test_client().get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Alice', response.data)
            self.assertIn(b'Hello world!', response.data)
            self.assertIn(b'just now', response.data)

    def test_post_route(self):
        with patch('requests.post') as mock_post:
            response = app.test_client().post('/post', data={'name': 'Bob', 'message': 'This is a test message'})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, 'http://localhost/')
            mock_post.assert_called_once_with(url='http://localhost:8080/messages', data='{"author": "Bob", "message": "This is a test message"}', headers={'content-type': 'application/json'})

    def test_format_duration_just_now(self):
        self.assertEqual(format_duration(time.time()), "just now")

    def test_format_duration_seconds_ago(self):
        self.assertEqual(format_duration(time.time() - 5), "5 seconds ago")

    def test_format_duration_minutes_ago(self):
        self.assertEqual(format_duration(time.time() - 65), "1 minute ago")

    def test_format_duration_hours_ago(self):
        self.assertEqual(format_duration(time.time() - 3605), "1 hour ago")

    def test_format_duration_days_ago(self):
        self.assertEqual(format_duration(time.time() - 86405), "1 day ago")

    def test_format_duration_years_ago(self):
        self.assertEqual(format_duration(time.time() - 31536005), "1 year ago")

if __name__ == '__main__':
    unittest.main()
