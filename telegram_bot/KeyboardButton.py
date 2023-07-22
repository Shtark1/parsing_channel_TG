from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


# ================= КНОПКИ АДМИНА =================
btn_add_admin = KeyboardButton("Добавить админа")
btn_del_admin = KeyboardButton("Удалить админа")
btn_all_admin = KeyboardButton("Все админы")

btn_add_channel = KeyboardButton("Добавить канал")
btn_del_channel = KeyboardButton("Удалить канал")
btn_all_channel = KeyboardButton("Все каналы")

btn_restart_parser = KeyboardButton("Перезапустить Парсер")


btn_edit_start = InlineKeyboardButton(text="Приветствие", callback_data="start")

btn_cancel = KeyboardButton("Отмена")


BUTTON_TYPES = {
    "BTN_HOME_ADMIN": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_add_admin, btn_del_admin).add(btn_all_admin).
    add(btn_add_channel, btn_del_channel).add(btn_all_channel).add(btn_restart_parser),

    "BTN_CANCEL": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel),
}
