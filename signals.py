from PyQt5.QtCore import QObject, pyqtSignal

class Signals(QObject):
    # signals need to be part of a sub-class of QObject
    update_loop_count = pyqtSignal()
    update_error_count = pyqtSignal()   # not implemented
    update_gold = pyqtSignal(int)
    update_world_stats = pyqtSignal(bool)
    update_arena_stats = pyqtSignal(bool)   # not implemented
    update_items_gained = pyqtSignal(str)
    add_ninja_card = pyqtSignal(object)