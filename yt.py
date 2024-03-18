import asyncio
from yt_dlp import YoutubeDL
import glob


async def download_vid(url):
    save_options = {
        'outtmpl': 'D:/!Projects/Bots/Telegram/git.bebraBot/bebraBot/yt/%(title)s.%(ext)s',
    }
    try:
        with YoutubeDL(save_options) as ydl:
            ydl.download([url])
            # Возвращаем имя последнего скачанного файла
            downloaded_files = glob.glob('D:/!Projects/Bots/Telegram/git.bebraBot/bebraBot/yt/*')
            if downloaded_files:
                return downloaded_files[-1]
            else:
                raise ValueError("Не удалось найти скачанный файл")
    except Exception as e:
        print(f"[ОШИБКА] Ошибка скачивания: {e}")
        return None

    
                    
async def download_audio(url):
    save_options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '328',
        }],
        'outtmpl': 'D:/!Projects/Bots/Telegram/git.bebraBot/bebraBot/audio/%(title)s.%(ext)s',
        'ffmpeg_location': 'D:/!Projects/Bots/Telegram/git.bebraBot/bebraBot/ffmpeg'
    }
    loop = asyncio.get_event_loop()
    with YoutubeDL(save_options) as ydl:
        await loop.run_in_executor(None, ydl.download, [url])
        downloaded_files = glob.glob('D:/!Projects/Bots/Telegram/git.bebraBot/bebraBot/audio/*')
        if downloaded_files:
            filename = downloaded_files[-1]
            return filename
        else:
            return None