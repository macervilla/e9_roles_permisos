import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


def get_database_url() -> str:
    """
    Devuelve la URL de conexión utilizando DATABASE_URL
    o construyéndola a partir de las variables individuales.
    """

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return database_url

    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    return (
        f"mysql+pymysql://"
        f"{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )


def create_db_engine():
    return create_engine(
        get_database_url(),
        pool_pre_ping=True,
    )


engine = create_db_engine()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()