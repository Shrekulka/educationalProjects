# fast_api_post_manager/controllers/post_controller.py


import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from models.models import Post, User
from schemas.post_schema import PostCreate
from utils.cache_utils import get_cache, set_cache, get_cache_key, invalidate_cache


def create_post(db: Session, post_data: PostCreate, user_id: uuid.UUID) -> Post:
    """
    Создает новый пост для пользователя.

    Args:
        db: Сессия базы данных
        post_data: Данные поста
        user_id: ID пользователя-автора

    Returns:
        Post: Созданный пост
    """
    # Создаем пост
    post = Post(
        title=post_data.title,
        text=post_data.text,
        status=post_data.status,
        user_id=user_id
    )

    # Сохраняем в БД
    db.add(post)
    db.commit()
    db.refresh(post)

    # Инвалидируем кэш постов пользователя
    invalidate_cache(str(user_id))

    return post


def get_user_posts(db: Session, user_id: uuid.UUID) -> list[Post]:
    """
    Получает все посты пользователя с возможным кэшированием.

    Args:
        db: Сессия базы данных
        user_id: ID пользователя

    Returns:
        list[Post]: Список постов пользователя
    """
    # Проверяем кэш
    cache_key = get_cache_key(str(user_id), "user_posts")
    cached_posts = get_cache(cache_key)

    if cached_posts is not None:
        return cached_posts

    # Если нет в кэше, получаем из БД
    posts = db.query(Post).filter(Post.user_id == user_id).all()

    # Кэшируем результат
    set_cache(cache_key, posts, minutes=5)

    return posts


def delete_user_post(db: Session, post_id: uuid.UUID, user_id: uuid.UUID) -> None:
    """
    Удаляет пост пользователя.

    Args:
        db: Сессия базы данных
        post_id: ID поста для удаления
        user_id: ID пользователя-владельца

    Raises:
        HTTPException: Если пост не найден
    """
    # Находим пост
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()

    if not post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Post not found")

    # Удаляем пост
    db.delete(post)
    db.commit()

    # Инвалидируем кэш
    invalidate_cache(str(user_id))