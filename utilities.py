from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
import json
from signals import Signals

class Colors:
    RED = QPalette()
    RED.setColor(QPalette.WindowText, Qt.red)

def load_settings(account: str) -> dict():
    with open('settings.json', 'r') as file:
        settings = json.load(file)
    return settings[account]

def save_settings(account: str, settings: dict) -> dict:
    with open('settings.json', 'r') as file:
        whole_settings = json.load(file)
    
    for key, val in settings.items():
        # only change certain settings, not all of them
        whole_settings[account][key] = val

    with open('settings.json', 'w+') as file:
        json.dump(whole_settings, file, indent=4)
    
    return whole_settings

def save_notes(account: str, notes: str):
    with open('settings.json', 'r') as file:
        whole_settings = json.load(file)
    
    whole_settings[account]['notes'] = notes

    with open('settings.json', 'w+') as file:
        json.dump(whole_settings, file, indent=4)