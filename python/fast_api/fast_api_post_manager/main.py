# fast_api_post_manager/main.py

from fastapi import FastAPI

from database.init_db import initialize_database
from routers.token_router import token_router
from routers.user_router import user_router

initialize_database()

app = FastAPI()


app.include_router(
    router=user_router,
    prefix="/users",
)

app.include_router(
    router=token_router,
    prefix="/tokens",
)