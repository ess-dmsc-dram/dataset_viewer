import unittest
import mock

import xarray as xr
import numpy as np

from datasetviewer.mainview.interfaces.MainViewInterface import MainViewInterface
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface
from datasetviewer.plot.interfaces.PlotViewInterface import PlotViewInterface
from datasetviewer.plot.PlotPresenter import PlotPresenter

from collections import OrderedDict as DataSet
from datasetviewer.dataset.Variable import Variable

class PlotPresenterTest(unittest.TestCase):

    def setUp(self):

        self.mock_main_view = mock.create_autospec(MainViewInterface)
        self.mock_plot_view = mock.create_autospec(PlotViewInterface)

        self.mock_main_presenter = mock.create_autospec(MainViewPresenterInterface)

        self.fake_data = DataSet()
        self.fake_data["good"] = Variable("good", xr.DataArray(np.random.rand(3, 4, 5), dims=['x', 'y', 'z']))
        self.fake_data["valid"] = Variable("valid", xr.DataArray(np.random.rand(3), dims=['b']))
        self.fake_data["twodims"] = Variable("twodims", xr.DataArray(np.random.rand(3,8), dims=['g','h']))
        self.fake_data["alsogood"] = Variable("alsogood", xr.DataArray(np.random.rand(3,4,5,6), dims=['c','d','e','f']))

    def test_presenter_throws_when_view_none(self):
        '''
        Test that the PlotPresenter throws an Exception when the PlotView is None.
        '''

        with self.assertRaises(ValueError):
            PlotPresenter(None)

    def test_clear_plot(self):
        '''
        Test that loading a new data array causes the previous plot to be cleared.
        '''

        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.register_master(self.mock_main_presenter)
        plot_pres.set_dict(self.fake_data)

        plot_pres.clear_plot = mock.MagicMock()
        plot_pres.create_default_plot("alsogood")
        plot_pres.clear_plot.assert_called_once()

    def test_plot_call(self):
        '''
        Test that creating a default plot with ND data causes the appropriate view plot function to be called.
        '''

        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.register_master(self.mock_main_presenter)
        plot_pres.set_dict(self.fake_data)

        plot_pres.create_default_plot("valid")
        xr.testing.assert_identical(self.mock_plot_view.plot_line.call_args[0][0], self.fake_data["valid"].data)

        plot_pres.create_default_plot("twodims")
        xr.testing.assert_identical(self.mock_plot_view.plot_line.call_args[0][0],
                                    self.fake_data["twodims"].data.transpose()[0])

        plot_pres.create_default_plot("alsogood")
        xr.testing.assert_identical(self.mock_plot_view.plot_image.call_args[0][0],
                                    self.fake_data["alsogood"].data.isel({'e':0, 'f':0}).transpose('d','c'))

    def test_register_master(self):
        '''
        Test the two-way link between the PlotPresenter and its MainViewPresenter by ensuring that the master's
        `subscribe_plot_presenter` method is called after the PlotPresenter's `register_master` method is called.
        '''

        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.register_master(self.mock_main_presenter)

        self.mock_main_presenter.subscribe_plot_presenter.assert_called_once_with(plot_pres)

    def test_label_axes(self):
        '''
        Test that the axes label functions are called with the expected inputs.
        '''

        # Don't label the axes in the case of 1D data
        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.register_master(self.mock_main_presenter)

        plot_pres.set_dict(self.fake_data)

        plot_pres.create_default_plot("valid")
        self.mock_plot_view.label_x_axis.assert_not_called()
        self.mock_plot_view.label_y_axis.assert_not_called()

        # Label a single axes in the case of 2D data
        plot_pres.create_default_plot("twodims")
        self.mock_plot_view.label_x_axis.assert_called_once_with(self.fake_data["twodims"].data.dims[0])
        self.mock_plot_view.label_y_axis.assert_not_called()

        self.mock_plot_view.reset_mock()
        plot_pres.set_dict(self.fake_data)

        # Label both axes in the case of nD data with n > 2
        plot_pres.create_default_plot("good")
        self.mock_plot_view.label_x_axis.assert_called_once_with(self.fake_data["good"].data.dims[0])
        self.mock_plot_view.label_y_axis.assert_called_once_with(self.fake_data["good"].data.dims[1])

    def test_draw_plot(self):
        '''
        Test that the presenter calls the PlotView's draw function after receiving new data.
        '''

        self.mock_plot_view.draw_plot = mock.MagicMock()

        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.register_master(self.mock_main_presenter)
        plot_pres.set_dict(self.fake_data)

        plot_pres.create_default_plot("valid")
        self.mock_plot_view.draw_plot.assert_called_once()

    def test_new_data_updates_toolbar(self):
        '''
        Test that loading new data causes the toolbar to be updated.
        '''

        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.register_master(self.mock_main_presenter)
        plot_pres.set_dict(self.fake_data)

        plot_pres.create_default_plot("valid")
        self.mock_main_presenter.update_toolbar.assert_called_once()
