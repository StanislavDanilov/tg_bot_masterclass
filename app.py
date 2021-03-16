import telebot
from telebot import types
from pymongo import MongoClient

bot = telebot.TeleBot('1677013439:AAGPm7M_Cnw8kWHEgD1vafilrJdzPS-meyA')

client = MongoClient('localhost', 27017)
db = client['Goroskop']
users = db['Clients']

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Как тебя зовут?")
    bot.register_next_step_handler(message, get_lastname)
def get_lastname(message):
    global nameReg
    global tg_id
    tg_id = message.from_user.id
    nameReg = message.text
    bot.send_message(message.from_user.id, "Какая у тебя фамилия?")
    bot.register_next_step_handler(message, get_email)
def get_email(message):
    global namelast
    namelast = message.text
    bot.send_message(message.from_user.id, "Какая у тебя почта?")
    bot.register_next_step_handler(message, get_happy)
def get_happy(message):
    global email
    email = "".join(message.text)
    bot.send_message(message.from_user.id, "Какого ты года рождения?")
    bot.register_next_step_handler(message, temp)
def temp(message):
    global happy
    happy = message.text
    bot.send_message(message.from_user.id, "Какой знак зодиака?")
    bot.register_next_step_handler(message, get_sign)
def get_sign(message):
    global sign
    global password
    password = [namelast+nameReg+happy, happy+namelast+nameReg]
    sign = message.text
    get_insert()
    bot.send_message(message.from_user.id, f"Индивидуальный гороскоп для пользователя {nameReg} {namelast}\nВаш знак зодиака - {sign} , поэтому вы - тонко чувствующая натура")

@bot.message_handler(commands=['password'])
def get_pass(message):
    bot.send_message(message.from_user.id, "Введите почту?")
    bot.register_next_step_handler(message, get_email_client)
def get_email_client(message):
    email_client = message.text
    find = users.find_one({"Email": email_client})
    if not find:
        bot.send_message(message.from_user.id, f"Пользователя еще нет!!!!")
    else:
        password = find["password"]
        i = 0
        bot.send_message(message.from_user.id, f"{email}<---Для пользователя с таким email, возможные пароли:\n")
        while i < len(password):
                print(password)
                bot.send_message(message.from_user.id, password[i])
                i+=1

def get_insert():
    db.Clients.insert_one({
    "Name": nameReg,
    "Email": email,
    "tg_id": tg_id,
    "sign": sign,
    "happy": happy,
    "password": password
                          })
bot.polling(none_stop=True, interval=0)
