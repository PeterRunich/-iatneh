from ..keyboards.filter_keyboard import filter_kb_builder
from aiogram.dispatcher.filters import Text
from ...database.db import Sqlite
from ..bot import dispatcher
import math
"""Обработчик кнопки фильтры, выводит страницы с фильтрами"""

@dispatcher.message_handler(Text(equals="фильтры", ignore_case=True), state="*")
async def filters_dialog(msg):
    kb = await filter_kb_builder(1, math.ceil(Sqlite().count_genres() / 30), 30)
    await msg.answer('Фильтры:', reply_markup=kb)
