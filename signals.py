# dependencies
from PyQt5.QtCore import QObject, pyqtSignal



'''
Just holds all the signals used in the program
'''


class Signals(QObject):
    # signals need to be part of a sub-class of QObject
    set_team_label = pyqtSignal(str)
    update_loop_count = pyqtSignal()
    update_error_count = pyqtSignal()   # not implemented yet
    update_gold = pyqtSignal(int)
    update_item_quantities = pyqtSignal()
    update_world_stats = pyqtSignal(bool)
    update_arena_stats = pyqtSignal(bool)
    update_items_gained = pyqtSignal(str)
    add_ninja_card = pyqtSignal(object)
    add_to_item_helper = pyqtSignal(int)