from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.db import Base


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_active = Column(Boolean)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)


# todo book model
