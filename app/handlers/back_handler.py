from ..helpers.start_kb_helper import start_kb
from aiogram.dispatcher.filters import Text
from ..bot import dispatcher
"""Обнуляет стейт и ставит клавиатуру главного меню"""

@dispatcher.message_handler(Text(equals="назад", ignore_case=True), state="*")
# ВНИМАНИЕ back_dialog используется в search_filter_handler
async def back_dialog(msg, state=False): # если хочеешь обнулить стейт то не забудь передать аргументом
    if state: await state.finish()
    await start_kb(msg)
