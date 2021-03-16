from ..keyboards.finded_genre_by_name_kb import finded_genre_by_name_kb
from aiogram.dispatcher.filters.state import State, StatesGroup
from ...database.db import Sqlite
from ..bot import bot, dispatcher
import json

class AskGenreName(StatesGroup):
    waiting_for_genre_name = State()

async def ask_genre_name(chat_id, genre_ids, message_text, message_id):
    ask_msg = await bot.send_message(chat_id, 'Напиши название жанра')
    await AskGenreName.waiting_for_genre_name.set()

    state = dispatcher.current_state(chat=chat_id)
    await state.update_data(cq_data=json.dumps({ 'message_text': message_text, 'chat_id': chat_id, 'genre_ids': genre_ids}), ask_msg_id=ask_msg.message_id)

    await bot.delete_message(chat_id, message_id)

@dispatcher.message_handler(state=AskGenreName.waiting_for_genre_name)
async def recieve_genre_name(msg, state):
    msg.text = msg.text.replace(':', '') # чтобы не сломался callback парсер
    data = await state.get_data()
    data_cq = json.loads(data['cq_data'])

    kb = await finded_genre_by_name_kb(Sqlite().find_genre_by_name(msg.text), data_cq['genre_ids'])
    await bot.send_message(data_cq['chat_id'], data_cq['message_text'], reply_markup=kb)

    await msg.delete()
    await bot.delete_message(data_cq['chat_id'], data['ask_msg_id'])

    await state.finish()
