from ._base_keyboard_pagination import BaseKeyboardPagination, BaseKeyboardPaginationExtension, BasePaginationControls
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import math
"""Создаёт и возвращает inline панель с кнопками с названием аниме и ссылкой на ресурс"""

async def anime_show_kb_builder(animes, last_page_number, current_page_number=1, limit=10):
    callback_id = 'cq2'

    return BaseKeyboardPagination(last_page_number,
                                  callback_id,
                                  current_page_number,
                                  [Animes(animes), BasePaginationControls()]).kb

class Animes(BaseKeyboardPaginationExtension):
    def __init__(self, animes):
        self.animes = animes

    def _extender(self):
        for anime in self.animes:
            anime_name = anime[1]
            anime_source_url = anime[2]

            self.pgn.kb.row_width = 3
            self.pgn.kb.insert(InlineKeyboardButton(anime_name, url=anime_source_url))
