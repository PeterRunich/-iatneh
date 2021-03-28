from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_builder():
    kb = InlineKeyboardMarkup()
    kb.row_width = 1
    btns = [
        InlineKeyboardButton('Поиск по названию', callback_data='main:to_search_by_name:'),
        InlineKeyboardButton('Поиск по жанрам', callback_data='main:to_filters:')
    ]

    kb.add(*btns)

    return kb
