from functools import wraps
from typing import Any, Awaitable, Callable

from aiogram.types import CallbackQuery, Message, Update

from app.models.models import UserRole


def require_role(required_role: UserRole):
    def decorator(
        func: Callable[[Message | Update | CallbackQuery, ...], Awaitable[Any]],
    ):
        @wraps(func)
        async def wrapper(event: Message | Update | CallbackQuery, *args, **kwargs):
            # A user is passed as a named parameter from middleware
            # Check if a user is in kwargs
            user = kwargs.get('user')

            # If not found in kwargs, try to find it in args
            if not user and args:
                for arg in args:
                    if isinstance(arg, dict) and 'user' in arg:
                        user = arg.get('user')
                        break

            # Validate user is found
            if not user:
                if isinstance(event, (Message, CallbackQuery)):
                    await event.answer(
                        '❌ Пользователь не идентифицирован. Попробуйте снова.'
                    )
                return None

            # Compare roles
            if user.role != required_role:
                if isinstance(event, (Message, CallbackQuery)):
                    await event.answer(
                        f"❌ Эта команда доступна только для {required_role.value}(-ов)."
                    )
                return None

            # Call the handler with original arguments
            return await func(event, *args, **kwargs)

        return wrapper

    return decorator
