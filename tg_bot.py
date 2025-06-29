import telebot
from telebot import types
import json
import os
from dotenv import load_dotenv
from telebot.types import BotCommand


load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
bot.set_my_commands([
    BotCommand("start", "Запустить бота"),
    BotCommand("help", "Помощь"),
    BotCommand("data", "Отображение бд"),
])
user_data = []
@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button1 = types.KeyboardButton('Расписание')
    button2 = types.KeyboardButton('Задания')
    button3 = types.KeyboardButton("Регистрация")
    keyboard.add(button1, button2, button3)
    bot.reply_to(message, 'Привет! Я бот.', reply_markup=keyboard)
@bot.message_handler(func=lambda message: message.text == "Регистрация")
def handle_reg(message):
    bot.send_message(message.chat.id, "Введите имя идиот:")
    bot.register_next_step_handler(message, save_name)
    keyboard = types.ReplyKeyboardMarkup(row_width=1)

def save_name(message):
    user_name = message.text

    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"users": []}

    # Ищем пользователя по ID (правильная проверка)
    user_exists = any(user["id"] == message.chat.id for user in data["users"])

    if user_exists:
        # Обновляем имя существующего пользователя
        for user in data["users"]:
            if user["id"] == message.chat.id:
                user["name"] = user_name
                break
    else:
        # Создаем нового пользователя
        new_user = {
            "id": message.chat.id,
            "name": user_name,
            "age": None
        }
        data["users"].append(new_user)

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    bot.send_message(message.chat.id, "Теперь введите возраст тварь:")
    bot.register_next_step_handler(message, save_age)


def save_age(message):
    try:
        user_age = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Введи возраст числом пидор!")
        return

    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        bot.send_message(message.chat.id, "Ошибка загрузки данных")
        return

    # Ищем пользователя по ID (правильный поиск)
    for user in data["users"]:
        if user["id"] == message.chat.id:
            user["age"] = user_age
            break

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    bot.send_message(message.chat.id, "Твой возраст сохранен! Пошёл Нахуй!")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "введи 1 из 2 комманд (/data или /start) Что сложного?" )

@bot.message_handler(commands=['data'])
def send_data(message):
    try:
        with open('data.json', 'r',encoding='utf-8') as file:
            data = json.load(file)

        if not data.get('users'):
            bot.send_message(message.chat.id, "Нет зарегистрированных пользователей")
            return

        users_list = []
        for user in data['users']:
            user_info = f"ID: {user.get('id', 'N/A')}\n" \
                        f"Имя: {user.get('name', 'N/A')}\n" \
                        f"Возраст: {user.get('age', 'N/A')}\n" \
                        "------------------------"
            users_list.append(user_info)

        response = "Зарегистрированные пользователи:\n\n" + "\n".join(users_list)
        bot.send_message(message.chat.id, response)

    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл данных не найден")

@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text == 'Расписание':
        bot.reply_to(message, 'Здесь будет расписание, а пока нам поухуй.')
    elif message.text == 'Задания':
        bot.reply_to(message, 'Здесь будут ваши задания, но я в рот ебал его придумывать')
    elif message.text == "Пидор":
        bot.reply_to(message, "От пидоора слышу! ")


bot.polling()