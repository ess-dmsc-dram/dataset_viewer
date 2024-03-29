from datasetviewer.mainview.interfaces.MainViewInterface import MainViewInterface
from datasetviewer.mainview.MainViewPresenter import MainViewPresenter
from datasetviewer.fileloader.FileLoaderWidget import FileLoaderWidget
from datasetviewer.preview.PreviewWidget import PreviewWidget
from PyQt5.QtWidgets import QMainWindow, QAction, QGridLayout, QWidget
from datasetviewer.plot.PlotWidget import PlotWidget

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class MainWindow(MainViewInterface, QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")

        file_loader_widget = FileLoaderWidget(self)
        file_loader_presenter = file_loader_widget.get_presenter()
        filemenu.addAction(file_loader_widget)

        preview_widget = PreviewWidget()
        preview_presenter = preview_widget.get_presenter()

        plot_widget = PlotWidget()
        plot_presenter = plot_widget.get_presenter()
        self.toolbar = NavigationToolbar(plot_widget, self)
        self.addToolBar(self.toolbar)

        MainViewPresenter(self, file_loader_presenter, preview_presenter, plot_presenter)

        # Action for exiting the program
        exitAct = QAction("Exit", self)
        exitAct.triggered.connect(self.close)
        filemenu.addAction(exitAct)

        self.statusBar()

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout()
        centralWidget.setLayout(gridLayout)

        gridLayout.addWidget(preview_widget, 0, 0)
        gridLayout.addWidget(plot_widget, 0, 1)

        self.setWindowTitle("Dataset Viewer")
        self.show()

    def update_toolbar(self):
        """ Informs the toolbar that the 'Home' button should take the plot back to the current state. Called when a new
            dataset is loaded. """

        self.toolbar.update()
        self.toolbar.push_current()
