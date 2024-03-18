import telebot
from telebot import types
import os
import asyncio
import requests
from yt import download_vid
from yt import download_audio
from stk import stk_convert  # Подключение необходимых модулей

print("[bebraBot] Инициализация...")

token = 'TOKEN'  # Здесь следует указать токен вашего бота

try:
    bot = telebot.TeleBot(token)
    print("[bebraBot] Инициализировано!")
except Exception as e:
    print(f"[ОШИБКА] Инициализация прошла безуспешно: {e}")

# Словарь для отслеживания статуса ожидания изображения
waiting_for_image = {}


@bot.message_handler(commands=['start', 'help'])
def start(message):
    # Обработчик команд /start и /help для отправки помощи пользователю
    bot.reply_to(message,
                 """
                 Бот который умеет делать всякие вещи.\n\n<b>Команды бота:</b>
    /start и /help - помощь
    /bebra - бебрить
    /vid [ссылка] - скачивать видео с ютуба
    /aud [ссылка] - скачивать аудио с ютуба
    /stk - преобразование изображения в размер подходящий для стикера
                 """,
                 parse_mode='html')
    print(f"[@{message.from_user.username}] Команда start/help:\nОтправлена помощь.")
    print("[bebraBot] Ожидание команд...")


@bot.message_handler(commands=['bebra'], content_types=['text'])
def run_bebra(message):
    # Обработчик команды /bebra для отправки изображения с подписью "bebra"
    asyncio.run(bebra(message))


async def bebra(message):
    # Асинхронная функция отправки изображения "bebra"
    photo = open('ph/1.jpg', 'rb')
    print(f"[@{message.from_user.username}] Команда bebra:\nОтправлена бебра.")
    bot.send_photo(message.chat.id, photo, caption='bebra')
    photo.close()
    print("[bebraBot] Ожидание команд...")


@bot.message_handler(commands=['t'])
def t(message):
    # Обработчик команды /t для отправки ответа "test"
    bot.reply_to(message, "test")


@bot.message_handler(commands=['vid'])
def run_vid(message):
    # Обработчик команды /vid для скачивания и отправки видео с YouTube
    asyncio.run(vid(message))


async def vid(message):
    # Асинхронная функция скачивания и отправки видео с YouTube
    if len(message.text.split()) > 1:
        url = f'{message.text.split(maxsplit=1)[1]}'
        bot.reply_to(message, f"⏩ Отправка {url}...", disable_web_page_preview=True)
        filename = await download_vid(url)
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

@bot.message_handler(commands=['aud'])
def run_audio(message):
    # Обработчик команды /aud для скачивания и отправки аудио с YouTube
    asyncio.run(audio(message))


async def audio(message):
    # Асинхронная функция скачивания и отправки аудио с YouTube
    if len(message.text.split()) > 1:
        url = f'{message.text.split(maxsplit=1)[1]}'
        bot.reply_to(message, f"⏩ Отправка {url}...", disable_web_page_preview=True)
        filename = await download_audio(url)
        if filename:
            print(f"[@{message.from_user.username}] Аудио скачано!")
            with open(filename, 'rb') as audio_file:
                bot.send_audio(message.chat.id, audio_file)
            bot.send_message(message.chat.id, "✅ Готово!")
            print("[bebraBot] Очистка...")
            os.remove(filename)
            print("[bebraBot] Ожидание команд...")
        else:
            bot.reply_to(message, "❌ Ошибка скачивания аудио :(")


@bot.message_handler(commands=['stk'], content_types=['text'])
def stk(message):
    # Устанавливаем статус ожидания изображения для данного пользователя
    waiting_for_image[message.chat.id] = True

    cancel_inline = types.InlineKeyboardMarkup()
    item_cancel = types.InlineKeyboardButton(text='❌ Отмена', callback_data='cancel')
    cancel_inline.add(item_cancel)

    # Обработчик команды /stk для ожидания отправки изображения и сохранения его как стикера
    bot.reply_to(message, "🏞 Отправь мне изображение в ответ, чтобы обработать её как стикер",
                 reply_markup=cancel_inline
                 )
    print(f"[@{message.from_user.username}] Команда stk:\nОжидание изображения...")


@bot.callback_query_handler(func=lambda call: True)
def stk_cancel(call):
    chat_id = call.message.chat.id  # Получаем chat_id из сообщения обратного вызова

    if call.data == 'cancel':
        try:
            # Удалить сообщение, на которое был дан ответ
            bot.delete_message(chat_id, call.message.message_id)
            waiting_for_image[chat_id] = False
            print(f"[bebraBot] stk отменён")
        except Exception as e:
            print("[ОШИБКА] Ошибка при удалении сообщения:", e)


@bot.message_handler(content_types=['photo', 'text'])
def giving_photo(message):
    if message.reply_to_message:  # Проверяем, был ли отправлен ответ на предыдущее сообщение
        replied_message = message.reply_to_message
        # Обработчик отправленного изображения в ответ на команду /stk
        if replied_message.text and message.chat.id in waiting_for_image and waiting_for_image[message.chat.id]:
            if message.photo:  # Check if there's a photo in the message
                stk_id = message.photo[-1].file_id
                stk_info = bot.get_file(stk_id)
                stk_path = stk_info.file_path
                file_url = f"https://api.telegram.org/file/bot{token}/{stk_path}"

                file_name = f"{message.chat.id}.jpg"
                input_path = os.path.join('stk', file_name)  # Путь к входному файлу

                if not os.path.exists('stk'):
                    os.makedirs('stk')

                print(f"[@{message.from_user.username}] Изображение получено!\nСкачивание изображения...")
                response = requests.get(file_url)
                with open(input_path, 'wb') as f:
                    f.write(response.content)

                output_path = os.path.splitext(input_path)[0] + ".png"  # Путь к выходному файлу

                stk_convert(input_path, output_path)  # Вызываем функцию для конвертации

                last_message_id = bot.reply_to(message, "⏩ Конвертирование...").message_id
                print(f"[@{message.from_user.username}] Конвертация в стикер...")

                stk_send(message, input_path, output_path)

                if last_message_id:
                    bot.delete_message(message.chat.id, last_message_id)

                waiting_for_image[message.chat.id] = False
            else:
                bot.reply_to(message, "Отправь мне изображение в ответ, балбес >:(")


def stk_send(message, input_path, output_path):
    try:
        # Отправляем сконвертированное изображение пользователю как документ
        with open(output_path, 'rb') as doc:
            bot.send_document(message.chat.id, doc)

        print("[bebraBot] Изображение успешно сконвертировано и отправлено.")
        bot.reply_to(message, "✅ Готово!")
        print("[bebraBot] Очистка...")
        os.remove(input_path)
        os.remove(output_path)
        print("[bebraBot] Ожидание команд...")
    except Exception as e:
        print(f"[ОШИБКА] Произошла ошибка при отправке документа: {e}")


bot.infinity_polling()  # Запуск бота в режиме бесконечного ожидания новых сообщений
