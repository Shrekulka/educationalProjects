# fast_api_post_manager/routers/token_router.py

from fastapi import APIRouter, Depends
from sqlmodel import Session

from controllers.token_controller import verify_user_and_generate_token
from database.database import get_db
from schemas.token_schema import TokenResponse
from schemas.user_schema import UserLogin



token_router = APIRouter()

@token_router.post("", response_model=TokenResponse, status_code=201)
def generate_access_token(user_data: UserLogin, db: Session = Depends(get_db)):
    return verify_user_and_generate_token(db=db, user_data=user_data)
