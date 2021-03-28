from .._base_keyboard import BaseKeyboardExtension
from aiogram.types import InlineKeyboardButton

class Back(BaseKeyboardExtension):
    def __init__(self, text, callback_data):
        self.callback_data = callback_data
        self.text = text

    def _extender(self):
        self.base.kb.add(InlineKeyboardButton(self.text, callback_data=self.callback_data))
