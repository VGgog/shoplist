from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers import register_handlers
from keyboards import register_buttons_callback
from config import Config


bot = Bot(token=Config.token)
dp = Dispatcher(bot, storage=MemoryStorage())

register_handlers(dp)
register_buttons_callback(dp)

executor.start_polling(dp)
