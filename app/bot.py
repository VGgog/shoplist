from aiogram import Bot, types, Dispatcher, executor

from handlers import register_handlers, register_group_buttons_callback


bot = Bot(token="5289843967:AAGvSL2RvJL56fubaPTeh-yDjeqmwennBho")
dp = Dispatcher(bot)

register_handlers(dp)
register_group_buttons_callback(dp)

executor.start_polling(dp)

