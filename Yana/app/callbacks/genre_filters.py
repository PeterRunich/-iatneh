from ..helpers.show_anime_search_results import show_animes_with_photo
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified
from aiogram.types.callback_query import CallbackQuery
from ..kb.selected_genres import selected_genres_build
from ..kb.genre_filters import genre_filter_builder
from ..kb.geners_by_name import show_geners_by_name
from ...config.bot import dispatcher as dp
from ..kb.back_btn import back_btn_builder
from aiogram.types.message import Message
from ._base_callback import BaseCallback
from aiogram.types.chat import Chat
from contextlib import suppress
from ...config.bot import bot
from ...db.db import Sqlite
import math

class GenreFiltersStates(StatesGroup):
    filter_page_number_wait = State()
    gener_name_for_search_wait = State()

class GenreFilters(BaseCallback):
    async def handle(self, cq, callback_answer=True):
        self.last_page = math.ceil(Sqlite().count_genres() / 30)
        await super().handle(cq, callback_answer)

    async def add_to_filter(self, genre_id):
        genre_ids = self.__parse_genre_ids()

        if self.message_text[-1] != ':': self.message_text += ','
        self.message_text += genre_id

        genre_ids.append(genre_id)
        kb = await genre_filter_builder(1, self.last_page, 30, genre_ids=genre_ids)
        await self.__send_edited_kb(kb)

    async def change_page_to(self, page_num):
        kb = await genre_filter_builder(int(page_num), self.last_page, 30, genre_ids=self.__parse_genre_ids())
        await self.__send_edited_kb(kb)

    async def ask_page_to_go(self):
        kb = back_btn_builder('genre_filters:back_from_state:', 'Назад к фильтрам')
        state = dp.current_state(chat=self.chat_id)

        await state.update_data(current_page_num=1, text=self.message_text, message_id=self.message_id, last_page=self.last_page)
        await self.cq['message'].edit_text(f'Введите номер страницы до {self.last_page}', reply_markup=kb)

        await GenreFiltersStates.filter_page_number_wait.set()

    async def search(self):
        genre_ids = self.__parse_genre_ids()

        if genre_ids == ['']: await self.cq.answer(); return;

        self.callback_answer = False

        await show_animes_with_photo(self.chat_id, self.message_id, 'genre', genre_ids)

    async def remove_from_filter(self, genre_id):
        genre_ids = self.__parse_genre_ids()

        genre_ids.remove(genre_id)
        self.message_text = 'Фильтры:' + ','.join(genre_ids)

        kb = await genre_filter_builder(1, self.last_page, 30, genre_ids=genre_ids)
        await self.__send_edited_kb(kb)

    async def find_genre_by_name(self):
        kb = back_btn_builder('genre_filters:back_from_state:', 'Назад к фильтрам')
        state = dp.current_state(chat=self.chat_id)

        await state.update_data(current_page_num=1, text=self.message_text, message_id=self.message_id, last_page=self.last_page)
        await self.cq['message'].edit_text(f'Введи название', reply_markup=kb)

        await GenreFiltersStates.gener_name_for_search_wait.set()

    async def show_selected_genres(self):
        selected_genres = self.__parse_genre_ids()
        kb = selected_genres_build(Sqlite().get_genres_by_ids(selected_genres), selected_genres)

        await self.__send_edited_kb(kb)

    async def back_from_state(self):
        state = dp.current_state(chat=self.chat_id)
        data = await state.get_data()
        self.message_text = data['text']
        await state.finish()

        kb = await genre_filter_builder(data['current_page_num'], genre_ids=self.__parse_genre_ids())

        await self.__send_edited_kb(kb)

    async def __send_edited_kb(self, kb):
        with suppress(MessageNotModified): # перехватывает ошибку о изменение контента сообщения на такой же контент
            await self.cq['message'].edit_text(self.message_text, reply_markup=kb)

    def __parse_genre_ids(self):
        return self.message_text.split(':')[1].split(',')

@dp.message_handler(state=GenreFiltersStates.filter_page_number_wait)
async def recieve_page_number(msg, state):
    await msg.delete()
    data = await state.get_data()

    if not msg.text.isdigit() or int(msg.text) < 1 or int(msg.text) > data['last_page']:
        msg.text = 1

    cq = CallbackQuery(data=f'genre_filters:change_page_to:{msg.text}',
                       message=Message(text=data['text'],
                       message_id=int(data['message_id']),
                       chat=Chat(id=int(msg['chat']['id']))))

    await GenreFilters().handle(cq, callback_answer=False)


    await state.finish()

@dp.message_handler(state=GenreFiltersStates.gener_name_for_search_wait)
async def recieve_genre_name(msg, state):
    await msg.delete()
    data = await state.get_data()
    selected_genres = data['text'].split(':')[1].split(',')

    kb =  show_geners_by_name(Sqlite().find_genre_by_name(msg.text), selected_genres)

    await bot.edit_message_text(data['text'], msg['chat']['id'], data['message_id'], reply_markup=kb)
    await state.finish()
