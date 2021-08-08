from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
import json

class Colors:
    RED = QPalette()
    RED.setColor(QPalette.WindowText, Qt.red)

async def get_account() -> dict:
    with open('login.json', 'r') as file:
        account = json.load(file)
    return account