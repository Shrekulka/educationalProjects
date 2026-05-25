# fast_api_post_manager/schemas/post_schema.py

from pydantic import BaseModel, validator, Field, field_validator
import uuid
from datetime import datetime
from typing import Optional

from pydantic_core.core_schema import ValidationInfo

from utils.validation import validate_text, validate_status


class PostBase(BaseModel):
    """
    Base post schema with common fields.

    Attributes:
        text (str): The content of the post, limited to 1MB.
        title (str, optional): Optional title for the post.
        status (str, optional): Status of the post (draft or published).
    """
    text: str = Field(...,
                      description="Post content text, limited to 1MB",
                      min_length=1,
                      max_length=1048576)
    title: Optional[str] = Field(None, max_length=100, description="Optional post title")
    status: Optional[str] = Field("draft", description="Post status (draft or published)")

    @field_validator('text')
    @classmethod
    def validate_text_size(cls, value: str, info: ValidationInfo) -> str:
        return validate_text(value)

    @field_validator('status')
    @classmethod
    def validate_status(cls, status, info: ValidationInfo) -> str:
        return validate_status(status)


class PostCreate(PostBase):
    """
    Schema for creating a new post.

    Extends PostBase with any additional fields needed for post creation.
    """
    pass


class PostUpdate(PostBase):
    """
    Schema for updating an existing post.

    All fields are optional to allow partial updates.
    """
    text: Optional[str] = None
    title: Optional[str] = None
    status: Optional[str] = None


class PostInDB(PostBase):
    """
    Schema for a post as stored in the database.

    Attributes:
        id (UUID): The unique identifier for the post.
        user_id (UUID): The identifier of the post's owner.
        created_date (datetime): The date and time when the post was created.
        updated_date (datetime, optional): The date and time when the post was last updated.
    """
    id: uuid.UUID
    user_id: uuid.UUID
    created_date: datetime
    updated_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class PostResponse(PostInDB):
    """
    Schema for API responses containing post data.

    Inherits all fields from PostInDB.
    """
    pass


class PostDelete(BaseModel):
    """
    Schema for post deletion requests.

    Attributes:
        post_id (UUID): The unique identifier of the post to delete.
    """
    post_id: uuid.UUID