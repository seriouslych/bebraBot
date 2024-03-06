import telebot
from telebot import types
import re
import os
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError


print("[bebraBot] Инициализация...")

token = '6617343138:AAGnQAWgJAYQdHGKN_sAWgk9q5R-2r7wBDs'

try:
    bot = telebot.TeleBot(token)
    print("[bebraBot] Инициализировано!")
except:
    print("[ОШИБКА] Инициализация прошла безуспешно :(\nВозможно вы ввели неправильный токен.")

@bot.message_handler(commands=['start', 'help'])
def on(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    help = types.KeyboardButton('/help')
    bebra = types.KeyboardButton('/bebra')
    vid_c = types.KeyboardButton('/vid')
    markup.add(help, bebra, vid_c)
    start(message)
def start(message):
    bot.reply_to(message, "Бот который умеет делать всякие вещи.\n\n<b>Команды бота:</b>\n/start и /help - помощь\n/bebra - бебрить\n/vid [ссылка] - скачивать видео с ютуба", parse_mode='html')
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
def url(message):
    if len(message.text.split()) > 1:
        url = f'{message.text.split(maxsplit=1)[1]}'
        try:
            yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
            vid = yt.title
        except AgeRestrictedError:
            print("[ОШИБКА] Видео имеет ограничение по возрасту :(")
            bot.reply_to(message, "❌ Ошибка скачивания :(\nСкорее всего видео имеет ограничение по возрасту.")
            return
        download(url, message, yt, vid)

def download(url, message, yt, vid):
    print(f"[@{message.from_user.username}] Скачивание видео...\n {vid}")
    yt.streams.filter(progressive=True, file_extension='mp4')
    video = yt.streams.get_by_itag(22)
    bot.reply_to(message, f"⏩ Отправка {vid}...")
    save = "yt/"
    try:
        video.download(save)
    except:
        print(f"[ОШИБКА] Ошибка скачивания :(")
        bot.reply_to(message, "❌ Ошибка скачивания :(")
    else:
        print(f"[@{message.from_user.username}] Видео скачано!")
        bot.send_message(message.chat.id, "✅ Готово!")
        clean_and_send(message, vid)

def clean_and_send(message, vid):
    sanitized_vid = clean(vid)
    send(message, sanitized_vid)

def clean(vid):
    sanitized_vid = re.sub(r'[\\/:"*?<>|,]+', '', vid)
    sanitized_vid = sanitized_vid.replace("'", "").replace('"', '')
    sanitized_vid = sanitized_vid.strip()
    return sanitized_vid
      
def send(message, vid):
    pvid = f"D:/!Projects/Bots/Telegram/bebraBot/yt/{vid}.mp4"
    bot.send_video(message.chat.id, open(pvid, 'rb'), supports_streaming=True, width=1920, height=1080)
    print("[bebraBot] Очистка...")
    os.remove(pvid)
    print("[bebraBot] Ожидание команд...")


print("[bebraBot] Ожидание команд...")
bot.infinity_polling()