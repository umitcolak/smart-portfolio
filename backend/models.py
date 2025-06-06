from sqlalchemy import Column, Integer, String
from .db import Base

class User(Base):
    __tablename__ = "Users"  # This is the name of the DB table

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

