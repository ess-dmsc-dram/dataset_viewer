import unittest
import mock

import xarray as xr
import numpy as np

from datasetviewer.mainview.interfaces.MainViewInterface import MainViewInterface
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface
from datasetviewer.plot.interfaces.PlotViewInterface import PlotViewInterface
from datasetviewer.plot.PlotPresenter import PlotPresenter

class PlotPresenterTest(unittest.TestCase):

    def setUp(self):

        self.mock_main_view = mock.create_autospec(MainViewInterface)
        self.mock_plot_view = mock.create_autospec(PlotViewInterface)

        self.mock_plot_view.plot_line = mock.MagicMock()
        self.mock_plot_view.plot_image = mock.MagicMock()

        self.fake_data = xr.Dataset({'good': (['x', 'y', 'z'], np.random.rand(3, 4, 5)),
                                     'valid': (['b'], np.random.rand(3)),
                                     'twodims': (['g', 'h'], np.random.rand(3, 8)),
                                     'alsogood': (['c', 'd', 'e', 'f'], np.random.rand(3, 4, 5, 6))})

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
        plot_pres.clear_plot = mock.MagicMock()
        plot_pres.create_default_plot(self.fake_data.alsogood)
        plot_pres.clear_plot.assert_called_once()

    def test_plot_call(self):
        '''
        Test that creating a default plot with ND data causes the appropriate view plot function to be called.
        '''

        plot_pres = PlotPresenter(self.mock_plot_view)

        plot_pres.create_default_plot(self.fake_data.valid)
        xr.testing.assert_identical(self.mock_plot_view.plot_line.call_args[0][0], self.fake_data.valid)

        plot_pres.create_default_plot(self.fake_data.twodims)
        xr.testing.assert_identical(self.mock_plot_view.plot_line.call_args[0][0], self.fake_data.twodims[0])

        plot_pres.create_default_plot(self.fake_data.alsogood)
        xr.testing.assert_identical(self.mock_plot_view.plot_image.call_args[0][0],
                                    self.fake_data.alsogood.isel({'e':0, 'f':0}).transpose('d','c'))

    def test_register_master(self):
        '''
        Test the two-way link between the PlotPresenter and its MainViewPresenter by ensuring that the master's
        `subscribe_plot_presenter` method is called after the PlotPresenter's `register_master` method is called.
        '''

        plot_pres = PlotPresenter(self.mock_plot_view)

        main_presenter = mock.create_autospec(MainViewPresenterInterface)
        plot_pres.register_master(main_presenter)

        main_presenter.subscribe_plot_presenter.assert_called_once_with(plot_pres)
