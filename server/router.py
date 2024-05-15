from fastapi import APIRouter, Depends
from schemas import House, HouseSaved, Price, PriceSaved, Service, ServiceSaved, Filter, Url
from models import Houses, Prices, Services
from sqlalchemy.orm import Session
from dependencies import get_db
from itertools import groupby

router = APIRouter()



def avg(lst):
    return sum(lst) / len(lst)


@router.get("/houses_all")
async def houses_all(db: Session = Depends(get_db)):
    try:
        houses = db.query(Houses).all()
        return houses
    except Exception as e:
        return e


@router.post("/filter_houses")
async def filter_houses(request: Filter, db: Session = Depends(get_db)):
    services = db.query(Services).filter(Services.name.in_(request.services)).all()
    houses = db.query(Houses).filter(Houses.type.in_(request.types)).all()
    prices = db.query(Prices).filter(Prices.price.between(request.min_price, request.max_price)).all()
    try:    
        res = []
        for house, price in zip(houses, prices):
            services = db.query(Services).where(Services.house_id == house.id == price.house_id).all()
            print(request.services)
            check = 0
            for service in services:
                if service.name in request.services:
                    check += 1
            if len(request.services) == check:
                    res.append({
                        'id': house.id,
                        'type': house.type,
                        'price': price.price,
                        'lat': house.lat,
                        'lon': house.lon,
                        'address': house.address
                    })
        return res
    except Exception as e:
        return e

    

@router.post("/add_house", response_model=HouseSaved)
async def add_house(request: House, db: Session = Depends(get_db)):
    data = Houses(url=request.url, address=request.address, type=request.type,
                  lat=request.lat, lon=request.lon)
    try:
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        return e


@router.get("/prices_all")
async def prices_all(db: Session = Depends(get_db)):
    try:
        prices = db.query(Prices).all()
        return prices
    except Exception as e:
        return e


@router.post("/add_price", response_model=PriceSaved)
async def add_price(request: Price, db: Session = Depends(get_db)):
    data = Prices(house_id=request.house_id, price=request.price)
    try:
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        return e


@router.get("/services_all")
async def services_all(db: Session = Depends(get_db)):
    try:
        services = db.query(Services).all()
        return services
    except Exception as e:
        return e

@router.post("/filter_services")
async def filter_services(request: Filter, db: Session = Depends(get_db)):
    houses = db.query(Houses).filter(Houses.type.in_(request.types)).all()
    prices = db.query(Prices).filter(Prices.price.between(request.min_price, request.max_price)).all()
    try:   
        res = []
        for house, price in zip(houses, prices):
            services = db.query(Services).where(Services.house_id == house.id == price.house_id).all()
            print(request.services)
            check = 0
            for service in services:
                if service.name in request.services:
                    check += 1
            if len(request.services) == check:
                for service in services:    
                    res.append({
                            'id': service.id,
                            'house_id': house.id,
                            'service_type': service.service_type,
                            'name': service.name
                        })
        return res
    except Exception as e:
        return e
    
@router.post("/add_service", response_model=ServiceSaved)
async def add_service(request: Service, db: Session = Depends(get_db)):
    data = Services(house_id=request.house_id, service_type=request.service_type, name=request.name)
    try:
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        return e

@router.post('/duplicates')
async def duplicates(request: Url, db: Session = Depends(get_db)):
    data = db.query(Houses).filter(Houses.url == request.url).all()
    try:
        if len(data) == 0:
            return {'message': 'None'}
        else:
            return {'message': 'Exist'}
    except Exception as e:
        return {'message': e}


@router.post("/filter_mean_prices")
async def filter_mean_prices(request: Filter, db: Session = Depends(get_db)):
    services = db.query(Services).filter(Services.name.in_(request.services)).all()
    houses = db.query(Houses).filter(Houses.type.in_(request.types)).all()
    prices = db.query(Prices).filter(Prices.price.between(request.min_price, request.max_price)).all()
    try:
        res = []
        for house, price in zip(houses, prices):
            services = db.query(Services).where(house.id == Services.house_id == price.house_id).all()
            print(request.services)
            check = 0
            for service in services:
                if service.name in request.services:
                    check += 1
            if len(request.services) == check:
                    res.append({
                        'id': house.id,
                        'type': house.type,
                        'price': price.price
                    })

        result = {a: avg([z["price"] for z in b])
                for a, b in groupby(res, key=lambda x: x['type'])}
        return result
    except Exception as e:
        return e
