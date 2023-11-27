from .sqlalchemy_database import SQLAlchemyPostgresDatabase


def get_database(db_type="sqlalchemy_postgres", **kwargs):
    if db_type == "sqlalchemy_postgres":
        return SQLAlchemyPostgresDatabase(**kwargs)
    else:
        raise ValueError("Unsupported database type")