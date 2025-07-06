from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Date

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    name = Column(String)
    tattoo_date = Column(Date)
    tattoo_size = Column(String)

class AvailableDate(Base):
    __tablename__ = "available_dates"

    id = Column(Integer, primary_key=True)
    date = Column(Date, unique=True)
