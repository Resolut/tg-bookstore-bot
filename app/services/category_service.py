from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Category


class CategoryService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_categories(self) -> list[Category]:
        result = self.db.execute(select(Category))
        return result.scalars().all()

    def get_category_by_id(self, category_id: int) -> Category | None:
        result = self.db.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()

    def create_category(self, name: str) -> Category:
        category = Category(name=name)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update_category(
        self, category_id: int, name: str, description: str | None = None
    ) -> Category | None:
        category = self.get_category_by_id(category_id)
        if category:
            category.name = name
            category.updated_at = datetime.now(UTC)
            self.db.commit()
            self.db.refresh(category)
        return category

    def delete_category(self, category_id: int) -> bool:
        category = self.get_category_by_id(category_id)
        if category:
            self.db.delete(category)
            self.db.commit()
            return True
        return False
