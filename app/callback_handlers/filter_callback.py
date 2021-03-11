from ..handlers.ask_filter_page_number_handler import ask_filter_page_number
from ..keyboards.anime_show_keyboard import anime_show_kb_builder
from ..keyboards.filter_keyboard import filter_kb_builder
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher.filters import Text
from ...database.db import Sqlite
from ..bot import bot, dispatcher
from contextlib import suppress

"""Callback обработчик клавиатуры с фильтрами (cqid = cq1)"""

@dispatcher.callback_query_handler(Text(startswith="cq1")) # callback текс приходит в виде "id callback handlera:action:arg1:arg2:arg3"
async def filter_callback(cq):
    action = cq.data.split(':')[1] # выделяем действие которое будет обработано
    args   = cq.data.split(':')[2:] # выделяем лист аргументов

    if action == 'move_to':
        kb = await filter_kb_builder(int(args[0]), 30)

    elif action == 'add_to_filter':
        cq['message']['text'] += ',' + args[0] # в cq хранится старый словарь с информацией о старом inline keyboard там есть поле cq['message']['text'] там хранится все жанры выбранные пользователем, тут мы добавляем просто ещё один жанр к этой строке
        kb = await filter_kb_builder(1, 30)

    elif action == 'no_action':
        await cq.answer()
        return

    elif action == 'search':
        genres = cq['message']['text'].split(',')[1:] # в cq хранится старый словарь с информацией о старом inline keyboard там есть поле cq['message']['text'] там хранится все жанры выбранные пользователем, тут мы вытаскиваем все жанры для дальнейшего поиска

        if genres == []:
            await cq.answer()
            return # если жанры не выбранны

        kb = await anime_show_kb_builder(Sqlite().find_anime_by_genre(genres))
        await bot.send_message(cq['message']['chat']['id'], f"Результаты: {' подходящих записей не найдено.' if kb['inline_keyboard'] == [] else ''}", reply_markup=kb)
        await cq.answer()
        await bot.delete_message(cq['message']['chat']['id'], cq['message']['message_id']) # удаляем inline панель с жанрами
        return

    elif action == 'go_to_page':
        if args == ['']: # если в аргументе не пришла страница то спрашиваем полльзователя
            await ask_filter_page_number(cq['message']['chat']['id'], cq['message']['text'], cq['message']['message_id'])
            await cq.answer()
            return

        page_number = args[0]
        if not page_number.isdigit() or int(page_number) < 1 or int(page_number) > 1000:
            return

        kb = await filter_kb_builder(int(page_number), 30)

    with suppress(MessageNotModified): # перехватывает ошибку о изменение контента сообщения на такой же контент
        await bot.edit_message_text(cq['message']['text'],
        chat_id=cq['message']['chat']['id'],
        message_id=cq['message']['message_id'],
        reply_markup=kb)

    if action not in ['go_to_page']: # т.к действия в списке вызваны из кода то нам не надо отправлять на сервер сообшение о успешной обработке callback
        await cq.answer()
