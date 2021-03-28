from ..kb.show_anime_search_results import show_anime_search_results_build
from aiogram.types.input_media import InputMediaPhoto, MediaGroup
from ..kb.back_btn import back_btn_builder
from ...config.bot import bot
from ...db.db import Sqlite
import math

async def show_animes_with_photo(chat_id, message_id, search_by_type, query):
    if search_by_type == 'genre':
        records = Sqlite().find_anime_by_genre(query)
    elif search_by_type == 'name':
        records = Sqlite().find_anime_by_name(query)

    if records == []:
        kb = back_btn_builder('main:to_main_menu:')
        await bot.edit_message_text('Результаты: подходящих записей не найдено', chat_id, message_id, reply_markup=kb)
        return

    posters = [InputMediaPhoto(media=record[3]) for record in records[:10]]
    media_msgs = await bot.send_media_group(chat_id, media=MediaGroup(medias=posters))

    str_with_msg_ids = ' '.join([str(media_msg['message_id']) for media_msg in media_msgs])

    kb = show_anime_search_results_build(records[:10], math.ceil(len(records) / 10))

    await bot.delete_message(chat_id, message_id)

    if search_by_type == 'genre':
        query = ','.join(query)
        await bot.send_message(chat_id, f'{str_with_msg_ids}:Поиск по жанрам:{query}', reply_markup=kb)
    elif search_by_type == 'name':
        await bot.send_message(chat_id, f'{str_with_msg_ids}:Поиск по имени:{query}', reply_markup=kb)
