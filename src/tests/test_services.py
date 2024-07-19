import unittest
from unittest.mock import patch, MagicMock
from src.services import fetch_menu, insert_menu_item, update_menu_item_in_db, delete_menu_item_from_db

class TestServices(unittest.TestCase):

    @patch('src.services.connect_to_database')
    def test_fetch_menu(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, 'Product 1'), (2, 'Product 2')]
        
        expected_result = [
            {'id': 1, 'name': 'Product 1'},
            {'id': 2, 'name': 'Product 2'}
        ]
        
        result = fetch_menu()
        
        self.assertEqual(result, expected_result)
        mock_cursor.execute.assert_called_once_with('SELECT * FROM menu ORDER BY id')

    @patch('src.services.connect_to_database')
    def test_fetch_menu_failure(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        expected_result = []
        
        result = fetch_menu()
        
        self.assertEqual(result, expected_result)
        mock_cursor.execute.assert_called_once_with('SELECT * FROM menu ORDER BY id')
    
    @patch('src.services.connect_to_database')
    def test_insert_menu_item(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        expected_result = {'id': 1, 'name': 'Product 1'}
        mock_cursor.fetchone.return_value = (1, 'Product 1')

        result = insert_menu_item('Product 1')

        self.assertEqual(result, expected_result)
        mock_cursor.execute.assert_called_once()
        args, kwargs = mock_cursor.execute.call_args
        self.assertEqual(
            ''.join(args[0].split()),
            ''.join('''
                INSERT INTO menu (name) 
                VALUES (%s) RETURNING id, name
            '''.split())
        )
        self.assertEqual(args[1], ('Product 1',))

    @patch('src.services.connect_to_database')
    def test_update_menu_item_in_db(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1)
        
        result = update_menu_item_in_db(1, 'Updated Name')
        
        self.assertEqual(result, {'status': 'success', 'message': 'Item updated successfully'})
        self.assertEqual(mock_cursor.execute.call_args[0][1], ('Updated Name', 1))
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
       
    @patch('src.services.connect_to_database')
    def test_update_menu_item_in_db_failure(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = None
        
        result = update_menu_item_in_db(1, 'Updated Name')
        
        self.assertEqual(result, {'status': 'failure', 'message': 'Item not found'})
        
        self.assertEqual(
            ''.join(mock_cursor.execute.call_args[0][0].split()),
            ''.join('''
                SELECT id FROM menu WHERE id = %s
            '''.split())
        )
        self.assertEqual(mock_cursor.execute.call_args[0][1], (1,))
        mock_conn.commit.assert_not_called()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('src.services.connect_to_database')
    def test_delete_menu_item_from_db(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1)
        
        result = delete_menu_item_from_db(1)
        
        self.assertEqual(
            ''.join(mock_cursor.execute.call_args[0][0].split()),
            ''.join('''
                DELETE FROM menu WHERE id = %s
            '''.split())
        )
        self.assertEqual(result, {'status': 'success', 'message': 'Item updated successfully'})
        self.assertEqual(mock_cursor.execute.call_args[0][1], (1,))
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

