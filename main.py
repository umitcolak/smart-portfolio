from fastapi import FastAPI
from backend import auth

app = FastAPI()

app.include_router(auth.router)
