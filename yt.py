import asyncio
from yt_dlp import YoutubeDL
import glob


async def download_type(url):
    save_options = {
        'outtmpl': 'D:/!Projects/Bots/Telegram/git.bebraBot/bebraBot/yt/%(title)s.%(ext)s',
    }
    loop = asyncio.get_event_loop()
    with YoutubeDL(save_options) as ydl:
        await loop.run_in_executor(None, ydl.download, [url])  # Асинхронный вызов ydl.download
        downloaded_files = glob.glob('D:/!Projects/Bots/Telegram/git.bebraBot/bebraBot/yt/*')
        if downloaded_files:
            filename = downloaded_files[-1]
            return filename
        else:
            return None
