from aiogram.dispatcher.filters import Text
from .bot import dispatcher as dp
from ..app import callbacks
from ..app import handlers

#message handlers
dp.register_message_handler(handlers.start.handler, commands=['start'], state='*')

#callback handlers
dp.register_callback_query_handler(callbacks.main_menu.MainMenu().handle, Text(startswith="main"), state='*')
dp.register_callback_query_handler(callbacks.anime_show.AnimeShow().handle, Text(startswith="anime_show"), state='*')
dp.register_callback_query_handler(callbacks.genre_filters.GenreFilters().handle, Text(startswith="genre_filters"), state='*')
