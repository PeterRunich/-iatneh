from .._base_keyboard import BaseKeyboardExtension
from aiogram.types import InlineKeyboardButton

class PaginationControls(BaseKeyboardExtension):
    def __init__(self, current_page_num, last_page_num):
        self.current_page_num = current_page_num
        self.last_page_num = last_page_num


    def _extender(self):
        self.base.kb.row_width = 5
        self.base.kb.row(self.__first_page(), self.__previous_page(), self.__page_indicator(), self.__next_page(), self.__last_page())

    def __first_page(self):
        return InlineKeyboardButton('«', callback_data=f'{self.base.callback_id}:change_page_to:1')

    def __last_page(self):
        return InlineKeyboardButton('»', callback_data=f'{self.base.callback_id}:change_page_to:{self.last_page_num}')

    def __next_page(self):
        if self.current_page_num + 1 > self.last_page_num:
            next_page = self.last_page_num
        else:
            next_page = self.current_page_num + 1

        return InlineKeyboardButton('>', callback_data=f'{self.base.callback_id}:change_page_to:{next_page}')

    def __previous_page(self):
        if self.current_page_num - 1 < 1:
            previous_page = 1
        else:
            previous_page = self.current_page_num - 1

        return InlineKeyboardButton('<', callback_data=f'{self.base.callback_id}:change_page_to:{previous_page}')

    def __page_indicator(self):
        return InlineKeyboardButton(f'{self.current_page_num}/{self.last_page_num}', callback_data=f'{self.base.callback_id}:no_action:')
