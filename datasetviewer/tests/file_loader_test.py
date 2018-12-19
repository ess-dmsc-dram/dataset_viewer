import unittest
from unittest.mock import patch
from datasetviewer.fileloader.FileLoaderTool import FileLoaderTool

import xarray as xr
import numpy as np

class FileLoaderTest(unittest.TestCase):

    def setUp(self):

        self.file_reader = FileLoaderTool()

        # Bad data in which one of the elements only has a single dimension
        self.bad_data = xr.Dataset({'good': (['x', 'y', 'z'], np.random.rand(3, 4, 5)), 'bad': np.random.rand(2)})

        # Good data for which all of the elements have 2+ dimensions
        self.good_data = xr.Dataset({'good': (['x', 'y', 'z'], np.random.rand(3, 4, 5)),
                                     'valid': (['a', 'b'], np.random.rand(3, 4)),
                                     'alsogood': (['c', 'd', 'e', 'f'], np.random.rand(3, 4, 5, 6))})

        self.fake_data_path = "madeuppath"

    def test_empty_file_throws(self):
        '''
        Test that an empty data array is rejected by the FileLoaderTool.
        '''
        empty_data = xr.Dataset()

        with patch('datasetviewer.fileloader.FileLoaderTool.open_dataset', side_effect = lambda path: empty_data):
            with self.assertRaises(ValueError):
                self.file_reader.file_to_dict(self.fake_data_path)

    def test_bad_dimensions_rejected(self):
        '''
        Test that a data array containing elements with fewer than two dimensions is deemed invalid by the FileLoaderTool
        '''
        self.assertTrue(self.file_reader.invalid_dataset(self.bad_data))

    def test_good_dimensions_accepted(self):
        '''
        Test that a data array containing no elements with fewer than two dimensions is deemed valid by the
        FileLoaderTool.
        '''
        self.assertFalse(self.file_reader.invalid_dataset(self.good_data))

    def test_file_read_success(self):
        '''
        Test that FileLoaderTool calls the `open_dataset` method.
        '''

        with patch('datasetviewer.fileloader.FileLoaderTool.open_dataset', side_effect = lambda path: self.good_data) as dummy_data_loader:
            self.file_reader.file_to_dict(self.fake_data_path)
            dummy_data_loader.assert_called_once_with(self.fake_data_path)

    def test_bad_data_raises(self):
        '''
        Test that bad data being returned by the `open_dataset` method raises an Exception.
        '''

        with patch('datasetviewer.fileloader.FileLoaderTool.open_dataset', side_effect = lambda path: self.bad_data):
            with self.assertRaises(ValueError):
                self.file_reader.file_to_dict(self.fake_data_path)
