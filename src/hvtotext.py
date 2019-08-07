import os
import telebot
from pydub import AudioSegment
import io
import speech_recognition as sr


from flask import Flask, request



recognizer=sr.Recognizer()

API_TOKEN=os.getenv("TG_API_TOKEN")
bot=telebot.TeleBot(API_TOKEN,skip_pending=True)

server=Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id,text="Привет. Все сообщения здесь будут записаны.")
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(chat_id=message.chat.id,text="Я записываю все, о чем вы тут пишете.")

@bot.message_handler(content_types=['voice'])
def message(message):
    mesin=bot.reply_to(message,"Слушаю...")
    try:
        voice_info=bot.get_file(message.voice.file_id)
        voice_bytes=bot.download_file(voice_info.file_path)
        with open(voice_info.file_path,'wb') as file:
            wav = AudioSegment.from_ogg(io.BytesIO(voice_bytes))
            wav.export("voicewav.wav",format='wav')
            with sr.AudioFile('voicewav.wav') as source:
                audio=recognizer.record(source)
                text=recognizer.recognize_google(audio,language='ru-RU')
                bot.edit_message_text(text = text,chat_id=mesin.chat.id,message_id=mesin.message_id)
    except:
        bot.edit_message_text(text = "По-моему, здесь ничего не сказано.",chat_id=mesin.chat.id,message_id=mesin.message_id)

@server.route('/'+API_TOKEN,methods=['POST'])
def get_message():
    json_update=request.stream.read().decode('utf-8')
    update=telebot.types.Update.de_json(json_update)

    bot.process_new_updates([update])

    return '', 200


if __name__=='__main__':
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv('WEBHOOK_URL')+API_TOKEN)
    server.run(host="0.0.0.0",
               port=int(os.getenv('PORT',8443)))
