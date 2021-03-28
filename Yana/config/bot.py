from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from os import environ

if 'TG_BOT_TOKEN' not in environ: exit('Error: Поставь TG_BOT_TOKEN как переменную среды')

storage = MemoryStorage()

bot = Bot(environ['TG_BOT_TOKEN'])

dispatcher = Dispatcher(bot, storage=MemoryStorage())
