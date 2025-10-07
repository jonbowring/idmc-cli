import yaml
import sys
from pathlib import Path

CLASS_PATH = Path(__file__)
I18N_PATH = 'config/i18n.yaml'

class I18n:
    def __init__(self):
        
        if hasattr(sys, '_MEIPASS'):
            # Running from a onefile PyInstaller bundle
            relative_path = Path(I18N_PATH)
            base_path = Path(sys._MEIPASS)
            self.i18n_path = base_path / relative_path
        else:
            # Running from source
            self.i18n_path = CLASS_PATH.parent / I18N_PATH

        self.data = {}
        self.load()

    def load(self):
        if self.i18n_path.is_file():
            with open(self.i18n_path, 'r') as f:
                self.data = yaml.load(f, Loader=yaml.SafeLoader)

    def get(self):
        return self.data
    
    def getHelpOption(self, command, sub_command, option):
        if sub_command:
            option = self.data['english']['help'][command][sub_command]['options'][option]
        else:
            option = self.data['english']['help'][command]['options'][option]
        
        return option
    
    def getErrorText(self, command, sub_command, error):
        if sub_command:
            error = self.data['english']['help'][command][sub_command]['errors'][error]
        else:
            error = self.data['english']['help'][command]['errors'][error]
        
        return error

# Expose the class as a variable
i18n = I18n()