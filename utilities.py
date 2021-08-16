from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
import json

class Colors:
    RED = QPalette()
    RED.setColor(QPalette.WindowText, Qt.red)

def load_settings(account: str) -> dict():
    with open('settings.json', 'r') as file:
        settings = json.load(file)
    return settings[account]