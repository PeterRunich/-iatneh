from ..keyboards.start_keyboard import start_kb_builder
"""Вспомогающий метод который поставит клавиатуру из главного меню"""

async def start_kb(msg):
        kb = await start_kb_builder()

        await msg.reply('.', reply_markup=kb)
