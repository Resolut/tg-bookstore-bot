import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from app.config import config
from app.logger import logger


# Initialize bot and dispatcher
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


@dp.message()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Hello!')


# Запуск процесса поллинга новых апдейтов
async def main():
    logger.info(f"Running {__name__}")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
