from fastapi import APIRouter, FastAPI
from app.database import get_database
from app.routers import products, inventory

database = get_database()
router = APIRouter()
app = FastAPI()
app.include_router(products.router)
app.include_router(inventory.router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}
