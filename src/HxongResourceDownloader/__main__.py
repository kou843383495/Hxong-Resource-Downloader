import argparse

from .telegram_download import tg_downloader

# Give the basic information about this tool in CLI
parser = argparse.ArgumentParser(
    prog='HxongResourceDownloader',
    description='This is a tool to help download some resource from some websites',
    epilog='More detail on the GitHub'
)



parser.add_argument('--setting',default='TgSetting.json')

args = vars(parser.parse_args())

try:
    tg_downloader()
except AssertionError as e:
    print(e)

