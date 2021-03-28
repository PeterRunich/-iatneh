from ._base_keyboard import BaseKeyboard, BaseKeyboardExtension
from aiogram.types import InlineKeyboardButton
from .components.genres_btns import GenreBtns
from .components.back_btn import Back

def show_geners_by_name(genre, selected_genres_ids):
    callback_id = 'genre_filters'
    return BaseKeyboard(callback_id,
                        [Back('Назад к фильтрам', 'genre_filters:change_page_to:1'), GenreBtns(genre, selected_genres_ids)]).kb
