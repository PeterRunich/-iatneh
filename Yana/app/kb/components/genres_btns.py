from .._base_keyboard import BaseKeyboardExtension
from aiogram.types import InlineKeyboardButton

class GenreBtns(BaseKeyboardExtension):
    def __init__(self, all_genres, selected_genre_ids):
        self.selected_genre_ids = selected_genre_ids
        self.all_genres = all_genres

    def _extender(self):
        for genre in self.all_genres:
            genre_id = genre[0]
            genre_name = genre[1]
            #мб стоит вынести логичку отсюда
            if str(genre_id) in self.selected_genre_ids:
                genre_name += ' ❌'
                action = 'remove_from_filter'
            else:
                action = 'add_to_filter'
            #мб стоит вынести логичку отсюда
            if len(genre_name) > 15:
                self.base.kb.row_width = 1
                self.base.kb.row(InlineKeyboardButton(genre_name, callback_data=f'{self.base.callback_id}:{action}:{genre_id}'))
            else:
                self.base.kb.insert(InlineKeyboardButton(genre_name, callback_data=f'{self.base.callback_id}:{action}:{genre_id}'))
                self.base.kb.row_width = 3
