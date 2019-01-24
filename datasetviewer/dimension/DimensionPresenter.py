from datasetviewer.dimension.interfaces.DimensionPresenterInterface import DimensionPresenterInterface
from datasetviewer.stack.interfaces.StackPresenterInterface import StackPresenterInterface
from datasetviewer.dimension.Command import Command

class DimensionPresenter(DimensionPresenterInterface):

    def __init__(self, dim_view, dim_name):

        self._view = dim_view
        self._dim_name = dim_name
        self._stack_master = None

    def notify(self, command):

        if command == Command.XBUTTONPRESS:

            new_x_state = self._view.get_x_state()
            self._stack_master.x_button_press(self._dim_name, new_x_state)

        if command == Command.YBUTTONPRESS:

            new_y_state = self._view.get_y_state()
            self._stack_master.y_button_press(self._dim_name, new_y_state)

    def register_stack_master(self, stack_master):

        assert (isinstance(stack_master, StackPresenterInterface))

        self._stack_master = stack_master
