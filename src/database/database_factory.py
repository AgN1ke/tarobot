from .sqlite_database import SQLiteDatabase
from .postgresql_database import PostgreSQLDatabase


def get_database(db_type="sqlite", **kwargs):
    if db_type == "sqlite":
        return SQLiteDatabase(**kwargs)
    elif db_type == "postgres":
        return PostgreSQLDatabase(**kwargs)
    else:
        raise ValueError("Unsupported database type")
