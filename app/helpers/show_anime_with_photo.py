from aiogram.types.input_media import InputMediaPhoto, MediaGroup
from ..keyboards.anime_show_keyboard import anime_show_kb_builder
from ..bot import bot
import math

async def show_anime_with_photo(chat_id, search_by_type, query, animes):
    if animes == []: await bot.send_message(chat_id, 'Результаты: подходящих записей не найдено.'); return;

    posters = [InputMediaPhoto(media=anime[3]) for anime in animes[:10]]

    media_msgs = await bot.send_media_group(chat_id, media=MediaGroup(medias=posters))

    str_with_msg_ids = ' '.join([str(media_msg['message_id']) for media_msg in media_msgs])

    kb = await anime_show_kb_builder(animes[:10], math.ceil(len(animes) / 10))

    if search_by_type == 'genre':
        query = ','.join(query)
        await bot.send_message(chat_id, f'{str_with_msg_ids}:Поиск по жанрам:{query}', reply_markup=kb)
    elif search_by_type == 'name':
        await bot.send_message(chat_id, f'{str_with_msg_ids}:Поиск по имени:{query}', reply_markup=kb)
