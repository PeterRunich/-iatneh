from ..keyboards.anime_show_keyboard import anime_show_kb_builder
from aiogram.utils.exceptions import MessageNotModified
from aiogram.types.input_media import InputMediaPhoto
from aiogram.dispatcher.filters import Text
from ._base_callback import BaseCallback
from ...database.db import Sqlite
from ..bot import dispatcher, bot
from contextlib import suppress

import asyncio
import time
"""Callback обработчик клавиатуры с покахом аниме (cqid = cq2)"""

@dispatcher.callback_query_handler(Text(startswith="cq2")) # callback текст приходит в виде "id callback handlera:action:arg1:arg2:arg3"
async def show_anime_with_photo_callback(cq):
    await ShowAnimeCallback(cq)._init_()

class ShowAnimeCallback(BaseCallback):
    def __init__(self, cq):
        super().__init__(cq)
        self.last_page = int(cq['message']['reply_markup']['inline_keyboard'][-1][2]['text'].split('/')[-1])
        self.img_ids, self.search_type, self.query = cq['message']['text'].split(':')
        self.img_ids = self.img_ids.split(' ')

    async def change_page_to(self, page_num):
        animes = self.__get_animes(int(page_num))
        kb = await anime_show_kb_builder(animes, self.last_page, int(page_num))

        await self.__send_edited_kb(kb)
        await self.__edit_poster_imgs(animes)


    async def __send_edited_kb(self, kb):
        with suppress(MessageNotModified): # перехватывает ошибку о изменение контента сообщения на такой же контент
            await self.cq['message'].edit_text(self.message_text, reply_markup=kb)

    async def __edit_poster_imgs(self, animes):
        default_img = InputMediaPhoto('https://pbs.twimg.com/profile_images/433369941736456192/YyHTQQ5M.jpeg')
        # tasks = []

        with suppress(MessageNotModified):
            for i in range(10):
                if i > len(animes) - 1:
                    await bot.edit_message_media(media=default_img, chat_id=self.chat_id, message_id=self.img_ids[i])
                else:
                    await bot.edit_message_media(media=InputMediaPhoto(media=animes[i][3]), chat_id=self.chat_id, message_id=self.img_ids[i])
            # tasks.append(asyncio.create_task(
            # [await task for task in tasks]

    def __parse_genre_ids(self):
        return self.message_text.split(':')[1].split(',')

    def __get_animes(self, page_num):
        offset = (page_num - 1) * 10

        if self.search_type == 'Поиск по жанрам':
            return Sqlite().find_anime_by_genre(self.query.split(','), 10, offset)
        elif self.search_type == 'Поиск по имени':
            return Sqlite().find_anime_by_name(self.query, 10, offset)
