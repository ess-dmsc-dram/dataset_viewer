import unittest

import mock

from enum import Enum

from datasetviewer.fileloader.FileLoaderPresenter import FileLoaderPresenter
from datasetviewer.fileloader.interfaces.FileLoaderViewInterface import FileLoaderViewInterface
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface
from datasetviewer.fileloader.Command import Command

import xarray as xr

class FileLoaderPresenterTest(unittest.TestCase):

    def setUp(self):

        self.mock_main_presenter = mock.create_autospec(MainViewPresenterInterface)
        self.mock_main_presenter.set_data = mock.MagicMock()
        self.mock_view = mock.create_autospec(FileLoaderViewInterface)

        self.empty_data = xr.Dataset()
        self.fake_file_path = "filepath"

        self.mock_view.get_selected_file_path = mock.MagicMock(side_effect=lambda: self.fake_file_path)

        self.fl_presenter = FileLoaderPresenter(self.mock_view)
        self.fl_presenter.register_master(self.mock_main_presenter)

    def test_presenter_throws_if_view_none(self):
        '''
        Test that the FileLoaderPresenter throws an Exception when the FileLoaderView is None.
        '''
        with self.assertRaises(ValueError):
            FileLoaderPresenter(None)

    def test_register_master(self):
        '''
        Test the two-way link between the FileLoaderPresenter and its MainViewPresenter by ensuring that the master's
        `subscribe_subpresenter` method is called after the FileLoaderPresenter's `register_master` method is called.
        '''
        fl_presenter = FileLoaderPresenter(self.mock_view)

        main_presenter = mock.create_autospec(MainViewPresenterInterface)
        fl_presenter.register_master(main_presenter)

        main_presenter.subscribe_subpresenter.assert_called_once_with(fl_presenter)

    def test_file_selection_calls_get_path_on_view(self):
        '''
        Test that a FILELOADREQUEST in the FileLoaderPresenter's `notify` function causes the `get_selected_file_path`
        method on the FileLoaderVIew to be called.
        '''
        fl_presenter = FileLoaderPresenter(self.mock_view)
        fl_presenter.register_master(self.mock_main_presenter)
        fl_presenter._load_data = mock.MagicMock()
        fl_presenter.notify(Command.FILEOPENREQUEST)
        self.mock_view.get_selected_file_path.assert_called_once()

    def test_bad_file_shows_message(self):
        '''
        Test that the request to open a bad file causes the view to display a message.
        '''
        with mock.patch("datasetviewer.fileloader.FileLoaderTool.open_dataset",
                        side_effect=lambda path: self.empty_data):

            self.fl_presenter._load_data(self.fake_file_path)
            self.mock_view.show_reject_file_message.assert_called_once()

    def test_load_file(self):
        '''
        Test that a FILEOPENREQUEST in `notify` causes the `_load_data` method to be called with the expected argument.
        '''
        fl_presenter = FileLoaderPresenter(self.mock_view)
        fl_presenter.register_master(self.mock_main_presenter)
        fl_presenter._load_data = mock.MagicMock(side_effect = lambda path: self.empty_data.variables)

        fl_presenter.notify(Command.FILEOPENREQUEST)
        fl_presenter._load_data.assert_called_once_with(self.fake_file_path)

    def test_file_open_success_informs_main_presenter(self):
        '''
        Test that successfully opening a file in the FileLoaderPresenter causes the resulting DataSet to be sent to the
        MainViewPresenter.
        :return:
        '''
        with mock.patch("datasetviewer.fileloader.FileLoaderTool.file_to_dict",
                        side_effect = lambda path: self.empty_data.variables):

            self.fl_presenter.notify(Command.FILEOPENREQUEST)
            self.mock_main_presenter.set_data.assert_called_once_with(self.empty_data.variables)

    def test_unknown_command_raises(self):
        '''
        Test that an exception is thrown if notify is called with a command it does not recognise.
        '''
        fl_presenter = FileLoaderPresenter(self.mock_view)

        fake_enum = Enum(value='invalid', names=[('bad_command', -200000)])

        with self.assertRaises(ValueError):
            fl_presenter.notify(fake_enum.bad_command)
