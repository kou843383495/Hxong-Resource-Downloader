import asyncio
import queue
from asyncio import get_running_loop
from pathlib import Path

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import InputMessagesFilterDocument

from ResourceCheck import tgDownloadCheck
from setting import SETTING


def TgDownloader():

    q = queue.Queue()


    exist_files = [f.name for f in SETTING.DOWNLOAD_DIR.iterdir()]

    client = TelegramClient(StringSession(SETTING.SESSION),int(SETTING.API_ID),SETTING.API_HASH)


    async def downloadFile():
        try:
            message = q.get()
        except queue.Empty:
            print(f'current download list is empty')
            return
        try:
            async with asyncio.timeout(None) as tm:
                print('start download', message.file.name)
                downloadPath = await message.download_media(file=str(SETTING.DOWNLOAD_DIR),
                                                            progress_callback=lambda r, t: (print(message.file.name, r / t),tm.reschedule(get_running_loop().time()+60*10)))
        except TimeoutError:
            print(f'{message.file.name} is no respond for 10 min, it will be restart')
            downloadPath = SETTING.DOWNLOAD_DIR / message.file.name
            downloadPath.unlink(missing_ok=True)
            q.put(message)
            return
        tgDownloadCheck(Path(downloadPath))


    async def main():

        print(client.session.save())
        if SETTING.SESSION is None:
            SETTING.SESSION = client.session.save()

        SETTING.saveSetting()

        channelId = None
        channelName = None

        async for channel in client.iter_dialogs():
            if input(f'{channel.name} is the channel or conversation you want find resources? please type yes to confirm: ') == 'yes':
                channelId = channel.id
                channelName = channel.name
                break

        assert channelId is not None , 'No channel or conservation be chosen'

        print(f'That you chosen ${channelName}')

        searchStr = None

        if input('Do You want to use keyword for search message? please type yes if you want: ') == 'yes':
            searchStr = input('The keywords:')

        messages = await client.get_messages(channelId,search=searchStr,filter=InputMessagesFilterDocument,limit=None)

        print(f'There a total ${messages.total} message have document, and total size is ${(sum([_.file.size for _ in messages])/(1024 ** 3)):.2f}GB')


        noDownloadMessages = [message for message in messages if message.file.name.split('.')[0] not in exist_files]

        print(f'There a total ${len(noDownloadMessages)} message not download, and total size is ${(sum([__.file.size for __ in noDownloadMessages])/(1024 ** 3)):.2f}GB')

        assert len(noDownloadMessages) != 0, 'There no resource can download'

        print('How many resource you want to download?')


        while True:
            temp = input('Please input a valid number:')
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

        print('How many resource you want to download at the same time?')

        while True:
            temp = input('Please input a valid number:')
            try:
                if int(temp) in range(1, 11):
                    downloadSameTimeNum = int(temp)
                    break
                else:
                    print('The number not in range (1-10)')
            except ValueError:
                print('input number not valid')



        while not q.empty():
            tasks = [downloadFile() for _ in range(downloadSameTimeNum)]

            L = await asyncio.gather(
                *tasks
            )

        print(f"finished")

    with client:
        client.loop.run_until_complete(main())

