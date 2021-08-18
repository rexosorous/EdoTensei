# dependencies
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFrame, QGridLayout, QTableWidgetItem, QMenu, QAction, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QPixmap, QPalette
import qasync

import sys
import asyncio
import functools
import logging
import structlog

import gui.main_window
import gui.main_frame
import gui.ninja_card_frame
import EdoTensei
import signals
import utilities as util
from DBHandler import DBHandler
from RecipeWindow import RecipeWindow



class MainFrame(QFrame, gui.main_frame.Ui_Frame):
    def __init__(self, account: str):
        # account should be "account_1" or "account_2"
        super().__init__()
        self.setupUi(self)
        self.db = DBHandler(account)
        self.sigs = signals.Signals()
        self.bot = EdoTensei.EdoTensei(self.db, self.sigs)
        self.recipe_window = RecipeWindow(self.db, self.sigs)
        self.account = account
        self.init_labels()
        self.create_context_menus()
        self.connect_events()
        self.load_settings()



    def init_labels(self):
        self.loop_count_label.setText('0')
        self.error_count_label.setText('0')
        self.gold_current_label.setText('0')
        # self.gold_gained_label.setText('+0')
        self.world_wins_label.setText('0')
        self.world_losses_label.setText('0')
        self.arena_wins_label.setText('0')
        self.arena_losses_label.setText('0')



    def create_context_menus(self):
        self.item_recipe_tree.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.item_recipe_tree.open_ = QAction("Add Recipes", self.item_recipe_tree)
        self.item_recipe_tree.remove = QAction("Remove This Recipe", self.item_recipe_tree)
        self.item_recipe_tree.addAction(self.item_recipe_tree.open_)
        self.item_recipe_tree.addAction(self.item_recipe_tree.remove)
        self.item_recipe_tree.open_.triggered.connect(self.open_recipe_window)
        self.item_recipe_tree.remove.triggered.connect(self.remove_recipe)

        self.item_location_table.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.item_location_table.set_mission = QAction("Set As World Mission", self.item_location_table)
        self.item_location_table.addAction(self.item_location_table.set_mission)
        self.item_location_table.set_mission.triggered.connect(self.set_world_mission)



    def connect_events(self):
        self.launch_button.clicked.connect(self.launch_or_close)
        self.start_button.clicked.connect(self.start_or_pause)
        self.reset_settings_button.clicked.connect(self.load_settings)
        self.submit_settings_button.clicked.connect(self.save_settings)
        self.notes_textbox.textChanged.connect(self.save_notes)
        self.sigs.set_team_label.connect(self.set_team_label)
        self.sigs.update_loop_count.connect(self.update_loop_label)
        self.sigs.update_error_count.connect(self.update_error_label)
        self.sigs.update_gold.connect(self.update_gold_labels)
        self.sigs.update_world_stats.connect(self.update_world_labels)
        self.sigs.update_arena_stats.connect(self.update_arena_labels)
        self.sigs.update_items_gained.connect(self.update_items_table)
        self.sigs.add_ninja_card.connect(self.add_ninja_card)
        self.sigs.add_to_item_helper.connect(self.add_to_item_helper)



    @qasync.asyncSlot()
    async def launch_or_close(self):
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
        if self.bot.state == EdoTensei.State.RUNNING:
            self.start_button.setIcon(QIcon('./icons/pause.png'))
            self.status_info_label.setText('manually paused')
            # self.bot.pause()
        elif self.bot.state == EdoTensei.State.PAUSED:
            self.start_button.setIcon(QIcon('./icons/start.png'))
            # self.bot.resume()



    @qasync.asyncSlot()
    async def load_settings(self):
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
        for item_id in settings['item_helper']:
            item_name = self.db.get_item_name(item_id)
            product_owned_qty = self.db.get_owned_qty(item_id)
            product_needed_qty = '0' if product_owned_qty else '1' 
            product_widget = QTreeWidgetItem([item_name, '1', str(product_owned_qty), product_needed_qty])
            await self.build_recipe(product_widget, item_id)
            self.item_recipe_tree.addTopLevelItem(product_widget)
        self.item_recipe_tree.expandAll()
        await self.populate_item_location_table()



    @qasync.asyncSlot()
    async def save_settings(self):
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
        util.save_notes(self.account, self.notes_textbox.toPlainText())



    @qasync.asyncSlot()
    async def open_recipe_window(self):
        await self.recipe_window.open()



    @qasync.asyncSlot(str)
    async def add_to_item_helper(self, item_name: str):
        item_id = self.db.get_item_id(item_name)
        product_owned_qty = self.db.get_owned_qty(item_id)
        product_needed_qty = '0' if product_owned_qty else '1' 
        product_widget = QTreeWidgetItem([item_name, '1', str(product_owned_qty), product_needed_qty])
        await self.build_recipe(product_widget, item_id)
        self.item_recipe_tree.addTopLevelItem(product_widget)
        self.item_recipe_tree.expandAll()
        await self.populate_item_location_table()
    
        # save the newly added recipe to settings
        item_helper_ids = []
        for index in range(self.item_recipe_tree.topLevelItemCount()):
            item_name = self.item_recipe_tree.topLevelItem(index).text(0)
            item_id = self.db.get_item_id(item_name)
            item_helper_ids.append(item_id)
        settings = {'item_helper': item_helper_ids}
        util.save_settings(self.account, settings)



    @qasync.asyncSlot(object, int)
    async def build_recipe(self, parent_widget, parent_item_id: int):
        data = self.db.get_item_recipe(parent_item_id) # should return id, name, qty needed to craft, qty owned
        if not data:
            return
        
        for ingredient in data:
            parent_needed_qty = int(parent_widget.text(3))
            craft_qty = ingredient[2]
            owned_qty = ingredient[3]
            needed_qty = (parent_needed_qty * craft_qty) - owned_qty
            if needed_qty < 0:
                needed_qty = 0
            child = QTreeWidgetItem(parent_widget, [str(x) for x in ingredient[1:]])
            child.setText(3, str(needed_qty))
            await self.build_recipe(child, ingredient[0])



    @qasync.asyncSlot()
    async def populate_item_location_table(self):
        while self.item_location_table.rowCount():
            self.item_location_table.removeRow(0)

        for index in range(self.item_recipe_tree.topLevelItemCount()):
            await self.add_location_entry(self.item_recipe_tree.topLevelItem(index), set())



    @qasync.asyncSlot(object)
    async def add_location_entry(self, tree_item: QTreeWidgetItem, already_added: set[str]) -> set[str]:
        item_name = tree_item.text(0)
        if item_name in already_added:
            return {item_name}
        already_added.add(item_name)

        location_data = self.db.get_item_drops_by_name(item_name)
        for data in location_data:
            last_row = self.item_location_table.rowCount()
            self.item_location_table.insertRow(last_row)
            fixed_location = data[3][data[3].find('area/')+5:] if 'area' in data[3] else data[3]
            self.item_location_table.setItem(last_row, 0, QTableWidgetItem(data[0]))
            self.item_location_table.setItem(last_row, 1, QTableWidgetItem(f'{data[1]}%'))
            self.item_location_table.setItem(last_row, 2, QTableWidgetItem(data[2]))
            self.item_location_table.setItem(last_row, 3, QTableWidgetItem(fixed_location))

        for index in range(tree_item.childCount()):
            already_added.update(await self.add_location_entry(tree_item.child(index), already_added))

        return already_added


    
    @qasync.asyncSlot()
    async def remove_recipe(self):
        selected_item = self.item_recipe_tree.currentItem()
        # get the top level item
        while selected_item.parent():
            selected_item = selected_item.parent()
        selected_item_index = self.item_recipe_tree.indexOfTopLevelItem(selected_item)
        self.item_recipe_tree.takeTopLevelItem(selected_item_index)
        await self.populate_item_location_table()

        # save to settings
        item_helper_ids = []
        for index in range(self.item_recipe_tree.topLevelItemCount()):
            item_name = self.item_recipe_tree.topLevelItem(index).text(0)
            item_id = self.db.get_item_id(item_name)
            item_helper_ids.append(item_id)
        settings = {'item_helper': item_helper_ids}
        util.save_settings(self.account, settings)



    @qasync.asyncSlot()
    async def set_world_mission(self):
        # this should also probably change the world behavior mode to manual whenever i implement those features
        row = self.item_location_table.currentRow()
        url = self.item_location_table.item(row, 3).text()
        self.world_mission_text.setText(url)
        new_settings = util.save_settings(self.account, {'mission_url': url})
        self.bot.update_settings(new_settings)


        



    # updating labels and such
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
        if cell:
            row = self.items_gained_table.row(cell[0])
            qty_cell = self.items_gained_table.itemAt(row, 0)
            qty_cell.setText(str(int(qty_cell.text()+1)))
        else:
            row = self.items_gained_table.rowCount()
            self.items_gained_table.insertRow(row)
            self.items_gained_table.setItem(row, 0, QTableWidgetItem('1'))
            self.items_gained_table.setItem(row, 1, QTableWidgetItem(name))

    @qasync.asyncSlot(object)
    async def add_ninja_card(self, ninja_card: EdoTensei.NinjaCard):
        # note that this only ADDS and will not update existing cards
        self.ninja_info_area.addWidget(ninja_card)











class MainWindow(QMainWindow, gui.main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.account_1_gui = MainFrame('account_1')
        self.account_1_layout = QGridLayout(self.account_1_tab)
        self.account_1_layout.addWidget(self.account_1_gui)

        self.account_2_gui = MainFrame('account_2')
        self.account_2_layout = QGridLayout(self.account_2_tab)
        self.account_2_layout.addWidget(self.account_2_gui)

    @qasync.asyncClose
    async def closeEvent(self, event):
        await self.account_1_gui.bot.shutdown()
        await self.account_2_gui.bot.shutdown()






async def main():
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
    # this suppresses the excessive amount of logs printed to console/stdout
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