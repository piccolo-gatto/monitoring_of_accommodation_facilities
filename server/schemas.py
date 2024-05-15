from pydantic import BaseModel


class House(BaseModel):
    url: str
    type: str
    address: str
    lat: float
    lon: float


class HouseSaved(House):
    id: int

    class Config:
        orm_mode = True


class Service(BaseModel):
    house_id: int
    service_type: str
    name: str


class ServiceSaved(House):
    id: int

    class Config:
        orm_mode = True


class Price(BaseModel):
    house_id: int
    price: int


class PriceSaved(House):
    id: int

    class Config:
        orm_mode = True


class Filter(BaseModel):
    types: list
    services: list
    min_price: int
    max_price: int


class Url(BaseModel):
    url: str
