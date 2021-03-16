from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class BaseKeyboardPagination:
    def __init__(self, last_page_num, callback_id, current_page_num=1, extensions=None):
        self.current_page_num = current_page_num
        self.last_page_num = last_page_num
        self.callback_id = callback_id
        self.extensions = extensions

        self.__create(extensions)

    def __create(self, extensions):
        self.kb = InlineKeyboardMarkup()

        for extension in extensions:
            self.kb.row_width = 1
            extension.extend_kb(self)

class BaseKeyboardPaginationExtension:
    def extend_kb(self, pagination_obj):
        self.pgn = pagination_obj
        self._extender()

class BasePaginationControls(BaseKeyboardPaginationExtension):
    def _extender(self):
        self.pgn.kb.row_width = 5
        self.pgn.kb.row(self.__first_page(), self.__previous_page(), self.__page_indicator(), self.__next_page(), self.__last_page())

    def __first_page(self):
        return InlineKeyboardButton('«', callback_data=f'{self.pgn.callback_id}:change_page_to:1')

    def __last_page(self):
        return InlineKeyboardButton('»', callback_data=f'{self.pgn.callback_id}:change_page_to:{self.pgn.last_page_num}')

    def __next_page(self):
        if self.pgn.current_page_num + 1 > self.pgn.last_page_num:
            next_page = self.pgn.last_page_num
        else:
            next_page = self.pgn.current_page_num + 1

        return InlineKeyboardButton('>', callback_data=f'{self.pgn.callback_id}:change_page_to:{next_page}')

    def __previous_page(self):
        if self.pgn.current_page_num - 1 < 1:
            previous_page = 1
        else:
            previous_page = self.pgn.current_page_num - 1

        return InlineKeyboardButton('<', callback_data=f'{self.pgn.callback_id}:change_page_to:{previous_page}')

    def __page_indicator(self):
        return InlineKeyboardButton(f'{self.pgn.current_page_num}/{self.pgn.last_page_num}', callback_data=f'{self.pgn.callback_id}:no_action:')
