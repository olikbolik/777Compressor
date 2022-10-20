import os
from unittest import TestCase
from unittest.mock import patch
from Jobs.Compressor import FileCompressor
from Common.Constants import HELPER_INFO_FILE

current_dir = os.getcwd()


class TestFileCompressor(TestCase):
    def setUp(self) -> None:
        self.compressor = FileCompressor()

    def tearDown(self) -> None:
        del self.compressor

    @patch('Jobs.Compressor.FileCompressor.files_to_compress')
    @patch('Jobs.Compressor.FileCompressor.compression_should_be_started')
    def test_compress(self, mock_compr, mock_files):
        path_to_log_file = current_dir+'/files_for_test/some_file.log'
        mock_compr.return_value = True
        with open(path_to_log_file, 'w+') as file:
            file.write('28')
        mock_files.return_value = [path_to_log_file]
        self.assertTrue(os.path.exists(path_to_log_file))
        self.compressor.compress()
        self.assertFalse(os.path.exists(path_to_log_file))
        self.assertTrue(os.path.exists(path_to_log_file+'.gz'))
        os.remove(path_to_log_file+'.gz')

    @patch('Jobs.Compressor.FileCompressor.files_to_compress')
    @patch('Jobs.Compressor.FileCompressor.compression_should_be_started')
    def test_compress_false(self, mock_comp, mock_files):
        path_to_log_file = current_dir+'/files_for_test/some_file.log'
        mock_comp.return_value = False
        with open(path_to_log_file, 'w+') as file:
            file.write('28')
        self.assertTrue(os.path.exists(path_to_log_file))
        self.compressor.compress()
        self.assertTrue(os.path.exists(path_to_log_file))
        self.assertFalse(os.path.exists(path_to_log_file+'.gz'))
        os.remove(path_to_log_file)
        mock_files.assert_not_called()

    @patch('Jobs.Compressor.LOGS_PATH', current_dir+'/files_for_test')
    def test_files_to_compress(self):
        self.assertEqual(self.compressor.files_to_compress(), [current_dir+'/files_for_test/test1.log'])

    def test_compression_should_be_started(self):
        path_to_helper_file = current_dir+'/files_for_test/'+HELPER_INFO_FILE
        self.compressor.helper_info_path = path_to_helper_file
        with open(path_to_helper_file, 'w+') as file:
            file.write('29')
        self.assertTrue(os.path.exists(path_to_helper_file))
        self.assertTrue(self.compressor.compression_should_be_started())
        os.remove(path_to_helper_file)

    def test_compression_should_be_started_no_file(self):
        path_to_helper_file = current_dir+'/files_for_test/'+HELPER_INFO_FILE
        self.compressor.helper_info_path = path_to_helper_file
        self.assertFalse(os.path.exists(path_to_helper_file))
        self.assertTrue(self.compressor.compression_should_be_started())
        self.assertTrue(os.path.exists(path_to_helper_file))
        os.remove(path_to_helper_file)

    def test_compression_should_be_started_false(self):
        path_to_helper_file = current_dir+'/files_for_test/'+HELPER_INFO_FILE
        self.compressor.helper_info_path = path_to_helper_file
        with open(path_to_helper_file, 'w+') as file:
            file.write('28')
        self.assertTrue(os.path.exists(path_to_helper_file))
        self.assertFalse(self.compressor.compression_should_be_started())
        os.remove(path_to_helper_file)
