from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers import register_handlers, register_buttons_callback


bot = Bot(token="5289843967:AAGvSL2RvJL56fubaPTeh-yDjeqmwennBho")
dp = Dispatcher(bot, storage=MemoryStorage())

register_handlers(dp)
register_buttons_callback(dp)

executor.start_polling(dp)
