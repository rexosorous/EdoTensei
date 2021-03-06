# standard python modules
import sys
import asyncio
import functools
import logging
import structlog

# dependencies
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFrame, QGridLayout, QTableWidgetItem, QAction, QTreeWidgetItem
from PyQt5.QtGui import QIcon
import qasync

# local modules
import gui.main_window
import gui.main_frame
import gui.ninja_card_frame
import EdoTensei
import signals
import utilities as util
from DBHandler import DBHandler
from RecipeWindow import RecipeWindow
import CustomPyQt



class MainFrame(QFrame, gui.main_frame.Ui_Frame):
    '''
    The GUI and logic for the QFrames that control browser activity
    Each instance of this should control and interact with only 1 browser driver instance and only 1 account

    Args:
        account (str): should either be 'account_1' or 'account_2'. determines which account this instance is tied to

    Attributes:
        account (str)
        db (DBHandler)
        sigs (Signals)
        bot (EdoTensei)
        recipe_window (RecipeWindow)
    '''
    def __init__(self, account: str):
        super().__init__()
        self.setupUi(self)
        self.account = account
        self.db = DBHandler(account)
        self.sigs = signals.Signals()
        self.bot = EdoTensei.EdoTensei(self.db, self.sigs)
        self.recipe_window = RecipeWindow(self.db, self.sigs)
        self.item_recipe_tree = CustomPyQt.Tree(self.item_recipe_tree)
        self.init_labels()
        self.create_context_menus()
        self.connect_events()
        self.load_settings()



    def init_labels(self):
        '''
        Initializes all the labels under Summary except for team_label and gold_gained_label
        This doesn't really need to be executed
        '''
        self.loop_count_label.setText('0')
        self.error_count_label.setText('0')
        self.gold_current_label.setText('0')
        # self.gold_gained_label.setText('+0')
        self.world_wins_label.setText('0')
        self.world_losses_label.setText('0')
        self.arena_wins_label.setText('0')
        self.arena_losses_label.setText('0')



    def create_context_menus(self):
        '''
        Creates all the right-click context menus
        '''
        self.item_location_table.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.item_location_table.set_mission = QAction("Set As World Mission", self.item_location_table)
        self.item_location_table.addAction(self.item_location_table.set_mission)
        self.item_location_table.set_mission.triggered.connect(self.set_world_mission)
        self.item_recipe_tree.create_context_menu()



    def connect_events(self):
        '''
        Connects all the button clicks, signals, and other events to functions

        Note:
            Does not include events created in self.create_context_menus()
        '''
        self.launch_button.clicked.connect(self.launch_or_close)
        self.start_button.clicked.connect(self.start_or_pause)
        self.reset_settings_button.clicked.connect(self.load_settings)
        self.submit_settings_button.clicked.connect(self.save_settings)
        self.notes_textbox.textChanged.connect(self.save_notes)
        self.sigs.set_team_label.connect(self.set_team_label)
        self.sigs.update_loop_count.connect(self.update_loop_label)
        self.sigs.update_error_count.connect(self.update_error_label)
        self.sigs.update_gold.connect(self.update_gold_labels)
        self.sigs.update_item_quantities.connect(self.update_item_helper_quantities)
        self.sigs.update_world_stats.connect(self.update_world_labels)
        self.sigs.update_arena_stats.connect(self.update_arena_labels)
        self.sigs.update_items_gained.connect(self.update_items_table)
        self.sigs.add_ninja_card.connect(self.add_ninja_card)
        self.sigs.add_to_item_helper.connect(self.add_to_item_helper)
        self.item_recipe_tree.open_action.triggered.connect(self.open_recipe_window)
        self.item_recipe_tree.remove_action.triggered.connect(self.remove_recipe)



    @qasync.asyncSlot()
    async def launch_or_close(self):
        '''
        Either starts the bot's logic sequence or shuts the bot down
        Also changes the icons and status to match
        '''
        if self.bot.state == EdoTensei.State.STOPPED:
            self.launch_button.setIcon(QIcon('./icons/stop.png'))
            self.start_button.setIcon(QIcon('./icons/pause.png'))
            self.status_label.setText('WAIT')
            self.status_label.setPalette(util.Colors.RED)
            await self.bot.run()
        elif self.bot.state != EdoTensei.State.STOPPED:
            self.launch_button.setIcon(QIcon('./icons/launch.png'))
            # self.start_button.setIcon()
            await self.bot.shutdown()



    @qasync.asyncSlot()
    async def start_or_pause(self):
        '''
        Either pauses the bot's main loop or continues it
        Also changes the icons and status to match
        '''
        if self.bot.state == EdoTensei.State.RUNNING:
            self.start_button.setIcon(QIcon('./icons/pause.png'))
            self.status_info_label.setText('manually paused')
            # self.bot.pause()
        elif self.bot.state == EdoTensei.State.PAUSED:
            self.start_button.setIcon(QIcon('./icons/start.png'))
            # self.bot.resume()



    @qasync.asyncSlot()
    async def load_settings(self):
        '''
        Opens up settings.json and changes the various UI elements to match
        '''
        settings = util.load_settings(self.account)
        await self.bot.update_settings(settings)
        self.sleep_lower_number.setValue(settings['sleep_lower'])
        self.sleep_upper_number.setValue(settings['sleep_upper'])
        self.world_behavior_combobox.setCurrentIndex(settings['world_mode'])
        self.world_mission_text.setText(settings['mission_url'])
        self.arena_energy_cap_number.setValue(settings['arena_energy_cap'])
        self.arena_rematches_only_checkbox.setCheckState(Qt.Checked) if settings['arena_rematches_only'] else self.arena_rematches_only_checkbox.setCheckState(Qt.Unchecked)
        self.arena_wins_only_checkbox.setCheckState(Qt.Checked) if settings['arena_wins_only'] else self.arena_wins_only_checkbox.setCheckState(Qt.Unchecked)
        self.notes_textbox.setText(settings['notes'])
        self.item_recipe_tree.clear()
        for item_id in settings['item_helper']:
            self.item_recipe_tree.add_product(item_id, self.db)
        self.item_recipe_tree.update_quantities(self.db)
        await self.populate_item_location_table(self.item_recipe_tree.map.keys())



    @qasync.asyncSlot()
    async def save_settings(self):
        '''
        Opens up settings.json and saves any settings that may have been changed
        Called ONLY when self.submit_settings_button is clicked
        '''
        settings = {
            'sleep_lower': self.sleep_lower_number.value(),
            'sleep_upper': self.sleep_upper_number.value(),
            'world_mode': self.world_behavior_combobox.currentIndex(),
            'mission_url': self.world_mission_text.text(),
            'arena_energy_cap': self.arena_energy_cap_number.value(),
            'arena_rematches_only': True if self.arena_rematches_only_checkbox.checkState() == Qt.Checked else False,
            'arena_wins_only': True if self.arena_wins_only_checkbox.checkState() == Qt.Checked else False
        }
        new_settings = util.save_settings(self.account, settings)
        await self.bot.update_settings(new_settings)



    @qasync.asyncSlot()
    async def save_notes(self):
        '''
        Saves only the notes portion of settings.json whenever a user types in self.notes_textbox
        This is separate from self.save_settings() because if the user accidentally makes changes to the settings UI
        and then types in the notes textbox, it'll save their settings changes even though they didn ot press the submit button
        '''
        util.save_settings(self.account, {'notes': self.notes_textbox.toPlainText()})



    @qasync.asyncSlot()
    async def open_recipe_window(self):
        '''
        Opens an instance of RecipeWindow which is used to add recipes to the item helper
        Called when a user right clicks in self.item_recipe_tree and clicks "Add Recipes"
        '''
        await self.recipe_window.open()



    @qasync.asyncSlot(int)
    async def add_to_item_helper(self, item_id: int):
        '''
        Adds a product item (the item the user wants to craft/find) to self.item_recipe_tree
        If the item is crafted, this will create a tree with the full recipe

        Note:
            This is a pretty sloppy implementation that shares a lot of the same code as RecipeWindow.py
            I should come back to this and pretty it up

        Args:
            item_id (int)
        '''
        self.item_recipe_tree.add_product(item_id, self.db)
        await self.populate_item_location_table(self.item_recipe_tree.map.keys())

        # save the newly added recipe to settings
        settings = {'item_helper': self.item_recipe_tree.get_product_ids()}
        util.save_settings(self.account, settings)



    @qasync.asyncSlot()
    async def update_item_helper_quantities(self):
        '''
        This updates the quantities of items owned in the item helper tree. This makes sure the number stays accurate as items are gained (or lost) during runtime
        Usually called when scraping forge.
        '''
        self.item_recipe_tree.update_quantities(self.db)



    @qasync.asyncSlot()
    async def populate_item_location_table(self, item_ids: set[int]):
        '''
        Populates self.item_location_table with items that are in self.item_recipe_tree
        '''
        CustomPyQt.populate_drop_table(self.item_location_table, self.db, item_ids)



    @qasync.asyncSlot()
    async def remove_recipe(self):
        '''
        Removes a product item and its recipe from self.item_recipe_tree
        Called when a user right clicks in self.item_recipe_tree and chooses "Remove This Recipe"
        '''
        self.item_recipe_tree.remove_recipe()
        await self.populate_item_location_table(self.item_recipe_tree.map.keys())

        # save to settings
        settings = {'item_helper': self.item_recipe_tree.get_product_ids()}
        util.save_settings(self.account, settings)



    @qasync.asyncSlot()
    async def set_world_mission(self):
        '''
        Sets the world mission to the selected item in self.item_location_table
        Called when the user right clicks in self.item_location_table and clicks "Set As World Mission"
        '''
        # this should also probably change the world behavior mode to manual whenever i implement those features
        row = self.item_location_table.currentRow()
        url = self.item_location_table.item(row, 3).text()
        self.world_mission_text.setText(url)
        new_settings = util.save_settings(self.account, {'mission_url': url})
        await self.bot.update_settings(new_settings)






    ######################################################################################################################################
    # small simple functions to change various labels in the UI
    # most of these are only called by EdoTensei via signal
    ######################################################################################################################################

    @qasync.asyncSlot(str)
    async def set_team_label(self, name: str):
        self.team_label.setText(name)

    @qasync.asyncSlot()
    async def update_loop_label(self):
        count = int(self.loop_count_label.text()) + 1
        self.loop_count_label.setText(str(count))

    @qasync.asyncSlot()
    async def update_error_label(self):
        count = int(self.loop_error_label.text()) + 1
        self.error_count_label.setText(str(count))

    @qasync.asyncSlot(int)
    async def update_gold_labels(self, new_curr: int):
        old_curr = int(self.gold_current_label.text())
        self.gold_current_label.setText(str(new_curr))

        if self.gold_gained_label.text():
            old_gained = int(self.gold_gained_label.text())
            new_gained = old_gained + (new_curr - old_curr)
            self.gold_gained_label.setText(f'+{new_gained}')
        else:
            self.gold_gained_label.setText(f'+0')

    @qasync.asyncSlot(bool)
    async def update_world_labels(self, win: bool):
        if win:
            count = int(self.world_wins_label.text()) + 1
            self.world_wins_label.setText(str(count))
        else:
            count = int(self.world_losses_label.text()) + 1
            self.world_losses_label.setText(str(count))

    @qasync.asyncSlot(bool)
    async def update_arena_labels(self, win: bool):
        if win:
            count = int(self.arena_wins_label.text()) + 1
            self.arena_wins_label.setText(str(count))
        else:
            count = int(self.arena_losses_label.text()) + 1
            self.arena_losses_label.setText(str(count))

    @qasync.asyncSlot(str)
    async def update_items_table(self, name: str):
        cell = self.items_gained_table.findItems(name, Qt.MatchFixedString)
        if cell:    # edit an existing table entry if it exists
            row = self.items_gained_table.row(cell[0])
            qty_cell = self.items_gained_table.itemAt(row, 0)
            qty_cell.setText(str(int(qty_cell.text())+1))
        else:       # make a new table entry if one doesn't yet exist
            row = self.items_gained_table.rowCount()
            self.items_gained_table.insertRow(row)
            self.items_gained_table.setItem(row, 0, QTableWidgetItem('1'))
            self.items_gained_table.setItem(row, 1, QTableWidgetItem(name))

    @qasync.asyncSlot(object)
    async def add_ninja_card(self, ninja_card: EdoTensei.NinjaCard):
        # note that this only ADDS and will not update existing cards
        self.ninja_info_area.addWidget(ninja_card)











class MainWindow(QMainWindow, gui.main_window.Ui_MainWindow):
    '''
    The main window that has a QTabWidget which then has instances of MainFrame of type QFrame
    Basically, each browser UI is a QFrame which then gets placed into this QMainWindow
    As such, this doesn't have that much logic in it, most of the logci will be held in the MainFrames
    '''
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        '''
        Creates the MainFrame instances for each account and then adds them to the appropriate tab
        '''
        self.account_1_gui = MainFrame('account_1')
        self.account_1_layout = QGridLayout(self.account_1_tab)
        self.account_1_layout.addWidget(self.account_1_gui)

        self.account_2_gui = MainFrame('account_2')
        self.account_2_layout = QGridLayout(self.account_2_tab)
        self.account_2_layout.addWidget(self.account_2_gui)

    @qasync.asyncClose
    async def closeEvent(self, event):
        '''
        Gracefully shuts down both bots
        This is a feature of qasync that triggers whenever the program is closed

        Args:
            event (PyQt5.QtGui.QCloseEvent)
        '''
        await self.account_1_gui.bot.shutdown()
        await self.account_2_gui.bot.shutdown()






async def main():
    '''
    required by qasync
    '''
    def close_future(future, loop):
        loop.call_later(10, future.cancel)
        future.cancel()

    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    app = qasync.QApplication.instance()
    if hasattr(app, "aboutToQuit"):
        getattr(app, "aboutToQuit").connect(functools.partial(close_future, future, loop))

    window = MainWindow()
    window.show()

    await future
    return True



def suppress_logs():
    '''
    this suppresses the excessive amount of logs printed to console/stdout by arsenic
    '''
    logger = logging.getLogger('arsenic')
    def logger_factory():
        return logger
    structlog.configure(logger_factory=logger_factory)
    logger.setLevel(logging.WARNING)



if __name__ == '__main__':
    try:
        suppress_logs()
        qasync.run(main())
    except asyncio.exceptions.CancelledError:
        sys.exit(0)