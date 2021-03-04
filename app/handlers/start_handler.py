from ..keyboards.start_keyboard import start_kb_builder
from aiogram.dispatcher.filters import Command
from ..bot import dispatcher
"""Обработчик главного меню"""

@dispatcher.message_handler(Command(['start'], ignore_case=True), state="*")
async def start_dialog(msg):
    kb = await start_kb_builder()

    await msg.answer('Главное меню', reply_markup=kb)
