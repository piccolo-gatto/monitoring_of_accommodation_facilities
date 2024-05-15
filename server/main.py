import uvicorn
from fastapi import FastAPI
from database import engine, Base
from router import router as houses_router
server = FastAPI()

Base.metadata.create_all(bind=engine)
server.include_router(houses_router)
if __name__ == "__main__":
    uvicorn.run(server, host='0.0.0.0', port=8000)

