from telegram_bot.utils import StatesUsers

# СООБЩЕНИЯ ОТ БОТА
start_message = """Привет 👋 
На связи бот БайкалАренды, выбери подразделение:"""
no_start_message = """Привет 👋 
К сожалению бот тебе не доступен"""
start_admin_message = "Приветствую админ 👋"
not_command_message = "Такой команды нет\nПиши /start"

add_admin_message = """ID состоит только из чисел 
 (его можно получить тут @username_to_id_bot)
Вводи ID пользователя:"""
not_admin_id_message = """Это не число, ID состоит только из чисел 
 (его можно получить тут @username_to_id_bot)
Вводи ID пользователя:"""

add_channel_message = "Введи id канала из которого парсить посты:"
id_channel_message = """Введи ID Супер группы 
(его можно получить тут @username_to_id_bot) 
и id Темы 

Пример:
-1001902790832
22"""

not_channel_message = "У вас нет добавленных каналов"
del_channel_message = "Скопируй строку для канала который надо удалить:"

MESSAGES = {
    "start": start_message,
    "no_start": no_start_message,
    "start_admin": start_admin_message,
    "not_command": not_command_message,
    "add_admin": add_admin_message,
    "not_admin_id": not_admin_id_message,
    "add_channel": add_channel_message,
    "id_channel": id_channel_message,
    "not_channel": not_channel_message,
    "del_channel": del_channel_message,
}
