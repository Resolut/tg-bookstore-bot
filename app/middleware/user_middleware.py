from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, Update

from app.models.models import UserRole
from app.services.user_service import UserService


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery | Update,
        data: Dict[str, Any],
    ) -> Any:
        # Look for database session in multiple possible keys
        db = data.get('db_session')

        if not db:
            raise ValueError('Database session not available in middleware chain')

        user_service = UserService(db)

        # Get user ID based on an event type
        if isinstance(event, Update):
            actual_event = event.event
            if actual_event is None:
                return await handler(event, data)
            event_for_user = actual_event
        else:
            event_for_user = event

        if isinstance(event_for_user, Message):
            telegram_id = event_for_user.from_user.id
            username = event_for_user.from_user.username or str(
                event_for_user.from_user.id
            )
            message = event_for_user
        else:  # CallbackQuery
            telegram_id = event_for_user.from_user.id
            username = event_for_user.from_user.username or str(
                event_for_user.from_user.id
            )
            message = event_for_user.message

        user = user_service.get_user_by_telegram_id(telegram_id)

        # Check if this should be the first admin (if placeholder exists)
        should_be_admin = False
        if not user:
            # Check if this is the first real user and should be admin
            first_user_flag = user_service.get_first_user_flag()
            if first_user_flag:
                should_be_admin = True
                # Remove the placeholder
                user_service.delete_user(first_user_flag.id)

        if not user:
            # Create new user, possibly as admin
            user = user_service.create_user(
                telegram_id=telegram_id,
                username=username,
                role=UserRole.ADMIN if should_be_admin else UserRole.CLIENT,
            )

            if should_be_admin:
                await message.answer(
                    '🎉 Поздравляем! Вы первый пользователь бота,'
                    ' поэтому вам присвоена роль Администратора'
                )

        # Add user as both a data key and a direct kwargs parameter
        data['user'] = user

        # Pass all middleware data as kwargs to handlers
        return await handler(event, data)
