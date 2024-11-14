import argparse

from TgDownloader import TgDownloader

# Give the basic information about this tool in CLI
parser = argparse.ArgumentParser(
    prog='HxongResourceDownloader',
    description='This is a tool to help download some resource from some websites',
    epilog='More detail on the GitHub'
)



parser.add_argument('--setting',default='TgSetting.json')

args = vars(parser.parse_args())

try:
    TgDownloader()
except AssertionError as e:
    print(e)

