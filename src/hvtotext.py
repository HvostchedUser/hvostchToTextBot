import os
import telebot
from pydub import AudioSegment
import io
import speech_recognition as sr
recognizer=sr.Recognizer()

API_TOKEN="927043149:AAGwAaG6TBJnht6SxVWZJEvC0UvzsrZf5Ew"
bot=telebot.TeleBot(API_TOKEN,skip_pending=True)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id,text="Привет. Все сообщения здесь будут записаны.")
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(chat_id=message.chat.id,text="Я записываю все, о чем вы тут пишете.")

@bot.message_handler(content_types=['voice'])
def message(message):
    mesin=bot.reply_to(message,"Слушаю...")
    voice_info=bot.get_file(message.voice.file_id)
    voice_bytes=bot.download_file(voice_info.file_path)
    with open(voice_info.file_path,'wb') as file:
        wav = AudioSegment.from_ogg(io.BytesIO(voice_bytes))
        wav.export("voicewav.wav",format='wav')
        with sr.AudioFile('voicewav.wav') as source:
            audio=recognizer.record(source)
            text=recognizer.recognize_google(audio,language='ru-RU')
            bot.edit_message_text(text = text,chat_id=mesin.chat.id,message_id=mesin.message_id)

bot.polling()
