import telebot
from telebot import types
from config import *
from database import *

bot=telebot.TeleBot(TOKEN)


def start_key():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Посмотреть вакансии")
    btn2 = types.KeyboardButton("Помощь")
    return markup.add(btn1, btn2)


@bot.message_handler(commands=['start'])
def start(message):
    con = sqlite3.connect("tg.db")
    cur = con.cursor()    
    user_id = message.from_user.id
    db_tgid(user_id, cur, con)
    markup = start_key()
    bot.send_message(message.chat.id, start_msg, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    con = sqlite3.connect("tg.db")
    cur = con.cursor()    
    user_id = message.from_user.id    
    if message.text == 'Посмотреть вакансии' or message.text == '/vacancy':
        records = db_takevacancy(cur, con)
        for i in range (0, len(records)):
            msg = vacancy_msg(records[i][0], records[i][1], records[i][2], records[i][3], records[i][4])
            bot.send_message(user_id, msg)
    elif message.text == 'Помощь' or message.text == '/help':
        bot.send_message(user_id, help)
        


bot.infinity_polling(none_stop=True,interval=0)