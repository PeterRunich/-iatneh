from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
"""Делает на клавиатурном месте две кнопки поиск и фильтры"""

async def start_kb_builder():
    kb = ReplyKeyboardMarkup() # базовый элемент клавиатуры

    [kb.add(KeyboardButton(text)) for text in ('Поиск', 'Фильтры')] # наполняем двумя кнопками поиск, фильтры

    return kb
