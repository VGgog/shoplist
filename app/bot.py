from aiogram import Bot, types, Dispatcher, executor
from handlers import register_handlers

bot = Bot(token="5289843967:AAGvSL2RvJL56fubaPTeh-yDjeqmwennBho")
dp = Dispatcher(bot)


# def register_handlers(dp: Dispatcher):
#     dp.register_message_handler(start_menu, commands="start")


register_handlers(dp)
executor.start_polling(dp)

