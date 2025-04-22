from sqlalchemy import inspect, text

from app.database.connection import SessionLocal, engine
from app.models.models import Base, User, UserRole


# async def init_models():
#     async with engine.begin() as conn:
#         # Create all tables
#         await conn.run_sync(Base.metadata.create_all)


def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create a flag for the first user being admin
    inspector = inspect(engine)
    if 'users' in inspector.get_table_names():
        with SessionLocal() as db:
            # Check if any user exists
            user_count = db.query(User).count()
            if user_count == 0:
                # Set a flag in a database to mark that the first user should be admin
                # We'll use a special placeholder user with ID -1 to indicate this
                admin_placeholder = User(
                    id=-1,
                    telegram_id=-1,
                    username='first_user_will_be_admin',
                    role=UserRole.ADMIN,
                )
                db.add(admin_placeholder)
                db.commit()
                print('First user flag created. Next user to register will be admin.')


def check_db_connection():
    try:
        # Try to create a connection
        with engine.connect() as connection:
            # Try to execute a simple query
            connection.execute(text('SELECT 1;'))
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False
