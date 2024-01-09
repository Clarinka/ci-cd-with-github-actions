import unittest
from flask import Flask
from app import app, items

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        items.clear()  # Reset the state of the 'items' list before each test

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Items', response.data)

    def test_add_item_route(self):
        response = self.app.post('/add', data={'item': 'Test Item'})
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0], 'Test Item')

    def test_delete_item_route(self):
        items.append('Item to delete')
        response = self.app.get('/delete/0')
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(len(items), 0)

    def test_update_item_route(self):
        items.append('Item to update')
        response = self.app.post('/update/0', data={'new_item': 'Updated Item'})
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0], 'Updated Item')

if __name__ == '__main__':
    unittest.main()
