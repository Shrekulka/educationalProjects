# fast_api_blog/controllers/post_controller.py

import traceback
from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from database.session import get_session
from models.models import User
from schemas.posts import PostCreate, Post
from utils.auth import get_current_user
from utils.cache import clear_cache, set_in_cache, get_from_cache
from utils.logger_config import logger


def add_post_handler(request: PostCreate, session: Session = Depends(get_session),
                     current_user: User = Depends(get_current_user)) -> JSONResponse:
    """
        Creates a new post.

        Args:
            request (PostCreate): Data schema for creating a new post.
            session (Session, optional): Instance of the database session. Defaults to Depends(get_session).
            current_user (User): Current user.

        Returns:
            JSONResponse: Response in JSON format with a success status message and data of the new post.

        Raises:
            HTTPException: If there is an error performing database operations during post creation.
    """
    try:
        # Проверка размера полезной нагрузки
        if len(request.text) > 1024:  # Предполагаемый максимальный размер полезной нагрузки 1 МБ (1024 байт)
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Payload size exceeds 1MB")

        # Создание нового поста с учетом даты создания и обновления
        new_post = Post(text=request.text, status=request.status,
                        created_date=datetime.now(timezone.utc),
                        updated_date=datetime.now(timezone.utc),
                        owner=current_user)
        session.add(new_post)      # Добавление нового поста в базу данных
        session.commit()           # Сохранение изменений в базе данных
        # Обновление объекта new_post в базе данных для получения значений, сгенерированных базой данных, таких как id
        session.refresh(new_post)

        # Возвращение успешного ответа с кодом состояния HTTP 200 OK и данными нового поста
        return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "success", "data": new_post.dict()})
    # Обработка ошибок базы данных при создании поста
    except SQLAlchemyError as e:
        detailed_error_traceback = traceback.format_exc()
        logger.error(f"Database error occurred during post creation: {str(e)}\n{detailed_error_traceback}")
        # Если произошла ошибка базы данных, генерируется исключение HTTP 500 INTERNAL SERVER ERROR
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database error occurred during post creation")


def get_posts_handler(status_param: Optional[str] = None, session: Session = Depends(get_session),
                      current_user: User = Depends(get_current_user)) -> JSONResponse:
    """
        Retrieves a list of posts.

        Args:
            status_param (str, optional): Parameter for post status. Defaults to None.
            session (Session, optional): Instance of the database session. Defaults to Depends(get_session).
            current_user (User): Current user.

        Returns:
            JSONResponse: Response in JSON format with a success status message and data of the list of posts.

        Raises:
            HTTPException: If there is an error performing database operations during post retrieval.
    """
    try:
        # Проверка кэша для текущего пользователя
        cached_posts = get_from_cache(current_user.email)
        # Если посты найдены в кэше
        if cached_posts:
            # Возвращаем успешный ответ с кодом состояния HTTP 200 OK и данные о постах в формате JSON
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"status": "success", "data": [post.dict() for post in cached_posts]})

        # Если задан параметр статуса, фильтруем посты по статусу и идентификатору текущего пользователя
        if status_param:
            posts = session.query(Post).filter(and_(Post.user_id == current_user.id, Post.status == status_param)).all()
        else:
            # Иначе, получаем все посты пользователя без фильтрации по статусу
            posts = session.query(Post).filter(Post.user_id == current_user.id).all()

        # Преобразование списка типов Post в список экземпляров Post
        posts_instances = [post() for post in posts]

        # Сохранение постов в кэше
        set_in_cache(current_user.email, posts_instances)

        # Возвращение успешного ответа с кодом состояния HTTP 200 OK и данными о постах
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"status": "success", "data": [post.dict() for post in posts_instances]})
    # Обработка ошибок базы данных при получении постов
    except SQLAlchemyError as e:
        detailed_error_traceback = traceback.format_exc()
        logger.error(f"Database error occurred during fetching posts: {str(e)}\n{detailed_error_traceback}")
        # Бросается исключение HTTP 500 INTERNAL SERVER ERROR в случае ошибки базы данных
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database error occurred during fetching posts")


def delete_post_handler(post_id: int, session: Session = Depends(get_session),
                        current_user: User = Depends(get_current_user)) -> JSONResponse:
    """
        Deletes a post.

        Args:
            post_id (int): Identifier of the post.
            session (Session, optional): Instance of the database session. Defaults to Depends(get_session).
            current_user (User): Current user.

        Returns:
            JSONResponse: Response in JSON format with a success status message.

        Raises:
            HTTPException: If there is an error performing database operations during post deletion.
    """
    try:
        # Поиск поста по его идентификатору и идентификатору текущего пользователя
        post = session.query(Post).filter(and_(Post.id == post_id, Post.user_id == current_user.id)).first()
        # Если пост не найден, генерируем исключение HTTP 404 NOT FOUND
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        # Удаление объекта поста из сессии базы данных
        session.delete(post)
        # Применение всех изменений в базе данных
        session.commit()

        # Удаление кэша для текущего пользователя
        clear_cache(current_user.email)

        return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "success"})
    # Обработка ошибок базы данных при удалении поста
    except SQLAlchemyError as e:
        detailed_error_traceback = traceback.format_exc()
        logger.error(f"Database error occurred during post deletion: {str(e)}\n{detailed_error_traceback}")
        # Бросается исключение HTTP 500 INTERNAL SERVER ERROR в случае ошибки базы данных
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database error occurred during post deletion")
