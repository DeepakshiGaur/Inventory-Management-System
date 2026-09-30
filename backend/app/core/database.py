from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import DATABASE_URL


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# def test_connection():
#     try:
#         with engine.connect() as connection:
#             result = connection.execute(text("SELECT 1"))
#             print("Database connection successful:", result.scalar())
#     except Exception as error:
#         print("Database connection failed:", error)