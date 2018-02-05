# Однострочный комментарий
"""
Многострочный коментарий
"""


import telebot
from telebot.types import ReplyKeyboardMarkup

import constant
import sqlite3

from telebot import types
bot = telebot.TeleBot(constant.token)
conn = sqlite3.connect("mydb.db") #Подключение бызы если ее нет то создаст
#cursor = conn.cursor()
#cursor.execute("CREATE TABLE users(Idus INT,Name TEXT)")   СОздание таблица

print("Бот Запущен")

@bot.message_handler(commands=['it'])
def handle_it (message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Шерлок ', ' Ватсон']])
    bot.send_message(message.chat.id, 'Кого выбираешь?', reply_markup =keyboard)
    if message.text == 'Шерлок':
        bot.send_message(message.chat.id, 'looopl')
        #keyboard = types.ReplyKeyboardMarkup
        bot.send_message(message.chat.id, 'looopl')
        bot.register_next_step_handler(message, handle_it )
    elif message.text == 'Ватсон':
        #keyboard = types.ReplyKeyboardMarkup
        bot.send_message(message.chat.id, 'loool')
        bot.register_next_step_handler(message, handle_it)

@bot.message_handler(content_types= [''])
def handle_text(message):
        print("Принято сообщение")

@bot.message_handler(commands=['db'])
def handle_db(message):
        conn = sqlite3.connect("mydb.db")
        conn.commit()
        print (type(message.chat.id))
        cursor = conn.cursor()

        cursor.execute("SELECT Idus FROM users WHERE Idus=:id",{"id": message.chat.id}) # ПРавильная запись запроса

        ids = cursor.fetchall()
        ids = str(ids[0])
        ids = ids[1:-2:]
        ids = int(ids)  # Из списка в целочислаенный List to Intager

        print(type(ids))
        if message.chat.id == ids:
            message.text = ("")
            bot.send_message(message.chat.id, ids)
            bot.send_message(message.chat.id, "Я тебя знаю") # Запись есть в базе
        else:
            bot.send_message(message.chat.id, "Представься, Я тебя не знаю")
            cursor.execute("INSERT INTO users VALUES(?,?)",(message.chat.id,message.text))
            conn.commit()
            cursor.execute("SELECT * FROM users")
            conn.commit()
            print (cursor.fetchall())
            conn.close()
            bot.send_message(message.chat.id, "CЫШ, я тебя запомнил")
            print(ids) # Записи нет в базе записывает заддыне в базу
        print("Принято команда \db")



bot.polling(none_stop=True, interval=0)