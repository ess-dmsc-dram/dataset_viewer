from abc import ABC, abstractmethod

class DimensionPresenterInterface(ABC):

    @abstractmethod
    def register_stack_master(self, stack_master):
        pass

    @abstractmethod
    def notify(self, command):
        pass

    @abstractmethod
    def get_x_state(self):
        pass

    @abstractmethod
    def set_x_state(self, state):
        pass

    @abstractmethod
    def get_y_state(self):
        pass

    @abstractmethod
    def set_y_state(self, state):
        pass

    @abstractmethod
    def disable_dimension(self):
        pass

    @abstractmethod
    def enable_dimension(self):
        pass

    @abstractmethod
    def is_enabled(self):
        pass

    @abstractmethod
    def get_slider_value(self):
        pass
