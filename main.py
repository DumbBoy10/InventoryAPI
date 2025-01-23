from fastapi import FastAPI

from Endpoints.Auth import APIRouter as auth
from Endpoints.Category import APIRouter as category
from Endpoints.Log import APIRouter as log
from Endpoints.Item import APIRouter as item


app = FastAPI()


app.include_router(auth, prefix="/auth", tags=["Auth"])
app.include_router(category, prefix="/category", tags=["Category"])
app.include_router(log, prefix="/log", tags=["Log"])
app.include_router(item, prefix="/items", tags=["Items"])


@app.get("/")
async def root():
    return {"message": "Try /auth/login  Username: Demo  Password: Demo123"}