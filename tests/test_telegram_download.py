import builtins

from HxongResourceDownloader.setting import SETTING
from HxongResourceDownloader.telegram_download import tg_downloader


def mock_input(message:str):
    match message:
        case 'my_test_channel is the channel or conversation you want find resources? please type yes to confirm: ':
            return 'yes'
        case 'Do You want to use keyword for search message? please type yes if you want: ':
            return 'no'
        case 'How many resource you want to download?: ':
            return 3
        case 'How many resource you want to download at the same time?: ':
            return 2
        case _:
            return 3

class TestTelegramDownload:

    def test_tg_downloader(self,tmp_path,monkeypatch):
        SETTING.DOWNLOAD_DIR = tmp_path
        monkeypatch.setattr(builtins,'input',mock_input)
        tg_downloader()