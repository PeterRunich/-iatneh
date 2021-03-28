from ._base_keyboard import BaseKeyboard, BaseKeyboardExtension
from .components.pagination_controls import PaginationControls
from aiogram.types import InlineKeyboardButton
from .components.genres_btns import GenreBtns
from .components.back_btn import Back
from ...db.db import Sqlite
import math

async def genre_filter_builder(current_page_number, last_page_num=math.ceil(Sqlite().count_genres() / 30), limit=30, genre_ids=[]):
    offset = (current_page_number - 1) * limit
    data = Sqlite().get_genres(limit, offset)
    callback_id = 'genre_filters'
    return BaseKeyboard(callback_id,
                        [GenreBtns(data, genre_ids), PaginationControls(current_page_number, last_page_num), GenresFilterControls(), Back('Назад в главное меню', 'main:to_main_menu:')]).kb

class GenresFilterControls(BaseKeyboardExtension):
    def _extender(self):
        self.base.kb.add(InlineKeyboardButton('Перейти на страницу по номеру', callback_data=f"{self.base.callback_id}:ask_page_to_go:"),
                        InlineKeyboardButton('Поиск жанра по названию', callback_data=f"{self.base.callback_id}:find_genre_by_name:"),
                        InlineKeyboardButton('Показать выбраные жанры', callback_data=f"{self.base.callback_id}:show_selected_genres:"),
                        InlineKeyboardButton('Поиск 🔎', callback_data=f"{self.base.callback_id}:search:"))
