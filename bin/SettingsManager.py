# SettingsManager.py

import os
import json

class SettingsManager:
    def __init__(self):
        self.settings_file = os.path.join(os.environ['APPDATA'], 'ECP Apps', 'QuickImageSorterSettings.json')
        self.settings = {"show_filenames": True}
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as file:
                self.settings = json.load(file)
    
    def save_settings(self):
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        with open(self.settings_file, 'w') as file:
            json.dump(self.settings, file, indent=4)
    
    def get_setting(self, key):
        return self.settings.get(key, None)

    def set_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()
