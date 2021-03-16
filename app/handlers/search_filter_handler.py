from ..helpers.show_anime_with_photo import show_anime_with_photo
from aiogram.dispatcher.filters.state import State, StatesGroup
from ..keyboards.back_keyboard import back_kb_builder
from ..helpers.start_kb_helper import start_kb
from aiogram.dispatcher.filters import Text
from .back_handler import back_dialog
from ...database.db import Sqlite
from ..bot import dispatcher
"""Обработчик поиска аниме по имени"""

class Search(StatesGroup): # отвечает за описание FSM маршрута
    waiting_for_name = State() # определяем возможный стейт

@dispatcher.message_handler(Text(equals="поиск", ignore_case=True), state="*")
async def search_by_name_dialog(msg):
    kb = await back_kb_builder()
    await msg.answer('Напиши название, если хотите прервать поиск нажми кнопку', reply_markup=kb)
    await Search.waiting_for_name.set() # переходим на состояние waiting_for_name

@dispatcher.message_handler(state=Search.waiting_for_name) # обработчик состояния waiting_for_name
async def search(msg, state):
    if msg.text == 'Назад': # если команда Назад то обнуляем состояние
        await back_dialog(msg, state)
        return True # прерываем функцию т.к пользователь не захотел идти дальше

    await state.finish() # обнуляем состояние т.к это конечное состояние
    await start_kb(msg) # возваращаем клавиатуру главного меню /start
    await msg.answer('Поиск по "' + msg.text + '"')
    
    await show_anime_with_photo(msg['chat']['id'], 'name', msg.text, Sqlite().find_anime_by_name(msg.text))
