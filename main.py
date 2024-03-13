import telebot
import os
import asyncio
from yt import download_type

print("[bebraBot] Инициализация...")

token = 'YOUR_API_KEY'

try:
    bot = telebot.TeleBot(token)
    print("[bebraBot] Инициализировано!")
except Exception as e:
    print(f"[ОШИБКА] Инициализация прошла безуспешно: {e}")


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message,
                 """
                 Бот который умеет делать всякие вещи.\n\n<b>Команды бота:</b>\n/start и /help - помощь\n
                 /bebra - бебрить\n/vid [ссылка] - скачивать видео с ютуба
                 """,
                 parse_mode='html')
    print(f"[@{message.from_user.username}] Команда start/help:\nОтправлена помощь.")
    print("[bebraBot] Ожидание команд...")


@bot.message_handler(commands=['bebra'], content_types=['text'])
def bebra(message):
    photo = open('ph/1.jpg', 'rb')
    print(f"[@{message.from_user.username}] Команда bebra:\nОтправлена бебра.")
    bot.send_photo(message.chat.id, photo, caption='bebra')
    photo.close()
    print("[bebraBot] Ожидание команд...")


@bot.message_handler(commands=['t'])
def t(message):
    bot.reply_to(message, "test")


@bot.message_handler(commands=['vid'])
def run(message):
    asyncio.run(handle_vid_command(message))


async def handle_vid_command(message):
    if len(message.text.split()) > 1:
        url = f'{message.text.split(maxsplit=1)[1]}'
        bot.reply_to(message, f"⏩ Отправка {url}...", disable_web_page_preview=True)
        filename = await download_type(url)
        if filename:
            print(f"[@{message.from_user.username}] Видео скачано!")
            with open(filename, 'rb') as video_file:
                bot.send_video(message.chat.id, video_file)
            bot.send_message(message.chat.id, "✅ Готово!")
            print("[bebraBot] Очистка...")
            os.remove(filename)
            print("[bebraBot] Ожидание команд...")
        else:
            bot.reply_to(message, "❌ Ошибка скачивания видео :(")


bot.infinity_polling()
