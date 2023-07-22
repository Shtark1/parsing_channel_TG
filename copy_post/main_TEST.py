from telethon import TelegramClient, events
import sqlite3
import asyncio


api_id = 22616016
api_hash = "387da1de125d82520899177387fad715"

connection = sqlite3.connect("copy_post/my_session_1.session")
cursor = connection.cursor()


client = TelegramClient("copy_post/my_session_1.session", api_id, api_hash, system_version="4.16.30-vxCUSTOM", device_model="PC 64bit")

target_channel = "TestBotKworkYouTube_BOT"





with client:
    client.run_until_disconnected()