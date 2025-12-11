from sqlalchemy import Column, Integer, String, Date
from database import Base
from datetime import date

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String, index=True)
    department = Column(String, index=True)
    date_joined = Column(Date, default=date.today())