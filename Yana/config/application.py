from aiogram import executor
from .bot import dispatcher
from .routes import *

executor.start_polling(dispatcher)
