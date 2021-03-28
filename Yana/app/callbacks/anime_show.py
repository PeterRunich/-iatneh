from ..kb.show_anime_search_results import show_anime_search_results_build
from aiogram.utils.exceptions import MessageNotModified
from aiogram.types.input_media import InputMediaPhoto
from ..kb.main_menu import main_menu_builder
from ...config.bot import dispatcher as dp
from ._base_callback import BaseCallback
from contextlib import suppress
from ...config.bot import bot
from ...db.db import Sqlite

class AnimeShow(BaseCallback):
    async def handle(self, cq):
        self.last_page = int(cq['message']['reply_markup']['inline_keyboard'][-2][2]['text'].split('/')[-1])
        self.img_ids, self.search_type, self.query = cq['message']['text'].split(':')
        self.img_ids = self.img_ids.split(' ')
        await super().handle(cq)

    async def to_main_menu(self):
        [await bot.delete_message(self.chat_id, img_msg_id) for img_msg_id in self.img_ids]

        kb = main_menu_builder()
        await self.cq['message'].edit_text('Главное меню', reply_markup=kb)

    async def change_page_to(self, page_num):
        animes = self.__get_animes(int(page_num))
        kb = show_anime_search_results_build(animes, self.last_page, int(page_num))

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
