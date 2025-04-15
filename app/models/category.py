from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.db import Base


class Category(Base):
    __tablename__ = 'categories'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, unique=True)
    is_active = Column(Boolean, default=False)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True, index=True)
