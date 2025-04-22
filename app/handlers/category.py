from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.decorators.role_check import require_role
from app.models.models import User, UserRole
from app.schemas import CategoryCreate, CategoryUpdate
from app.services.category_service import CategoryService


router = Router()


class CategoryStates(StatesGroup):
    waiting_for_category_name = State()
    waiting_for_category_update = State()


@router.message(Command('categories'))
async def category_menu(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='📋 Список Категорий', callback_data='list_categories'
                ),
                InlineKeyboardButton(
                    text='➕ Добавить Категорию', callback_data='add_category'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='✏️ Обновить Категорию', callback_data='update_category'
                ),
                InlineKeyboardButton(
                    text='❌ Удалить Категорию', callback_data='delete_category'
                ),
            ],
        ]
    )
    await message.answer('Меню управления категориями:', reply_markup=keyboard)


@router.callback_query(lambda c: c.data == 'list_categories')
async def list_categories(callback_query: CallbackQuery, db_session: Session):
    category_service = CategoryService(db_session)
    categories = category_service.get_all_categories()

    if not categories:
        await callback_query.message.answer('Категорий не найдено.')
        return

    message = '📚 Категории:\n\n'
    for category in categories:
        message += f"• {category.name}\n"

    await callback_query.message.answer(message)


@router.callback_query(lambda c: c.data == 'add_category')
@require_role(UserRole.ADMIN)
async def add_category(callback_query: CallbackQuery, state: FSMContext, user):
    await callback_query.message.answer(
        'Напишите название категории и ее описание в формате:\n' 'Название: Описание'
    )
    await state.set_state(CategoryStates.waiting_for_category_name)


@router.message(CategoryStates.waiting_for_category_name)
@require_role(UserRole.ADMIN)
async def handle_category_add(
    message: Message, state: FSMContext, db_session: Session, user: User
):
    try:
        name, description = message.text.split(':', 1)
        category_data = CategoryCreate(
            name=name.strip(), description=description.strip()
        )
    except (ValueError, ValidationError):
        await message.answer(
            'Неправильный формат. Пожалуйста, используйте формат: название: описание'
        )
        return

    category_service = CategoryService(db_session)
    category = category_service.create_category(name=category_data.name)

    await message.answer(f'✅ Категория {category.name} успешно добавлена!')
    await state.clear()


@router.callback_query(lambda c: c.data == 'update_category')
@require_role(UserRole.ADMIN)
async def update_category(
    callback_query: CallbackQuery, db_session: Session, user: User
):
    category_service = CategoryService(db_session)
    categories = category_service.get_all_categories()

    keyboard = []
    for category in categories:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=category.name, callback_data=f"update_category_{category.id}"
                )
            ]
        )

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback_query.message.answer(
        'Выберите категорию для обновления', reply_markup=reply_markup
    )


@router.callback_query(lambda c: c.data.startswith('update_category_'))
@require_role(UserRole.ADMIN)
async def handle_category_update(
    callback_query: CallbackQuery, state: FSMContext, user: User
):
    category_id = int(callback_query.data.split('_')[-1])
    await state.update_data(category_id=category_id)
    await callback_query.message.answer(
        'Пожалуйста, укажите новое название категории и ее описание в формате:\n'
        'Название: Описание'
    )
    await state.set_state(CategoryStates.waiting_for_category_update)


@router.message(CategoryStates.waiting_for_category_update)
@require_role(UserRole.ADMIN)
async def process_category_update(
    message: Message, state: FSMContext, db_session: Session, user: User
):
    try:
        name, description = message.text.split(':', 1)
        category_data = CategoryUpdate(
            name=name.strip(), description=description.strip()
        )
    except (ValueError, ValidationError):
        await message.answer(
            'Неправильный формат. Пожалуйста, используйте формат: название: описание'
        )
        return

    state_data = await state.get_data()
    category_service = CategoryService(db_session)
    category = category_service.update_category(
        category_id=state_data['category_id'],
        name=category_data.name,
        description=category_data.description,
    )

    if not category:
        await message.answer('❌ Категория не найдена.')
        return

    await message.answer('✅ Категория успешно обновлена!')
    await state.clear()


@router.callback_query(lambda c: c.data == 'delete_category')
@require_role(UserRole.ADMIN)
async def delete_category(
    callback_query: CallbackQuery, db_session: Session, user: User
):
    category_service = CategoryService(db_session)
    categories = category_service.get_all_categories()

    keyboard = []
    for category in categories:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=category.name, callback_data=f"delete_category_{category.id}"
                )
            ]
        )

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await callback_query.message.answer(
        'Выберите категорию для удаления:', reply_markup=reply_markup
    )


@router.callback_query(lambda c: c.data.startswith('delete_category_'))
@require_role(UserRole.ADMIN)
async def handle_category_delete(
    callback_query: CallbackQuery, db_session: Session, user: User
):
    category_id = int(callback_query.data.split('_')[-1])
    category_service = CategoryService(db_session)

    success = category_service.delete_category(category_id)
    if success:
        await callback_query.message.answer('✅ Категория успешно удалена')
    else:
        await callback_query.message.answer('❌ Категория не найдена')
