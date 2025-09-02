from decouple import config

from sqlalchemy import create_engine, text


def get_database_url(use_pooling=True):
    db_url_env = config("DATABASE_URL", cast=str)
    if use_pooling:
        db_url_env = config("DATABASE_URL_POOL", cast=str)
        # db_url_env = "postgresql://neondb_owner:npg_OuY3PWAz2DqM@ep-polished-darkness-a4rgg5r7-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"
    if db_url_env.startswith("postgres://"):
        return db_url_env.replace("postgres://", "postgresql://", 1)
    return db_url_env



def init_vector_db():
    db_url = get_database_url(use_pooling=True)
    vector_db_name = config("VECTOR_DB_NAME", cast=str)
    # print(f"Initializing vector database: {vector_db_name}")
    # print(f"Using database URL: {db_url}")
    vector_db_name = config("VECTOR_DB_TABLE_NAME", cast=str)
    # print(f"Using vector table name: {vector_db_name}")
    engine = create_engine(db_url, isolation_level="AUTOCOMMIT")
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1 FROM pg_database WHERE datname = :db_name"), {"db_name": vector_db_name})
        db_exists = result.scalar() == 1
        if not db_exists:
            connection.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
            connection.execute(text(f"CREATE DATABASE {vector_db_name}"))