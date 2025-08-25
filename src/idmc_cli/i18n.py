import yaml
from pathlib import Path

I18N_DIR = Path('config')
I18N_FILE = I18N_DIR / 'i18n.yaml'

class I18n:
    def __init__(self):
        self.i18n_path = I18N_FILE
        self.data = {}
        self.load()

    def load(self):
        if self.i18n_path.exists():
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