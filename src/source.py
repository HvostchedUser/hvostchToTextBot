import os
import telebot

API_TOKEN="788745548:AAHoAmBoSxg0oyMyED-YOg9Hi07ra67cw9A"
bot=telebot.TeleBot(API_TOKEN,skip_pending=True)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id,text="Привет. Все сообщения здесь будут записаны.")
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(chat_id=message.chat.id,text="Я записываю все, о чем вы тут пишете.")

@bot.message_handler(content_types=['voice'])
def message(message):
    voice_info=bot.get_file(message.voice.file_id)
    voice_bytes=bot.download_file(voice_info.file_path)
    with open(voice_info.file_path,'wb') as file:
        file.write(voice_bytes)

@bot.message_handler(content_types=['document'])
def message(message):
    voice_info=bot.get_file(message.document.file_id)
    voice_bytes=bot.download_file(voice_info.file_path)
    with open(message.document.file_name,'wb') as file:
        file.write(voice_bytes)
@bot.message_handler(content_types=['photo'])
def message(message):
    phsize=message.photo
    for ph in phsize:
        voice_info=bot.get_file(ph.file_id)
        voice_bytes=bot.download_file(voice_info.file_path)
        with open(voice_info.file_path,'wb') as file:
            file.write(voice_bytes)




bot.polling()
