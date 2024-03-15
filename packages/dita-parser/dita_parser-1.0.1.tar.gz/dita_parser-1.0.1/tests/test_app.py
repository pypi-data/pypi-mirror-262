import logging
import unittest
from unittest.mock import patch

from src.app import main


class TestApp(unittest.TestCase):
    def setUp(self):
        self.mock_isdir_patcher = patch('os.path.isdir', return_value=True)
        self.mock_isdir = self.mock_isdir_patcher.start()

    def tearDown(self):
        self.mock_isdir_patcher.stop()

    def test_merge_operation_success(self):
        with patch('dita_processor.merge_dita_files') as mock_merge_dita_files, \
                patch('file_utils.validate_referenced_dita_files', return_value=[]), \
                patch('dita_processor.parse_ditamap'), \
                patch('file_utils.find_ditamap_in_directory'), \
                patch('file_utils.list_dita_files'), \
                patch('plac.call') as mock_plac_call:
            mock_plac_call.side_effect = lambda func, args: func(*args)
            main('merge', 'input_dir', 'output_dir')
            mock_merge_dita_files.assert_called_once()

    def test_split_operation_success(self):
        with patch('dita_processor.split_dita_files') as mock_split_dita_files, \
                patch('dita_processor.validate_merged_xml', return_value=['merged.xml']), \
                patch('plac.call') as mock_plac_call:
            mock_plac_call.side_effect = lambda func, args: func(*args)
            main('split', 'input_dir', 'output_dir')
            mock_split_dita_files.assert_called_once()

    def test_invalid_dir(self):
        with patch('os.path.isdir', return_value=False), \
                patch('plac.call') as mock_plac_call:
            mock_plac_call.side_effect = lambda func, args: func(*args)
            with self.assertRaises(SystemExit) as cm:
                with self.assertLogs(level='ERROR') as cm_log:
                    logging.getLogger().setLevel(logging.ERROR)
                    main('merge', 'input_dir', 'output_dir')
            self.assertEqual(cm.exception.code, 1)
            self.assertIn(
                "Error: The specified input path 'input_dir' is not a directory or does not exist. Please provide a valid input folder.",
                cm_log.output[0])

    def test_no_action_given(self):
        with patch('plac.call') as mock_plac_call:
            mock_plac_call.side_effect = lambda func, args: func(*args)
            with self.assertRaises(SystemExit) as cm:
                with self.assertLogs(level='ERROR') as cm_log:
                    main('', 'input_dir', 'output_dir')
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Invalid action ''. Action must be either 'merge' or 'split'.", cm_log.output[0])

    def test_invalid_action_given(self):
        with patch('plac.call') as mock_plac_call:
            mock_plac_call.side_effect = lambda func, args: func(*args)
            with self.assertRaises(SystemExit) as cm:
                with self.assertLogs(level='ERROR') as cm_log:
                    main('sing', 'input_dir', 'output_dir')
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("Invalid action 'sing'. Action must be either 'merge' or 'split'.", cm_log.output[0])


class TestAppIntegration(unittest.TestCase):
    def test_merge_command(self):
        main('merge', '../examples/input_dita_files', '../examples/output_of_merge')

    def test_split_command(self):
        main('split', '../examples/output_of_merge', '../examples/output_of_split')


if __name__ == "__main__":
    unittest.main()
