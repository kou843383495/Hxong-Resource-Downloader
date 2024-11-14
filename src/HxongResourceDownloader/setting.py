import json
from pathlib import Path


class Setting:
    def __init__(self,settingFilePath:str = 'TgSetting.json'):
        if Path(settingFilePath).exists():
            tg_setting = json.load(open(settingFilePath, 'r'))
            self.API_ID = tg_setting['API_ID'] if 'API_ID' in tg_setting else None
            self.API_HASH = tg_setting['API_HASH'] if 'API_HASH' in tg_setting else None
            self.SESSION = tg_setting['SESSION'] if 'SESSION' in tg_setting else None
            self.DOWNLOAD_DIR = Path(tg_setting['DOWNLOAD_DIR'])
            self.PASSWORDS = tg_setting['PASSWORDS'] if 'PASSWORDS' in tg_setting else None
        else:
            self.API_ID = input('Please input the telegram API_ID ')
            self.API_HASH = input('Please input the telegram API_HASH ')
            self.DOWNLOAD_DIR = Path(input('Please input the dir you want to save file. Type . if you want save current folder '))
            self.PASSWORDS = input('Please input the possible passwords.Can be multiple. ').split(' ')
            self.SESSION = None
            self.saveSetting()

    def reloadSettingFile(self,settingFilePath:str):
        self.__init__(settingFilePath = settingFilePath)

    def saveSetting(self):
        with open('TgSetting.json','w') as f:
            _ = self.__dict__.copy()
            _['DOWNLOAD_DIR'] = str(_['DOWNLOAD_DIR'])
            json.dump(_,f)


SETTING = Setting()
