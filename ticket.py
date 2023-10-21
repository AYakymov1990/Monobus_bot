import telebot
from telebot import types

# Ваш токен от @BotFather
token = '5694253036:AAE-3oUcLVas-o_1o-3-_QQgh4ZObsg0Hwo'

# Создание бота
bot = telebot.TeleBot(token)

# Словарь для хранения данных о пользователе
user_data = {}


# Обработка команды /start и отображение главного меню
@bot.message_handler(commands=['start'])
def start(message):
    send_main_menu(message.chat.id)


# Функция для отправки главного меню
def send_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    item_schedule = types.KeyboardButton("📆 Дізнатися розклад")
    item_booking = types.KeyboardButton("🚌 Бронювання квитків")
    item_have_booked = types.KeyboardButton("✅ Я уже забронював квиток")
    markup.add(item_schedule, item_booking, item_have_booked)

    bot.send_message(chat_id, "Ласкаво просимо до головного меню!", reply_markup=markup)


# Обработка команды "Дізнатись розклад" для начала запроса расписания
@bot.message_handler(func=lambda message: message.text == "📆 Дізнатися розклад")
def book_schedule(message):
    bot.send_message(message.chat.id, "Звідки ви відправляєтеся?")
    bot.register_next_step_handler(message, get_departure_schedule)


# Функция для получения места отправления
def get_departure_schedule(message):
    departure = message.text
    bot.send_message(message.chat.id, "Куди ви направляєтеся?")
    user_data[message.chat.id] = {"departure": departure}
    bot.register_next_step_handler(message, get_destination_schedule)


# Функция для получения места назначения
def get_destination_schedule(message):
    destination = message.text
    user_data[message.chat.id]["destination"] = destination
    bot.send_message(message.chat.id, "Введіть дату вашої поїздки (у форматі ДД.ММ.РРРР):")
    bot.register_next_step_handler(message, get_date_schedule)


# Функция для получения даты поездки
def get_date_schedule(message):
    date = message.text
    chat_id = message.chat.id
    user_data[chat_id]["date"] = date
    bot.send_message(chat_id, "Введіть ваш номер телефону:")
    bot.register_next_step_handler(message, get_phone_schedule)


# Функция для получения номера телефона
def get_phone_schedule(message):
    phone = message.text
    chat_id = message.chat.id
    user_info = user_data.get(chat_id, {})
    user_info["phone"] = phone
    send_schedule_request_to_admin(chat_id, user_info, message.from_user.id, message.from_user.username)
    bot.send_message(chat_id,
                     f"Ваш запит на отримання розкладу на {user_info['date']} прийнятий. Ми зв'яжемося з вами по номеру {user_info['phone']} для підтвердження.")
    reset_user_data(chat_id)
    send_main_menu(chat_id)  # Вернуть в главное меню


# Функция для отправки запроса расписания администратору
def send_schedule_request_to_admin(chat_id, user_info, user_id, user_username):
    admin_channel_id = '@monobusMeneger'  # Идентификатор канала администратора
    username = user_info.get("username", "Нет информации")
    phone = user_info.get("phone", "Нет информации")
    departure = user_info.get("departure", "Нет информации")
    destination = user_info.get("destination", "Нет информации")
    date = user_info.get("date", "Нет информации")

    admin_message = f"**Новий запит на розклад**\n\n" \
                    f"Користувач: @{user_username} (ID: {user_id})\n" \
                    f"Номер телефону: {phone}\n" \
                    f"Звідки: {departure}\n" \
                    f"Куди: {destination}\n" \
                    f"Дата: {date}"

    bot.send_message(admin_channel_id, admin_message, parse_mode='Markdown')


# Обработка команды "Бронювання квитків" для начала запроса бронирования
@bot.message_handler(func=lambda message: message.text == "🚌 Бронювання квитків")
def book_tickets(message):
    bot.send_message(message.chat.id, "Введіть місце відправлення:")
    bot.register_next_step_handler(message, get_departure_booking)


# Функция для получения места отправления (бронирование)
def get_departure_booking(message):
    departure = message.text
    bot.send_message(message.chat.id, "Введіть місце призначення:")
    user_data[message.chat.id] = {"departure": departure}
    bot.register_next_step_handler(message, get_destination_booking)


# Функция для получения места назначения (бронирование)
def get_destination_booking(message):
    destination = message.text
    user_data[message.chat.id]["destination"] = destination
    bot.send_message(message.chat.id, "Введіть дату вашої поїздки (у форматі ДД.ММ.РРРР):")
    bot.register_next_step_handler(message, get_date_booking)


# Функция для получения даты поездки (бронирование)
def get_date_booking(message):
    date = message.text
    chat_id = message.chat.id
    user_data[chat_id]["date"] = date
    bot.send_message(chat_id, "Введіть кількість місць, які ви хочете забронювати:")
    bot.register_next_step_handler(message, get_seat_count_booking)


# Функция для получения количества мест (бронирование)
def get_seat_count_booking(message):
    seat_count = message.text
    chat_id = message.chat.id
    user_data[chat_id]["seat_count"] = seat_count
    bot.send_message(chat_id, "Введіть ваше ім'я та фамілію:")
    bot.register_next_step_handler(message, get_name_booking)


# Функция для получения имени и фамилии (бронирование)
def get_name_booking(message):
    name = message.text
    chat_id = message.chat.id
    user_data[chat_id]["name"] = name
    bot.send_message(chat_id, "Введіть ваш номер телефону:")
    bot.register_next_step_handler(message, get_phone_booking)


# Функция для получения номера телефона (бронирование)
def get_phone_booking(message):
    phone = message.text
    chat_id = message.chat.id
    user_info = user_data.get(chat_id, {})
    user_info["phone"] = phone
    send_booking_request_to_admin(chat_id, user_info, message.from_user.id, message.from_user.username)
    bot.send_message(chat_id,
                     f"Ваше бронювання прийняте. Ми зв'яжемося з вами по номеру {user_info['phone']} для підтвердження.")
    reset_user_data(chat_id)
    send_main_menu(chat_id)  # Вернуть в главное меню


# Функция для отправки запроса на бронирование администратору
def send_booking_request_to_admin(chat_id, user_info, user_id, user_username):
    admin_channel_id = '@monobusMeneger'  # Идентификатор канала администратора
    username = user_info.get("username", "Нет информации")
    phone = user_info.get("phone", "Нет информации")
    departure = user_info.get("departure", "Нет информации")
    destination = user_info.get("destination", "Нет информации")
    date = user_info.get("date", "Нет информации")
    seat_count = user_info.get("seat_count", "Нет информации")
    name = user_info.get("name", "Нет информации")

    admin_message = f"**Новий запит на бронювання**\n\n" \
                    f"Користувач: @{user_username} (ID: {user_id})\n" \
                    f"Номер телефону: {phone}\n" \
                    f"Відправлення: {departure}\n" \
                    f"Призначення: {destination}\n" \
                    f"Дата: {date}\n" \
                    f"Кількість місць: {seat_count}\n" \
                    f"Ім'я та фамілія: {name}"

    bot.send_message(admin_channel_id, admin_message, parse_mode='Markdown')

# Функция для получения текстового сообщения (Я уже забронював квиток)
def get_question_have_booked(message):
    question = message.text
    chat_id = message.chat.id
    user_data[chat_id]["question"] = question
    send_request_have_booked_ticket_to_admin(chat_id, user_data[chat_id], message.from_user.id, message.from_user.username)
    bot.send_message(chat_id, "Ваш запит відправлений. Ми зв'яжемося з вами для відповіді на ваше питання.")
    reset_user_data(chat_id)
    send_main_menu(chat_id)  # Вернуть в главное меню

# Обработка команды "Я уже забронював квиток" для начала запроса о уже забронированных билетах
@bot.message_handler(func=lambda message: message.text == "✅ Я уже забронював квиток")
def have_booked_ticket(message):
    bot.send_message(message.chat.id, "Введіть ваше ім'я та фамілію:")
    bot.register_next_step_handler(message, get_name_have_booked)



# Функция для получения имени и фамилии (я уже забронировал билет)
def get_name_have_booked(message):
    name = message.text
    chat_id = message.chat.id
    user_data[chat_id] = {"name": name}
    bot.send_message(chat_id, "Введіть ваш номер телефону:")
    bot.register_next_step_handler(message, get_phone_have_booked)

# Функция для получения номера телефона (я уже забронировал билет)
def get_phone_have_booked(message):
    phone = message.text
    chat_id = message.chat.id
    user_info = user_data.get(chat_id, {})
    user_info["phone"] = phone
    bot.send_message(chat_id, "Введіть ваше питання:")
    bot.register_next_step_handler(message, get_question_have_booked)

# Функция для отправки запроса "Я уже забронював квиток" администратору
def send_request_have_booked_ticket_to_admin(chat_id, user_info, user_id, user_username):
    admin_channel_id = '@monobusMeneger'  # Идентификатор канала администратора
    username = user_info.get("username", "Нет информации")
    phone = user_info.get("phone", "Нет информации")
    name = user_info.get("name", "Нет информации")
    question = user_info.get("question","Нет информации")


    admin_message = f"**Новий запит 'Я уже забронював квиток'**\n\n" \
                    f"Користувач: @{user_username} (ID: {user_id})\n" \
                    f"Номер телефону: {phone}\n" \
                    f"Ім'я та фамілія: {name}\n" \
                    f"Запит: {question}"

    bot.send_message(admin_channel_id, admin_message, parse_mode='Markdown')


# Функция для сброса данных пользователя
def reset_user_data(chat_id):
    if chat_id in user_data:
        del user_data[chat_id]


if __name__ == "__main__":
    bot.polling(none_stop=True)
