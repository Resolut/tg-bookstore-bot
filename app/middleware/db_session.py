from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, Update

from app.database.connection import SessionLocal


class DatabaseSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery | Update,
        data: Dict[str, Any],
    ) -> Any:
        with SessionLocal() as session:
            data['db_session'] = session

            try:
                # Pass the session directly as a keyword argument
                result = await handler(event, data)
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                raise e
