import unittest
from unittest.mock import patch

from src.file_utils import *


class TestFileUtils(unittest.TestCase):

    @patch('os.listdir')
    @patch('os.path.exists')
    def test_find_ditamap_in_directory_single_file(self, mock_exists, mock_listdir):
        # Setup mocks
        mock_exists.return_value = True
        mock_listdir.return_value = ['test.ditamap']
        input_directory = '/path/to/directory'

        # Action
        result = find_ditamap_in_directory(input_directory)

        # Assert
        self.assertIn('test.ditamap', result)

    @patch('os.listdir')
    def test_find_ditamap_in_directory_no_file(self, mock_listdir):
        # Setup
        mock_listdir.return_value = []
        input_directory = '/path/to/directory'

        # Assert
        with self.assertRaises(ValueError):
            find_ditamap_in_directory(input_directory)

    @patch('os.listdir')
    def test_list_dita_files(self, mock_listdir):
        # Setup
        mock_listdir.return_value = ['file1.dita', 'file2.dita', 'not_a_dita_file.txt']
        input_directory = '/path/to/directory'

        # Action
        result = list_dita_files(input_directory)

        # Assert
        self.assertEqual(len(result), 2)
        self.assertTrue(all(file.endswith('.dita') for file in result))

    @patch('os.path.isfile')
    def test_validate_referenced_dita_files_all_present(self, mock_isfile):
        # Setup
        ditamap_structure = [
            {'path': 'file1.dita', 'children': []},
            {'path': 'file2.dita', 'children': []}
        ]
        dita_files = [os.path.join('/path/to', file) for file in ['file1.dita', 'file2.dita']]
        input_directory = '/path/to'

        # Mock os.path.isfile to always return True for these tests
        mock_isfile.return_value = True

        # Action
        missing_files = validate_referenced_dita_files(ditamap_structure, dita_files, input_directory)

        # Assert
        self.assertEqual(missing_files, [])

    @patch('os.path.isfile')
    def test_validate_referenced_dita_files_missing_files(self, mock_isfile):
        # Setup
        ditamap_structure = [
            {'path': 'file1.dita', 'children': []},
            {'path': 'missing_file.dita', 'children': []}
        ]
        dita_files = [os.path.join('/path/to', file) for file in ['file1.dita']]
        input_directory = '/path/to'

        # Make os.path.isfile return False when checking for 'missing_file.dita'
        mock_isfile.side_effect = lambda x: not x.endswith('missing_file.dita')

        # Action
        missing_files = validate_referenced_dita_files(ditamap_structure, dita_files, input_directory)

        # Assert
        self.assertEqual(missing_files, ['missing_file.dita'])


if __name__ == '__main__':
    unittest.main()
