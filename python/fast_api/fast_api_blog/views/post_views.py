# fast_api_blog/views/post_views.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from controllers.post_controller import add_post_handler, get_posts_handler, delete_post_handler
from database.session import get_session
from schemas.posts import PostCreate
from utils.auth import get_current_user

# Создаем экземпляр маршрутизатора API для постов.
posts_router = APIRouter()


@posts_router.post("/addPost")
def add_post(request: PostCreate, current_user=Depends(get_current_user), session: Session = Depends(get_session)) \
        -> JSONResponse:
    """
        Endpoint for adding a new post.

        Args:
            request (PostCreate): Data schema for creating a new post, containing post text and status.
            current_user: Current user authenticated.
            session (Session, optional): Instance of the database session. Defaults to Depends(get_session).

        Returns:
            JSONResponse: Response in JSON format containing success status and added post data.

        Raises:
            HTTPException: If there is an error performing database operations during post creation.
    """
    # Вызываем функцию обработчика добавления поста, передавая ей запрос на создание поста (request),
    # текущего пользователя (current_user) и сессию базы данных (session) в качестве аргументов.
    return add_post_handler(request=request, session=session, current_user=current_user)


@posts_router.get("/getPosts")
def get_posts(status_param: str = None, current_user=Depends(get_current_user),
              session: Session = Depends(get_session)) -> JSONResponse:
    """
        Endpoint for retrieving posts.

        Args:
            status_param (str, optional): Filter posts by status. Defaults to None.
            current_user: Current user authenticated.
            session (Session, optional): Instance of the database session. Defaults to Depends(get_session).

        Returns:
            JSONResponse: Response in JSON format containing success status and retrieved posts.

        Raises:
            HTTPException: If there is an error performing database operations during fetching posts.
    """
    # Вызываем функцию обработчика получения постов, передавая ей параметры запроса, текущего пользователя
    # и сессию базы данных в качестве аргументов.
    return get_posts_handler(status_param=status_param, current_user=current_user, session=session)


@posts_router.delete("/deletePost/{post_id}")
def delete_post(post_id: int, current_user=Depends(get_current_user), session: Session = Depends(get_session)) \
        -> JSONResponse:
    """
        Endpoint for deleting a post.

        Args:
            post_id (int): ID of the post to delete.
            current_user: Current user authenticated.
            session (Session, optional): Instance of the database session. Defaults to Depends(get_session).

        Returns:
            JSONResponse: Response in JSON format containing success status.

        Raises:
            HTTPException: If there is an error performing database operations during post deletion.
    """
    # Вызываем функцию обработчика удаления поста, передавая ей ID удаляемого поста, текущего пользователя
    # и сессию базы данных в качестве аргументов.
    return delete_post_handler(post_id=post_id, current_user=current_user, session=session)
