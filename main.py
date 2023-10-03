from fastapi import FastAPI
from routes import home

app = FastAPI()

app.include_router(home.home_route)