from aiogram import executor

from handlers.handler import register_handlers
from keyboards.callbacks import register_buttons_callback
from bot import dp

register_handlers(dp)
register_buttons_callback(dp)

executor.start_polling(dp)
