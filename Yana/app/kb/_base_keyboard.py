from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class BaseKeyboard:
    def __init__(self, callback_id, extensions=None):
        self.callback_id = callback_id
        self.extensions = extensions

        self.__create(extensions)

    def __create(self, extensions):
        self.kb = InlineKeyboardMarkup()

        for extension in extensions:
            self.kb.row_width = 1
            extension.extend_kb(self)

class BaseKeyboardExtension:
    def extend_kb(self, base):
        self.base = base
        self._extender()
