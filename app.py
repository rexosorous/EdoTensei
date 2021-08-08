# dependencies
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFrame, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap, QPalette
import qasync

import sys
import asyncio
import functools

import gui.main_window
import gui.main_frame
import gui.ninja_card_frame
import EdoTensei
import signals
import utilities as util



class Ninja_Card(QFrame, gui.ninja_card_frame.Ui_Frame):
    def __init__(self, ninja_info):
        super().__init__()
        self.setupUi(self)
        self.image.setPixmap(QPixmap(f'./{ninja_info.image_dir}'))
        self.ninja_name.setText(ninja_info.name)
        self.ninja_exp.setText(f'Lv.{int(ninja_info.exp/100)}@{ninja_info.exp%100}%')
        self.ninja_exp_gain.setText('+0%')
        self.bl_name.setText(ninja_info.BL_name)
        self.bl_exp.setText(f'Lv.{int(ninja_info.BL_exp/100)}@{ninja_info.BL_exp%100}%')
        self.bl_exp_gain.setText('+0%')










class Main_Frame(QFrame, gui.main_frame.Ui_Frame):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sigs = signals.Signals()
        self.bot = EdoTensei.EdoTensei(self.sigs)
        self.connect_events()



    def connect_events(self):
        self.launch_button.clicked.connect(self.launch_or_close)
        self.start_button.clicked.connect(self.start_or_pause)
        self.sigs.ninja_signal.connect(self.add_ninja_card)



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



    def start_or_pause(self):
        if self.bot.state == EdoTensei.State.RUNNING:
            self.start_button.setIcon(QIcon('./icons/pause.png'))
            self.status_info_label.setText('manually paused')
            # self.bot.pause()
        elif self.bot.state == EdoTensei.State.PAUSED:
            self.start_button.setIcon(QIcon('./icons/start.png'))
            # self.bot.resume()



    def add_ninja_card(self, ninja_info):
        # note that this only ADDS and will not update existing cards
        new_card = Ninja_Card(ninja_info)
        self.ninja_info_area.addWidget(new_card)











class Main_Window(QMainWindow, gui.main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.chrome_gui = Main_Frame()
        self.chrome_layout = QGridLayout(self.chrome_tab)
        self.chrome_layout.addWidget(self.chrome_gui)

    @qasync.asyncClose
    async def closeEvent(self, event):
        await self.chrome_gui.bot.shutdown()
        






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



if __name__ == '__main__':
    try:
        qasync.run(main())
    except asyncio.exceptions.CancelledError:
        sys.exit(0)