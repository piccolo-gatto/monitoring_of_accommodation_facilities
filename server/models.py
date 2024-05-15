from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.schema import ForeignKey
from database import Base


class Houses(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    address = Column(String)
    type = Column(String)
    lat = Column(Float)
    lon = Column(Float)


class Services(Base):
    __tablename__ = "service"

    id = Column(Integer, primary_key=True, index=True)
    house_id = Column(Integer, ForeignKey("houses.id"))
    service_type = Column(String)
    name = Column(String)


class Prices(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True, index=True)
    house_id = Column(Integer, ForeignKey("houses.id"))
    price = Column(Integer)
