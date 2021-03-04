from ..keyboards.anime_show_keyboard import anime_show_kb_builder
from ..keyboards.filter_keyboard import filter_kb_builder
from aiogram.dispatcher.filters import Text
from ...database.db import Sqlite
from ..bot import bot, dispatcher
"""Callback обработчик клавиатуры с фильтрами (cqid = cq1)"""

@dispatcher.callback_query_handler(Text(startswith="cq1")) # callback текс приходит в виде "id callback handlera:action:arg1:arg2:arg3"
async def process_callback_button1(cq):
    action = cq.data.split(':')[1] # выделяем действие которое будет обработано
    args   = cq.data.split(':')[2:] # выделяем лист аргументов

    if action == 'move_to':
        kb = await filter_kb_builder(int(args[0]), 30)
    elif action == 'add_to_filter':
        cq['message']['text'] += ',' + args[0] # в cq хранится старый словарь с информацией о старом inline keyboard там есть поле cq['message']['text'] там хранится все жанры выбранные пользователем, тут мы добавляем просто ещё один жанр к этой строке
        kb = await filter_kb_builder(1, 30)
    elif action == 'no_action':
        await cq.answer() # нужно отвечать callback кнопкам иначе у пользователя повиснит белый таймер
        return True
    elif action == 'search':
        await cq.answer() # нужно отвечать callback кнопкам иначе у пользователя повиснит белый таймер
        genres = cq['message']['text'].split(',')[1:] # в cq хранится старый словарь с информацией о старом inline keyboard там есть поле cq['message']['text'] там хранится все жанры выбранные пользователем, тут мы вытаскиваем все жанры для дальнейшего поиска
        kb = await anime_show_kb_builder(Sqlite().find_anime_by_genre(genres))
        await bot.send_message(cq['message']['chat']['id'], 'Результаты', reply_markup=kb)
        return True

    await bot.edit_message_text(cq['message']['text'],
    chat_id=cq['message']['chat']['id'],
    message_id=cq['message']['message_id'],
    reply_markup=kb)

    await cq.answer()
