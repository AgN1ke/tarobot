# user.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id: int = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    telegram_id: str = Column(String)
    name: str = Column(String)
    age: int = Column(Integer)
    gender: str = Column(String)
