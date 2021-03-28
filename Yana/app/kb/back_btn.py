from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def back_btn_builder(callback_data, text='Назад в главное меню'):
    kb = InlineKeyboardMarkup()

    kb.add(InlineKeyboardButton(text, callback_data=callback_data))

    return kb
