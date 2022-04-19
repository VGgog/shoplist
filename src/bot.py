import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.handlers import register_handlers
from bot.keyboards import register_buttons_callback
from config import Config


bot = Bot(token=Config.token)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

register_handlers(dp)
register_buttons_callback(dp)

executor.start_polling(dp)
