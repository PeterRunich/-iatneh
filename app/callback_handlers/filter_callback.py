from ..handlers.ask_filter_page_number_handler import ask_filter_page_number
from ..helpers.show_anime_with_photo import show_anime_with_photo
from ..keyboards.filter_keyboard import filter_kb_builder
from aiogram.utils.exceptions import MessageNotModified
from ..helpers.selected_genres import selected_genres
from ..handlers.ask_genre_name import ask_genre_name
from aiogram.dispatcher.filters import Text
from ._base_callback import BaseCallback
from ...database.db import Sqlite
from contextlib import suppress
from ..bot import dispatcher
import math
"""Callback обработчик клавиатуры с фильтрами (cqid = cq1)"""

@dispatcher.callback_query_handler(Text(startswith="cq1")) # callback текст приходит в виде "id callback handlera:action:arg1:arg2:arg3"
async def filter_callback(cq, callback_answer=True):
    await FilterCallback(cq, callback_answer)._init_()

class FilterCallback(BaseCallback):
    def __init__(self, cq, callback_answer):
        super().__init__(cq, callback_answer)

        self.last_page = math.ceil(Sqlite().count_genres() / 30)

    async def add_to_filter(self, genre_id):
        genre_ids = self.__parse_genre_ids()

        if self.message_text[-1] != ':': self.message_text += ','
        self.message_text += genre_id

        genre_ids.append(genre_id)
        kb = await filter_kb_builder(1, self.last_page, 30, genre_ids=genre_ids)
        await self.__send_edited_kb(kb)

    async def change_page_to(self, page_num):
        kb = await filter_kb_builder(int(page_num), self.last_page, 30, genre_ids=self.__parse_genre_ids())
        await self.__send_edited_kb(kb)

    async def ask_page_to_go(self):
        await ask_filter_page_number(self.chat_id, self.message_text, self.message_id)

    async def search(self):
        genre_ids = self.__parse_genre_ids()

        if genre_ids == ['']: await self.cq.answer(); return;

        self.callback_answer = False

        await show_anime_with_photo(self.chat_id, 'genre', genre_ids, Sqlite().find_anime_by_genre(genre_ids))

        await self.cq['message'].delete()

    async def remove_from_filter(self, genre_id):
        genre_ids = self.__parse_genre_ids()

        genre_ids.remove(genre_id)
        self.message_text = 'Фильтры:' + ','.join(genre_ids)

        kb = await filter_kb_builder(1, self.last_page, 30, genre_ids=genre_ids)
        await self.__send_edited_kb(kb)

    async def find_genre_by_name(self):
        await ask_genre_name(self.chat_id, self.__parse_genre_ids(), self.cq['message']['text'], self.message_id)

    async def show_selected_genres(self):
        await selected_genres(self.chat_id, self.__parse_genre_ids(), self.cq['message']['text'], self.message_id)

    async def back(self):
        kb = await filter_kb_builder(1, self.last_page, 30, genre_ids=self.__parse_genre_ids())

        await self.__send_edited_kb(kb)

    async def __send_edited_kb(self, kb):
        with suppress(MessageNotModified): # перехватывает ошибку о изменение контента сообщения на такой же контент
            await self.cq['message'].edit_text(self.message_text, reply_markup=kb)

    def __parse_genre_ids(self):
        return self.message_text.split(':')[1].split(',')
