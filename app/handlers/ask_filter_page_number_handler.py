from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.callback_query import CallbackQuery
from ..callback_handlers import filter_callback as fc
from aiogram.types.message import Message
from aiogram.types.chat import Chat
from ..bot import bot, dispatcher
import json
"""Спрашивает пользователя на какую странцу с фильтрами он хочет перейти. Вызов в filter_callback"""

class AskPage(StatesGroup):
    waiting_for_page_number = State()

async def ask_filter_page_number(chat_id, message_text, message_id):
    ask_msg = await bot.send_message(chat_id, 'Напиши странцу')
    await AskPage.waiting_for_page_number.set()

    state = dispatcher.current_state(chat=chat_id)
    await state.update_data(cq_data=json.dumps({ 'text': message_text, 'chat_id': chat_id, 'message_id': message_id }), ask_msg_id=ask_msg.message_id)

@dispatcher.message_handler(state=AskPage.waiting_for_page_number)
async def recieve_page_number(msg, state):
    msg.text = msg.text.replace(':', '') # чтобы не сломался callback парсер
    data = await state.get_data()
    data_cq = json.loads(data['cq_data'])

    cq = CallbackQuery(data=f'cq1:go_to_page:{msg.text}', message=Message(text=data_cq['text'], message_id=int(data_cq['message_id']), chat=Chat(id=int(data_cq['chat_id'])))) #создаём программно callback чтобы успешно обработать его в filter_callback
    await fc.filter_callback(cq)

    await msg.delete()
    await bot.delete_message(data_cq['chat_id'], data['ask_msg_id'])

    await state.finish()
