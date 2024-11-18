import asyncio
import queue
import sys
from asyncio import get_running_loop
from contextlib import redirect_stdout
from pathlib import Path

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import InputMessagesFilterDocument
from tqdm import tqdm

from HxongResourceDownloader.Excepation.FileExcepation import NoFindSuitablePasswordError
from HxongResourceDownloader.download_resource_check import check_file
from HxongResourceDownloader.setting import SETTING


def tg_downloader():

    q = queue.Queue()


    exist_files = [f.name for f in SETTING.DOWNLOAD_DIR.iterdir()]

    client = TelegramClient(StringSession(SETTING.SESSION),int(SETTING.API_ID),SETTING.API_HASH)



    async def download_file(progress_position:int,total_bar):
        progressBar = tqdm(position=progress_position,unit_scale=True,unit_divisor=1024*1024)
        while not q.empty():
            try:
                message = q.get()
            except queue.Empty:
                progressBar.close()
                break
            progressBar.reset(total=message.file.size)
            progressBar.set_description_str(message.file.name.split('.')[0])
            try:
                async with asyncio.timeout(None) as tm:
                    def progressMonitor(r, t):
                        progressBar.update(r - progressBar.n)
                        tm.reschedule(get_running_loop().time() + 60 * 10)
                    downloadPath = await message.download_media(file=str(SETTING.DOWNLOAD_DIR),progress_callback=progressMonitor)
                    check_file(Path(downloadPath))
                    total_bar.update()
            except Exception as e:
                if type(e) is TimeoutError:
                    downloadPath = SETTING.DOWNLOAD_DIR / message.file.name
                    downloadPath.unlink(missing_ok=True)
                    q.put(message)
                elif type(e) is NoFindSuitablePasswordError:
                    pass
                else:
                    raise e
                break


    async def main():

        if SETTING.SESSION is None:
            SETTING.SESSION = client.session.save()

        SETTING.save_setting()

        channelId = None
        channelName = None

        async for channel in client.iter_dialogs():
            if input(f'{channel.name} is the channel or conversation you want find resources? please type yes to confirm: ') == 'yes':
                channelId = channel.id
                channelName = channel.name
                break

        assert channelId is not None , 'No channel or conservation be chosen'

        print(f'That you chosen {channelName}')

        searchStr = None

        if input('Do You want to use keyword for search message? please type yes if you want: ') == 'yes':
            searchStr = input('The keywords:')

        messages = await client.get_messages(channelId,search=searchStr,filter=InputMessagesFilterDocument,limit=None)

        print(f'There a total {messages.total} message have document, and total size is {(sum([_.file.size for _ in messages])/(1024 ** 3)):.2f}GB')


        noDownloadMessages = [message for message in messages if message.file.name.split('.')[0] not in exist_files and message.file.name.split('.')[0] not in exist_files]

        print(f'There a total {len(noDownloadMessages)} message not download, and total size is {(sum([__.file.size for __ in noDownloadMessages])/(1024 ** 3)):.2f}GB')

        assert len(noDownloadMessages) != 0, 'There no resource can download'



        while True:
            temp = input('How many resource you want to download?: ')
            try:
                if int(temp) in range(1,len(noDownloadMessages)+1):
                    downloadNum = int(temp)
                    break
                else:
                    print('The number outer the range of valid number compare to the message')
            except ValueError:
                print('input number not valid')


        for _ in range(downloadNum):
            q.put(noDownloadMessages[_])


        while True:
            temp = input('How many resource you want to download at the same time?: ')
            try:
                if int(temp) in range(1, 11):
                    downloadSameTimeNum = int(temp)
                    break
                else:
                    print('The number not in range (1-10)')
            except ValueError:
                print('input number not valid')

        total_progress_bar = tqdm(desc='Total resources will download')

        tasks = [download_file(_+1,total_progress_bar) for _ in range(downloadSameTimeNum)]

        L = await asyncio.gather(
            *tasks
        )

        total_progress_bar.close()

        print(f"finished")

    with client:
        client.loop.run_until_complete(main())

