from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
"""Создание кнопки назад"""

async def back_kb_builder():
    return ReplyKeyboardMarkup().add(KeyboardButton('Назад')) # клавиатура с кнопкой Назад
