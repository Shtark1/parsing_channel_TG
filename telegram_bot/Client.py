from aiogram.types import Message
from aiogram.dispatcher import Dispatcher

from content_text.messages import MESSAGES
from telegram_bot.KeyboardButton import BUTTON_TYPES
from cfg.config import USER_POST, ADMIN_ID
from create_bot import dp, bot


# ===================================================
# ================== СТАРТ КОМАНДА ==================
# ===================================================
async def start_command(message: Message):
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["start_admin"], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

    else:
        await bot.send_message(text=MESSAGES["not_command"], chat_id=message.from_user.id)


# ===================================================
# =============== НЕИЗВЕСТНАЯ КОМАНДА ===============
# ===================================================
async def unknown_command(message: Message):
    if message.from_user.id in USER_POST:
        try:
            topic_super_gr = message.text.split("\n")
            await bot.send_message(chat_id=topic_super_gr[-2], text="\n".join(topic_super_gr[0:-2]), reply_to_message_id=topic_super_gr[-1])
        except:
            ...
    else:
        await bot.send_message(text=MESSAGES["not_command"], chat_id=message.from_user.id)


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands="start")
    dp.register_message_handler(unknown_command, content_types=["text"])

