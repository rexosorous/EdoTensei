# dependencies
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFrame, QGridLayout, QTableWidgetItem
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
import DBHandler



class Main_Frame(QFrame, gui.main_frame.Ui_Frame):
    def __init__(self, account: str):
        # account should be "account_1" or "account_2"
        super().__init__()
        self.setupUi(self)
        self.db = DBHandler.DBHandler(account)
        self.sigs = signals.Signals()
        self.bot = EdoTensei.EdoTensei(self.db, self.sigs, account)
        self.connect_events()
        self.init_labels()



    def connect_events(self):
        self.launch_button.clicked.connect(self.launch_or_close)
        self.start_button.clicked.connect(self.start_or_pause)
        self.sigs.update_loop_count.connect(self.update_loop_label)
        self.sigs.update_error_count.connect(self.update_error_label)
        self.sigs.update_gold.connect(self.update_gold_labels)
        self.sigs.update_world_stats.connect(self.update_world_labels)
        self.sigs.update_arena_stats.connect(self.update_arena_labels)
        self.sigs.update_items_gained.connect(self.update_items_table)
        self.sigs.add_ninja_card.connect(self.add_ninja_card)



    def init_labels(self):
        self.loop_count_label.setText('0')
        self.error_count_label.setText('0')
        self.gold_current_label.setText('0')
        # self.gold_gained_label.setText('+0')
        self.world_wins_label.setText('0')
        self.world_losses_label.setText('0')
        self.arena_wins_label.setText('0')
        self.arena_losses_label.setText('0')



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



    # updating labels and such
    @qasync.asyncSlot()
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
    async def add_ninja_card(self, ninja_card: EdoTensei.Ninja_Card):
        # note that this only ADDS and will not update existing cards
        self.ninja_info_area.addWidget(ninja_card)











class Main_Window(QMainWindow, gui.main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.account_1_gui = Main_Frame('account_1')
        self.account_1_layout = QGridLayout(self.account_1_tab)
        self.account_1_layout.addWidget(self.account_1_gui)

        self.account_2_gui = Main_Frame('account_2')
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

    window = Main_Window()
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