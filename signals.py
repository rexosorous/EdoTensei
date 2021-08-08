from PyQt5.QtCore import QObject, pyqtSignal

class Signals(QObject):
    # signals need to be part of a sub-class of QObject
    ninja_signal = pyqtSignal(object)