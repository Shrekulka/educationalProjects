# fast_api_blog/schemas/posts.py

from datetime import datetime

from pydantic import BaseModel, Field


# Определение базовой схемы для поста
class PostBase(BaseModel):
    """
        Basic post schema.

        Attributes:
            text (str): The text of the post.
    """
    text: str               # Поле для текста поста


# Определение схемы для создания поста, наследует базовую схему
class PostCreate(BaseModel):
    """
        Schema for creating a post.

        Attributes:
        text (str): The text of the post. This is a required field containing the post text. The maximum length of the
                    text is limited to 1024 characters.
        status (str): The status of the post. This is an optional field that can take the values "draft" or "published".
                      The default value is set to "draft".
    """
    # Определение поля text с типом str для текста поста.
    # Используется Field из Pydantic для дополнительной конфигурации поля.
    # Аргумент ... указывает, что поле обязательно для заполнения.
    # max_length=1024 устанавливает максимальную длину текста поста до 1024 символов.
    # description содержит описание поля, которое будет отображаться в документации.
    text: str = Field(..., max_length=1024, description="The text of the post")

    # Определение поля status с типом str для статуса поста.
    # Используется Field из Pydantic для дополнительной конфигурации поля.
    # default="draft" устанавливает значение по умолчанию "draft" для статуса.
    # description содержит описание поля, которое будет отображаться в документации.
    # Статус может быть "draft" (черновик) или "published" (опубликован).
    status: str = Field(default="draft", description="The status of the post (draft or published)")


# Определение схемы для поста, наследует базовую схему
class Post(PostBase):
    """
        Post schema.

        Attributes:
            id (int): Unique identifier of the post.
            created_date (datetime): Date and time when the post was created.
            updated_date (datetime): Date and time of the last update to the post.
            status (str): Status of the post. Can take values "draft" or "published".

        Notes:
            - The created date (created_date) is set automatically when the post is created.
            - The updated date (updated_date) is automatically updated with each modification to the post.
            - The status of the post (status) can be "draft" or "published".
    """
    id: int                 # Поле для идентификатора поста
    created_date: datetime  # Поле для даты создания
    updated_date: datetime  # Поле для даты обновления
    status: str             # Поле для статуса поста

    # Внутренний класс для конфигурации модели
    class Config:
        """
            Model configuration.

            Attributes:
                orm_mode (bool): Indicates whether to use the ORM mode for SQLAlchemy model.
        """
        orm_mode = True     # Указание использовать режим ORM для модели SQLAlchemy
