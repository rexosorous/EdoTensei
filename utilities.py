# standard python modules
import json

# dependencies
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette



'''
A utility file that holds simple functions
'''



class Colors:
    RED = QPalette()
    RED.setColor(QPalette.WindowText, Qt.red)



def load_settings(account: str) -> dict():
    '''
    Reads from settings.json and returns ONLY the settings for a specific account

    Args:
        account (str): should either be 'account_1' or 'account_2'

    Returns:
        dict
    '''
    with open('settings.json', 'r') as file:
        settings = json.load(file)
    return settings[account]



def save_settings(account: str, settings: dict) -> dict:
    '''
    Writes to settings.json with the new settings

    Args:
        settings (dict): does NOT need to be the full settings dict. can be a partial/incomplete dict and
                         this only overwrite the fields given to it

    Returns:
        dict: the WHOLE updated settings
    '''
    with open('settings.json', 'r') as file:
        whole_settings = json.load(file)

    for key, val in settings.items():
        # only change certain settings, not all of them
        whole_settings[account][key] = val

    with open('settings.json', 'w+') as file:
        json.dump(whole_settings, file, indent=4)

    return whole_settings[account]