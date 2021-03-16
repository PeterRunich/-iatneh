from ..keyboards.selected_genres_kb import selected_genres_kb
from ...database.db import Sqlite
from ..bot import bot

async def selected_genres(chat_id, genre_ids, message_text, message_id):
    await bot.delete_message(chat_id, message_id)

    kb = await selected_genres_kb(Sqlite().get_genres(limit=10000, offset=0), genre_ids)
    await bot.send_message(chat_id, message_text, reply_markup=kb)
