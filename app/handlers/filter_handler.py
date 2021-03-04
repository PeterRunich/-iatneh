from ..keyboards.filter_keyboard import filter_kb_builder
from aiogram.dispatcher.filters import Text
from ..bot import dispatcher
"""Обработчик кнопки фильтры, выводит страницы с фильтрами"""

@dispatcher.message_handler(Text(equals="фильтры", ignore_case=True), state="*")
async def filters_dialog(msg):
    kb = await filter_kb_builder(1, 30)
    await msg.answer('Фильтры:', reply_markup=kb)
