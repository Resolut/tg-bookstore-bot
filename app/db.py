from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


engine = create_engine('sqlite:///bookstore_bot.db', echo=True)
session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
