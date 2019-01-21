from abc import ABCMeta, abstractmethod
from PyQt5 import QtCore

from six import with_metaclass

class Meta(ABCMeta, type(QtCore.QObject)):
    pass

class StackViewInterface(with_metaclass(Meta)):

    @abstractmethod
    def clear_stack(self):
        pass
