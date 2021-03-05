from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
import os
"""Первоначальная настройка бота"""

exit('Error: Поставь TG_BOT_TOKEN как переменную среды') if 'TG_BOT_TOKEN' not in os.environ else True # проверяем есть ли переменнаю среды

# Объявляем бота, 1 аргумент - токен бота, его можно получить в @BotFather
bot = Bot(os.environ['TG_BOT_TOKEN'])
# Выбираем хранилище для хранения состояний FSM https://mastergroosha.github.io/telegram-tutorial-2/fsm/
storage = MemoryStorage()
# Объявляем обработчик комманд, 1 аргумент экземпляр бота, 2 какое хранилише для FSM мы используем
dispatcher = Dispatcher(bot, storage=MemoryStorage())
