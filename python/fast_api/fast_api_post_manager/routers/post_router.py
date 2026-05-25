# fast_api_post_manager/routers/post_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated
import uuid

from database.database import get_db
from models.models import User, Post
from schemas.post_schema import PostCreate, PostResponse, PostDelete
from utils.cache_utils import get_cache, set_cache, get_cache_key
from utils.token_utils import verify_token

post_router = APIRouter()


@post_router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def add_post(
        post_data: PostCreate,
        current_user: Annotated[User, Depends(verify_token)],
        db: Session = Depends(get_db)
):
    """
    Создание нового поста.

    Args:
        post_data: Данные для создания поста
        current_user: Текущий пользователь (из проверки токена)
        db: Сессия БД

    Returns:
        PostResponse: Созданный пост
    """
    # Создаем новый пост
    new_post = Post(
        title=post_data.title,
        text=post_data.text,
        status=post_data.status,
        user_id=current_user.id
    )

    # Сохраняем в БД
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # Инвалидируем кэш для этого пользователя
    invalidate_user_posts_cache(str(current_user.id))

    return new_post


@post_router.get("/", response_model=List[PostResponse])
def get_posts(
        current_user: Annotated[User, Depends(verify_token)],
        db: Session = Depends(get_db)
):
    """
    Получение всех постов текущего пользователя.

    Args:
        current_user: Текущий пользователь (из проверки токена)
        db: Сессия БД

    Returns:
        List[PostResponse]: Список постов пользователя
    """
    # Ключ кэша для постов пользователя
    cache_key = get_cache_key(str(current_user.id), "get_posts")

    # Пробуем получить из кэша
    cached_posts = get_cache(cache_key)
    if cached_posts is not None:
        return cached_posts

    # Если в кэше нет - получаем из БД
    posts = db.query(Post).filter(Post.user_id == current_user.id).all()

    # Сохраняем в кэш на 5 минут
    set_cache(cache_key, posts, minutes=5)

    return posts


@post_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        post_id: uuid.UUID,
        current_user: Annotated[User, Depends(verify_token)],
        db: Session = Depends(get_db)
):
    """
    Удаление поста по ID.

    Args:
        post_id: ID поста для удаления
        current_user: Текущий пользователь (из проверки токена)
        db: Сессия БД
    """
    # Находим пост
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == current_user.id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # Удаляем пост
    db.delete(post)
    db.commit()

    # Инвалидируем кэш для этого пользователя
    invalidate_user_posts_cache(str(current_user.id))

    return None

def invalidate_user_posts_cache(user_id: str) -> None:
    """
    Инвалидирует кэш постов пользователя.

    Args:
        user_id: ID пользователя
    """
    from utils.cache_utils import invalidate_cache
    invalidate_cache(user_id)