from abc import ABC, abstractmethod

class PlotPresenterInterface(ABC):

    @abstractmethod
    def create_default_plot(self, data):
        pass

    @abstractmethod
    def clear_plot(self):
        pass

    @abstractmethod
    def register_master(self, master):
        pass

    @abstractmethod
    def draw_plot(self):
        pass
