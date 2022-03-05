from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import Config


bot = Bot(token=Config.token)
dp = Dispatcher(bot, storage=MemoryStorage())
