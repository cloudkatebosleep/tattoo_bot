from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime,BigInteger
Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    name = Column(String)
    tattoo_date = Column(DateTime)
    tattoo_size = Column(String)

class AvailableDate(Base):
    __tablename__ = "available_dates"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, unique=True)
