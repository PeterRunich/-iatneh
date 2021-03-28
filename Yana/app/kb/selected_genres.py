from ._base_keyboard import BaseKeyboard, BaseKeyboardExtension
from aiogram.types import InlineKeyboardButton
from .components.genres_btns import GenreBtns
from .components.back_btn import Back

def selected_genres_build(genre, selected_genres_ids):
    callback_id = 'genre_filters'
    return BaseKeyboard(callback_id,
                        [GenreBtns(genre, selected_genres_ids), Back('Назад к фильтрам', 'genre_filters:change_page_to:1')]).kb
