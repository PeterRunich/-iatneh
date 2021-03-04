from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
"""Первоначальная настройка бота"""

# Объявляем бота, 1 аргумент - токен бота, его можно получить в @BotFather
bot = Bot('TOKEN')
# Выбираем хранилище для хранения состояний FSM https://mastergroosha.github.io/telegram-tutorial-2/fsm/
storage = MemoryStorage()
# Объявляем обработчик комманд, 1 аргумент экземпляр бота, 2 какое хранилише для FSM мы используем
dispatcher = Dispatcher(bot, storage=MemoryStorage())
