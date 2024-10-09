import telebot
import sqlite3

# Токен бота
TOKEN = 'твой_токен_бота'

bot = telebot.TeleBot(TOKEN)

# Подключение к базе данных
conn = sqlite3.connect('bot_users.db', check_same_thread=False)
cursor = conn.cursor()

# Функция для регистрации пользователя
def register_user(chat_id):
    cursor.execute('INSERT OR IGNORE INTO users (chat_id) VALUES (?)', (chat_id,))
    conn.commit()

# Функция для получения всех пользователей
def get_all_users():
    cursor.execute('SELECT chat_id FROM users')
    return cursor.fetchall()

# Команда /start для регистрации пользователя
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    register_user(chat_id)
    bot.send_message(chat_id, "Вы успешно зарегистрированы для получения уведомлений!")

# Команда для администратора, чтобы отправить сообщение всем пользователям
@bot.message_handler(commands=['admin'])
def admin_send_message(message):
    if message.chat.id == твой_chat_id_администратора:  # проверяем, что это админ
        bot.send_message(message.chat.id, "Введите сообщение для рассылки:")
        bot.register_next_step_handler(message, broadcast_message)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для этой команды.")

# Функция рассылки сообщений всем пользователям
def broadcast_message(message):
    text = message.text
    users = get_all_users()
    for user in users:
        try:
            bot.send_message(user[0], text)  # user[0] — это chat_id
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user[0]}: {e}")

bot.polling()
