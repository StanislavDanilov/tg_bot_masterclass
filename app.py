import telebot
from telebot import types
from pymongo import MongoClient

bot = telebot.TeleBot('1677013439:AAGPm7M_Cnw8kWHEgD1vafilrJdzPS-meyA');
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Как тебя зовут?")
    bot.register_next_step_handler(message, get_lastname)
def get_lastname(message):
    global nameReg
    nameReg = message.text
    bot.send_message(message.from_user.id, "Какая у тебя фамилия?")
    bot.register_next_step_handler(message, get_email)
def get_email(message):
    global namelast
    namelast = message.text
    bot.send_message(message.from_user.id, "Какая у тебя почта?")
    bot.register_next_step_handler(message, happy)
def happy(message):
    global email
    
    email = str(message.text)
    bot.send_message(message.from_user.id, "Какого ты года рождения?")
    bot.register_next_step_handler(message, temp)
def temp(message):
    global happy
    happy = message.text
    bot.register_next_step_handler(message, menu)

@bot.message_handler(content_types=['text'])
def menu(message):
    if message.text == "Возможный пароль":
        bot.send_message(message.from_user.id, f"{email}<---Для пользователя с таким email, возможные пароли:\n")
        password = [namelast+nameReg+happy, happy+namelast+nameReg]
        i = 0
        while i < len(password):
            print(password)
            bot.send_message(message.from_user.id, password[i])
            i+=1
bot.polling(none_stop=True, interval=0)
