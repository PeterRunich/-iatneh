from ..helpers.show_anime_search_results import show_animes_with_photo
from aiogram.dispatcher.filters.state import State, StatesGroup
from ..kb.genre_filters import genre_filter_builder
from ..kb.main_menu import main_menu_builder
from ..kb.back_btn import back_btn_builder
from ...config.bot import dispatcher as dp
from ._base_callback import BaseCallback
from ...config.bot import bot

class SearchByName(StatesGroup):
    waiting_for_name = State()

class MainMenu(BaseCallback):
    async def to_search_by_name(self):
        kb = back_btn_builder('main:to_main_menu:')
        state = dp.current_state(chat=self.chat_id)
        await state.update_data(message_id=self.message_id)

        await self.cq['message'].edit_text('Введите название', reply_markup=kb)
        await SearchByName.waiting_for_name.set()

    async def to_filters(self):
        kb = await genre_filter_builder(1)
        await self.cq['message'].edit_text('Фильтры:', reply_markup=kb)

    async def to_main_menu(self):
        kb = main_menu_builder()
        await self.cq['message'].edit_text('Главное меню', reply_markup=kb)

@dp.message_handler(state=SearchByName.waiting_for_name)
async def search(msg, state):
    data = await state.get_data()
    message_id = data['message_id']
    await msg.delete()
    await state.finish()

    await show_animes_with_photo(msg['chat']['id'], message_id, 'name', msg.text)
