from ._base_keyboard_pagination import BaseKeyboardPagination, BaseKeyboardPaginationExtension
from aiogram.types import InlineKeyboardButton

async def selected_genres_kb(genres, genre_ids):
    callback_id = 'cq1'

    return BaseKeyboardPagination(0,
                                  callback_id,
                                  0,
                                  [GenreFilters(genres, genre_ids), GenreFiltersBack()]).kb

class GenreFilters(BaseKeyboardPaginationExtension):
    def __init__(self, all_genres, selected_genre_ids):
        self.selected_genre_ids = selected_genre_ids
        self.all_genres = all_genres

    def _extender(self):
        for genre in self.all_genres:
            genre_id = genre[0]
            genre_name = genre[1]
            #мб стоит вынести логичку отсюда
            if str(genre_id) in self.selected_genre_ids:
                genre_name += ' ✅'
                action = 'remove_from_filter'
            else:
                continue
            #мб стоит вынести логичку отсюда
            if len(genre_name) > 15:
                self.pgn.kb.row_width = 1
                self.pgn.kb.row(InlineKeyboardButton(genre_name, callback_data=f'{self.pgn.callback_id}:{action}:{genre_id}'))
            else:
                self.pgn.kb.insert(InlineKeyboardButton(genre_name, callback_data=f'{self.pgn.callback_id}:{action}:{genre_id}'))
                self.pgn.kb.row_width = 3

class GenreFiltersBack(BaseKeyboardPaginationExtension):
    def _extender(self):
        self.pgn.kb.row_width = 1
        self.pgn.kb.row(InlineKeyboardButton('Назад', callback_data=f'{self.pgn.callback_id}:back:'))
