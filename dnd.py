import telebot
import random
from random import randint
import os

API_TOKEN = '7549935732:AAHUpHaiM9qQauuOT4m1tXRQ6yNe_jTzKY4'

bot = telebot.TeleBot(API_TOKEN)

user_rolls = {}

def save_roll_history(user_id, roll):
    if user_id not in user_rolls:
        user_rolls[user_id] = []
    user_rolls[user_id].append(roll)
    with open(f'{user_id}_rolls.txt', 'w') as f:
        for roll in user_rolls[user_id]:
            f.write(str(roll) + '\n')

def load_roll_history(user_id):
    if os.path.exists(f'{user_id}_rolls.txt'):
        with open(f'{user_id}_rolls.txt', 'r') as f:
            return [int(line.strip()) for line in f]
    return []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id not in user_rolls:
        user_rolls[user_id] = []
    
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    btn1 = telebot.types.KeyboardButton('Я Мастер')
    btn2 = telebot.types.KeyboardButton('Я Игрок')
    btn3 = telebot.types.KeyboardButton('Совет дня')
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(chat_id, "Выберите вашу роль:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_role(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if message.text == 'Я Мастер':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        btn1 = telebot.types.KeyboardButton('Кинуть дайсы')
        btn2 = telebot.types.KeyboardButton('Назад')
        markup.add(btn1, btn2)
        bot.send_message(chat_id, "Вы выбрали роль Мастера", reply_markup=markup)

    elif message.text == 'Я Игрок':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        btn1 = telebot.types.KeyboardButton('Кинуть дайсы')
        btn2 = telebot.types.KeyboardButton('Назад')
        markup.add(btn1, btn2)
        bot.send_message(chat_id, "Вы выбрали роль Игрока", reply_markup=markup)

    elif message.text == 'Кинуть дайсы':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
        btn1 = telebot.types.KeyboardButton('К4')
        btn2 = telebot.types.KeyboardButton('К6')
        btn3 = telebot.types.KeyboardButton('К8')
        btn4 = telebot.types.KeyboardButton('К10')
        btn5 = telebot.types.KeyboardButton('К12')
        btn6 = telebot.types.KeyboardButton('К20')
        btn7 = telebot.types.KeyboardButton('К100')
        btn8 = telebot.types.KeyboardButton('Сохранить историю бросков')
        btn9 = telebot.types.KeyboardButton('Назад')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
        bot.send_message(chat_id, "Выберите кубик для броска:", reply_markup=markup)

    elif message.text == 'Сохранить историю бросков':
        rolls = load_roll_history(user_id)
        with open('История бросков', 'w') as f:
            for roll in rolls:
                f.write(str(roll) + '\n')
        bot.send_document(chat_id, document=open('История бросков', 'rb'))

    elif message.text == 'Назад':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        btn1 = telebot.types.KeyboardButton('Я Игрок')
        btn2 = telebot.types.KeyboardButton('Я Мастер')
        btn3 = telebot.types.KeyboardButton('Совет дня')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=markup)

    elif message.text == 'Совет дня':
        tips = [
            "Когда игрок делает спасбросок от смерти, попросите его поделиться каким-то воспоминанием из жизни его персонажа.",
            "Броски навыков становятся интереснее, если дать игрокам возможность выбирать между двумя вариантами действий, каждый из которых дает разный бонус к броску. У разных персонажей может быть разный подход к одной и той же проблеме.",
            "Навык Insight — это не “детектор лжи”, он лишь позволяет заметить признаки тех чувств, которые НПС испытывает по отношению к предмету беседы. Например – “Когда вы упоминаете капитана гвардии, вы замечаете, что сержант кусает губы и сжимает костяшки пальцев”.",
            "Ноль хитов не обязательно означает смерть; это может быть просто крупный провал для персонажа. Зачастую интереснее спросить игрока, чего он лишился, чем просить создать нового персонажа.",
            "Не каждая встреча с монстрами должна заканчиваться боем. Делайте какие-нибудь броски реакции монстров на персонажей игроков.",
            "Живые существа редко дерутся до смерти. Делайте проверки их морали или боевого духа, когда битва начинает идти по плохому для них сценарию.",
            "Позволяйте любому персонажу попытаться произнести заклинание из свитка, но пусть шансы на успех зависят от степени его знакомства с магией. Это может стать решающим фактором в какой-то момент!",
            "Не забывайте о бонусах и штрафах к броскам.",
            "Когда игрок снижает хиты монстра до нуля, попросите его описать, как он добивает противника.",
            "В самом начале кампании подчеркните, что бегство — это всегда доступный вариант действий.",
            "Это нормально напоминать игрокам о том, что знают их персонажи. Возможно, внутри игры прошел всего час времени, но в реальном мире последняя сессия была месяц назад.",
            "воды"
        ]
        tip = random.choice(tips)
        bot.send_message(message.chat.id, f"Совет дня: {tip}")
    else:
        try:
            dice_sides = int(message.text[1:])
            roll = randint(1, dice_sides)
            save_roll_history(user_id, roll)
            bot.send_message(chat_id, f"Вы бросили {roll}")
        except ValueError:
            bot.send_message(chat_id, "Пожалуйста, выберите доступную кнопку.")

bot.polling()
