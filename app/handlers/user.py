from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.orm import Session

from app.decorators.role_check import require_role
from app.models.models import User, UserRole
from app.services.user_service import UserService


router = Router(name='user_router')


@router.message(Command('assign_role'))
@require_role(UserRole.ADMIN)
async def assign_role(message: types.Message, db_session: Session, user: User) -> None:
    user_service = UserService(db_session)
    users = user_service.get_all_users_except(message.from_user.id)

    if not users:
        await message.answer('Пользователи не найдены')
        return

    keyboard = []
    for target_user in users:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"@{target_user.username} ({target_user.role.value})",
                    callback_data=f"assign_role_{target_user.id}",
                )
            ]
        )

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.answer(
        'Выберите пользователя для изменения роли:', reply_markup=reply_markup
    )


@router.callback_query(lambda c: c.data.startswith('assign_role_'))
@require_role(UserRole.ADMIN)
async def handle_role_selection(
    callback_query: types.CallbackQuery, db_session: Session, user: User
) -> None:
    user_id = int(callback_query.data.split('_')[-1])
    user_service = UserService(db_session)
    target_user = user_service.get_user_by_id(user_id)

    if not target_user:
        await callback_query.message.answer('❌ Пользователь не найден')
        return

    keyboard = [
        [
            InlineKeyboardButton(
                text='Admin', callback_data=f"set_role_{user_id}_admin"
            ),
            InlineKeyboardButton(
                text='Client', callback_data=f"set_role_{user_id}_client"
            ),
            InlineKeyboardButton(
                text='Supplier', callback_data=f"set_role_{user_id}_supplier"
            ),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback_query.message.answer(
        f"Выберите новую роль для @{target_user.username}:", reply_markup=reply_markup
    )


@router.callback_query(lambda c: c.data.startswith('set_role_'))
@require_role(UserRole.ADMIN)
async def set_user_role(
    callback_query: types.CallbackQuery, db_session: Session, user: User
) -> None:
    _, user_id, role = callback_query.data.split('_')
    user_id = int(user_id)

    user_service = UserService(db_session)
    target_user = user_service.update_user_role(user_id, UserRole(role))

    if not target_user:
        await callback_query.message.answer('❌ Пользователь не найден')
        return

    await callback_query.message.answer(
        f"✅ Роль успешно обновлена!\n" f"@{target_user.username} теперь {role}."
    )
