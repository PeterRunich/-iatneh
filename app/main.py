from os import system
from sys import platform
if platform.lower() == 'win32':
    system('cls')
else:
    system('clear')

from .callback_handlers import *
from aiogram import executor
from .bot import dispatcher
from .handlers import *
"""Главный файл предназначен для запсука бота"""

# Запускаем event loop тольео если файл был запущен на прямую
if __name__ == '__main__':
    executor.start_polling(dispatcher)
