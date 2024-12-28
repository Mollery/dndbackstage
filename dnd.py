import telebot
import random
from random import randint
import os

API_TOKEN = '7549935732:AAHUpHaiM9qQauuOT4m1tXRQ6yNe_jTzKY4'

bot = telebot.TeleBot(API_TOKEN)

user_rolls = {}

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.roll_history = []

    def save_roll_history(self):
        with open(f'{self.user_id}_rolls.txt', 'w') as f:
            for roll in self.roll_history:
                f.write(str(roll) + '\n')

    def load_roll_history(self):
        if os.path.exists(f'{self.user_id}_rolls.txt'):
            with open(f'{self.user_id}_rolls.txt', 'r') as f:
                return [int(line.strip()) for line in f]
        return []

    def add_roll(self, roll):
        self.roll_history.append(roll)
        self.save_roll_history()

class Master(User):
    def __init__(self, user_id):
        super().__init__(user_id)
        self.role = 'Мастер'

    def handle_commands(self, message):
        # Дополнительные методы и команды для Мастера
        pass

class Player(User):
    def __init__(self, user_id):
        super().__init__(user_id)
        self.role = 'Игрок'

    def handle_commands(self, message):
        # Дополнительные методы и команды для Игрока
        pass

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if user_id not in user_rolls:
        user_rolls[user_id] = User(user_id)
    
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
    
    if not hasattr(user_rolls[user_id], 'role'):
        if message.text == 'Я Мастер':
            user_rolls[user_id] = Master(user_id)
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
            btn1 = telebot.types.KeyboardButton('Кинуть дайсы')
            btn2 = telebot.types.KeyboardButton('Назад')
            markup.add(btn1, btn2)
            bot.send_message(chat_id, "Вы выбрали роль Мастера", reply_markup=markup)
        elif message.text == 'Я Игрок':
            user_rolls[user_id] = Player(user_id)
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
            btn1 = telebot.types.KeyboardButton('Кинуть дайсы')
            btn2 = telebot.types.KeyboardButton('Назад')
            markup.add(btn1, btn2)
            bot.send_message(chat_id, "Вы выбрали роль Игрока", reply_markup=markup)
        elif message.text == 'Совет дня':
            tips = [
                "Когда игрок делает спасбросок от смерти, попросите его поделиться каким-то воспоминанием из жизни его персонажа.",
                # ... (остальные советы)
            ]
            tip = random.choice(tips)
            bot.send_message(chat_id, f"Совет дня: {tip}")
        else:
            bot.send_message(chat_id, "Пожалуйста, выберите доступную кнопку.")
    else:
        user = user_rolls[user_id]
        if message.text == 'Кинуть дайсы':
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
            rolls = user.load_roll_history()
            with open('История бросков', 'w') as f:
                for roll in rolls:
                    f.write(str(roll) + '\n')
            bot.send_document(chat_id, document=open('История бросков', 'rb'))
        elif message.text == 'Назад':
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
            btn1 = telebot.types.KeyboardButton('Я Игрок') if isinstance(user, Player) else None
            btn2 = telebot.types.KeyboardButton('Я Мастер') if isinstance(user, Master) else None
            btn3 = telebot.types.KeyboardButton('Совет дня')
            markup.add(*[btn for btn in [btn1, btn2] if btn is not None], btn3)
            bot.send_message(chat_id, "Вы вернулись в главное меню", reply_markup=markup)
        elif message.text == 'Совет дня':
            tips = [
                # ... (оставшиеся советы)
            ]
            tip = random.choice(tips)
            bot.send_message(chat_id, f"Совет дня: {tip}")
        else:
            try:
                dice_sides = int(message.text[1:])
                roll = randint(1, dice_sides)
                user.add_roll(roll)
                bot.send_message(chat_id, f"Вы бросили {roll}")
            except ValueError:
                bot.send_message(chat_id, "Пожалуйста, выберите доступную кнопку.")

bot.polling()