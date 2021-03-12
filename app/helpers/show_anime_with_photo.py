from ..keyboards.anime_show_keyboard import anime_show_kb_builder
from ..bot import bot

async def generate_message(animes, chat_id):
    if animes == []:
        await bot.send_message(chat_id, "Результаты: подходящих записей не найдено.")
    for anime in animes:
        kb =  await anime_show_kb_builder([anime])
        if kb['inline_keyboard'] != []:
            await bot.send_photo(chat_id, anime[3], reply_markup = kb)
