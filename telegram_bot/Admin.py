import re
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext, Dispatcher

from telegram_bot.utils import StatesAdmin, StatesAddUser
from telegram_bot.KeyboardButton import BUTTON_TYPES
from content_text.messages import MESSAGES
from cfg.config import ADMIN_ID, ADD_CHANNEL_ID
from create_bot import dp, bot


# ===================================================
# ===================== АДМИНКА =====================
# ===================================================
# ================= ДОБАВИТЬ АДМИНА =================
async def add_admin(message: Message):
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["add_admin"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAdmin.all()[1])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# =============== ВВОД ID АДМИНА ===============
async def id_admin(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text.isnumeric():
        new_users_id = int(message.text)
        ADMIN_ID.append(new_users_id)
        await message.answer("Добавил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await message.answer(MESSAGES["not_admin_id"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[1])


# ===================================================
# ================= УДАЛИТЬ АДМИНА ==================
# ===================================================
async def del_admin(message: Message):
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["add_admin"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAdmin.all()[2])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# ========== ВВОД ID АДМИНА ДЛЯ УДАЛЕНИЯ ==========
async def del_id_admin(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text.isnumeric():
        new_users_id = int(message.text)
        try:
            ADMIN_ID.remove(new_users_id)
            await message.answer("Удалил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        except:
            await message.answer("Такого пользователя нет!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

        await state.finish()
    else:
        await message.answer(MESSAGES["not_admin_id"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[2])


# ===================================================
# =================== ВСЕ АДМИНЫ ====================
# ===================================================
async def all_admin(message: Message):
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(chat_id=message.from_user.id, text="👉🏿 " + "\n👉🏿 ".join(list(map(str, ADMIN_ID))), reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# ===================================================
# ================= ДОБАВИТЬ КАНАЛ ==================
# ===================================================
async def add_channel(message: Message):
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["add_channel"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAdmin.all()[0])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# ========== ВВОД ID ЧАТА КУДА ОТПРАВЛЯТЬ ==========
async def username_channel(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await state.update_data(username_channel=message.text)
        await message.answer(MESSAGES["id_channel"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[3])


# ========== ЗАПИСЬ ДАННЫХ ==========
async def data_recording(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        try:
            id_s_id_t = message.text.split("\n")
            us_ch = await state.get_data()
            text_code = f"""
@client.on(events.NewMessage(chats={us_ch["username_channel"]}))
async def handler(event):
    await client.send_message(target_channel, f'''{{event.message.message}}\\n{id_s_id_t[0]}\\n{id_s_id_t[1]}''')
    await asyncio.sleep(2)

"""
            with open("copy_post/main_TEST.py", "r+") as f:
                lines = f.readlines()
                lines.insert(-3, text_code)
                f.seek(0)
                f.writelines(lines)

            ADD_CHANNEL_ID[f"{us_ch['username_channel']} | {message.text}"] = text_code

            await message.answer("Добавил!\nНе забудь перезапустить парсер", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        except:
            await message.answer("Не верные данные\nПопробуй заново", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

        await state.finish()


# ===================================================
# ================= УДАЛИТЬ КАНАЛ ==================
# ===================================================
async def del_channel(message: Message):
    if message.from_user.id in ADMIN_ID:
        all_ch = list(ADD_CHANNEL_ID.keys())
        if all_ch:
            text = "Все добавленные каналы: \n"
            for idx, ch in enumerate(all_ch):
                text += f"\n{idx + 1}. <code>{ch}</code>"
            await bot.send_message(chat_id=message.from_user.id, text=text, parse_mode="HTML")
            await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["del_channel"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(StatesAdmin.all()[4])
        else:
            await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_channel"], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# =============== ВВОД КАНАЛА ===============
async def data_channel(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        try:
            key_kod = message.text.split("\n")
            key_kod = "\n".join(key_kod)

            file_path = "copy_post/main_TEST.py"

            with open(file_path, "r") as file:
                content = file.read()

            pattern = re.escape(ADD_CHANNEL_ID[key_kod])
            updated_content = re.sub(pattern, '', content)

            with open(file_path, "w") as file:
                file.write(updated_content)

            ADD_CHANNEL_ID.pop(key_kod)

            await message.answer("Удалил!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        except Exception as ex:
            await message.answer("Такого канала нет!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

        await state.finish()


# ===================================================
# =================== ВСЕ КАНАЛЫ ====================
# ===================================================
async def all_channels(message: Message):
    if message.from_user.id in ADMIN_ID:
        all_ch = list(ADD_CHANNEL_ID.keys())
        text = "Все добавленные каналы: \n"
        for idx, ch in enumerate(all_ch):
            text += f"\n{idx + 1}. @{ch}"
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# ===================================================
# =================== ВСЕ КАНАЛЫ ====================
# ===================================================
async def restart_parser(message: Message):
    if message.from_user.id in ADMIN_ID:
        # try:
        import subprocess
        import psutil

        # import os
        # import signal
        # os.killpg(0, signal.SIGTERM)

        current_process = psutil.Process()

        python_processes = [p.info for p in psutil.process_iter(attrs=['pid', 'name']) if p.info['name'] == 'python.exe']

        # Завершаем всех процессов Python, кроме текущего
        for process in python_processes:
            if process['pid'] != current_process.pid:
                subprocess.run(f"taskkill /F /PID {process['pid']}", shell=True)

        # ЗАПУСК
        subprocess.Popen(["python", "copy_post/main_TEST.py"])

        await bot.send_message(chat_id=message.from_user.id, text="ПЕРЕЗАПУСТИЛ!")

    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# ===================================================
# ================= УЗНАТЬ  ID КАНАЛ ================
# ===================================================
async def what_id(message: Message):
    if message.from_user.id in ADMIN_ID:
        await bot.send_message(chat_id=message.from_user.id, text=message.message_id)

    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


def register_handler_admin(dp: Dispatcher):
    # ДОБАВЛЕНИЕ АДМИНА
    dp.register_message_handler(add_admin, lambda message: message.text.lower() == 'добавить админа')
    dp.register_message_handler(id_admin, state=StatesAdmin.STATES_1)

    # УДАЛЕНИЕ АДМИНА
    dp.register_message_handler(del_admin, lambda message: message.text.lower() == 'удалить админа')
    dp.register_message_handler(del_id_admin, state=StatesAdmin.STATES_2)

    # ВСЕ АДМИНЫ
    dp.register_message_handler(all_admin, lambda message: message.text.lower() == 'все админы')

    # ДОБАВИТЬ КАНАЛ
    dp.register_message_handler(add_channel, lambda message: message.text.lower() == 'добавить канал')
    dp.register_message_handler(username_channel, state=StatesAdmin.STATES_0)
    dp.register_message_handler(data_recording, state=StatesAdmin.STATES_3)

    # УДАЛИТЬ КАНАЛ
    dp.register_message_handler(del_channel, lambda message: message.text.lower() == 'удалить канал')
    dp.register_message_handler(data_channel, state=StatesAdmin.STATES_4)

    # ВСЕ КАНАЛЫ
    dp.register_message_handler(all_channels, lambda message: message.text.lower() == 'все каналы')

    # ПЕРЕЗАПУСТИТЬ ПАРСЕР
    dp.register_message_handler(restart_parser, lambda message: message.text.lower() == 'перезапустить парсер')

    # УЗНАТЬ ID ТЕМЫ
    dp.register_message_handler(what_id, commands=['id'])
