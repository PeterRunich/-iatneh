from ._base_keyboard import BaseKeyboard, BaseKeyboardExtension
from .components.pagination_controls import PaginationControls
from aiogram.types import InlineKeyboardButton
from .components.back_btn import Back

def show_anime_search_results_build(animes, last_page_number, current_page_number=1, limit=10):
    callback_id = 'anime_show'
    return BaseKeyboard(callback_id,
                        [Animes(animes), PaginationControls(current_page_number, last_page_number), Back('Назад в главное меню', 'anime_show:to_main_menu:')]).kb

class Animes(BaseKeyboardExtension):
    def __init__(self, animes):
        self.animes = animes

    def _extender(self):
        for anime in self.animes:
            anime_name = anime[1]
            anime_source_url = anime[2]

            self.base.kb.row_width = 3
            self.base.kb.insert(InlineKeyboardButton(anime_name, url=anime_source_url))
