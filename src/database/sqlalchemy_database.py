# sqlalchemy_postgres_database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from .database_interface import DatabaseInterface
from src.database.user import User, Base


class SQLAlchemyPostgresDatabase(DatabaseInterface):
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def add_user(self, user: User):
        session = self.Session()
        try:
            session.add(user)
            session.commit()
            return user.user_id  # Assuming user_id is eagerly loaded
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_user(self, user: User):
        session = self.Session()
        try:
            session.query(User).filter(User.user_id == user.user_id).update({
                User.telegram_id: user.telegram_id,
                User.name: user.name,
                User.age: user.age,
                User.gender: user.gender
            })
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def user_exists(self, user_id: int):
        session = self.Session()
        try:
            return session.query(User).filter(User.user_id == user_id).scalar() is not None
        except Exception as e:
            raise e
        finally:
            session.close()

    def get_user(self, user_id: int):
        session = self.Session()
        try:
            user = session.query(User).filter(User.user_id == user_id).one()
            return user  # Make sure user object has all needed data loaded
        except NoResultFound:
            return None
        except Exception as e:
            raise e
        finally:
            session.close()
