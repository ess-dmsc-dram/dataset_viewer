from abc import ABCMeta, abstractmethod
from PyQt5 import QtCore

from six import with_metaclass

class Meta(ABCMeta, type(QtCore.QObject)):
    pass

class StackViewInterface(with_metaclass(Meta)):

    @abstractmethod
    def create_stack_element(self):
        pass

    @abstractmethod
    def add_dimension_widget(self, idx, widget):
        pass

    @abstractmethod
    def change_stack_face(self, idx):
        pass

    @abstractmethod
    def delete_widget(self, idx):
        pass

    @abstractmethod
    def get_presenter(self):
        pass
