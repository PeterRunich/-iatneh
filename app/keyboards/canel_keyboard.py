from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
"""Создание кнопки cancel"""

async def canel_kb_builder():
    return ReplyKeyboardMarkup().add(KeyboardButton('/canel')) # клавиатура с кнопкой /canel
