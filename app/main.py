import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import settings
from app.database.init_db import check_db_connection, init_db
from app.handlers.category import router as category_router
from app.handlers.user import router as user_router
from app.logger import logger
from app.middleware.db_session import DatabaseSessionMiddleware
from app.middleware.user_middleware import UserMiddleware


# Initialize bot and dispatcher
bot = Bot(token=settings.bot_token.get_secret_value())
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Register middleware
dp.update.middleware.register(DatabaseSessionMiddleware())
dp.update.middleware.register(UserMiddleware())

# Register routers
dp.include_router(category_router)
dp.include_router(user_router)


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(
        'Добро пожаловать в Bookstore Bot! 📚\n\n'
        'Доступные команды:\n'
        '/categories - Управление книжными категориями\n'
        '/assign_role - Присвоение ролей пользователям (доступно только администраторам)'
    )


async def main():
    logger.info('Starting bot...')

    # Initialize a database and check connection
    if not check_db_connection():
        logger.error('Failed to connect to database. Exiting...')
        exit(1)
    init_db()
    logger.info('Database initialized successfully')

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
