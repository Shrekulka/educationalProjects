# fast_api_blog/schemas/auth.py

from pydantic import BaseModel, EmailStr
from pydantic.v1 import validator


class BaseUserSchema(BaseModel):
    """
       Base schema for user-related data validation.

       This schema provides validators for common user-related fields such as password and email.

       Attributes:
           validate_password_length (validator): Validator to check password length.
           validate_email (validator): Validator to check email correctness.
    """

    @validator('password')
    def validate_password_length(self, password: str) -> str:
        """
            Validator to check password length.

            Args:
                password (str): User's password.

            Returns:
                str: The entered password if it meets the conditions.

            Raises:
                ValueError: If the password is less than 8 characters.
        """
        # Если длина пароля меньше 8 символов, генерируется исключение ValueError с сообщением об ошибке.
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        # Возвращаем введенный пароль, если он соответствует требованиям.
        return password

    @validator('email')
    def validate_email(self, email: str) -> str:
        """
            Validator to check email correctness.

            Args:
                email (str): Email address.

            Returns:
                str: The entered email address if it is correct.

            Raises:
                ValueError: If the email address is incorrect.
        """
        # Проверяем, оканчивается ли адрес электронной почты на допустимый домен.
        # Если нет, генерируем исключение ValueError с сообщением об ошибке.
        if not email.endswith('@example.com'):
            raise ValueError('Invalid email address. Only example.com is allowed.')
        # Возвращаем введенный email, если он соответствует требованиям.
        return email


class UserCreate(BaseUserSchema):
    """
        Schema for creating a new user.

        Attributes:
            email (EmailStr): User's email.
            password (str): User's password.
    """
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """
        Schema for login request.

        Attributes:
            email (EmailStr): User's email.
            password (str): User's password.
    """
    email: EmailStr
    password: str


class RequestDetails(BaseModel):
    """
        Schema for request details.

        Attributes:
            email (EmailStr): User's email.
            password (str): User's password.
    """
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    """
        Schema for token.

        Attributes:
            access_token (str): Access token.
            refresh_token (str): Refresh token.
    """
    access_token: str
    refresh_token: str


class ChangePassword(BaseModel):
    """
        Schema for password change.

        Attributes:
            email (EmailStr): User's email.
            old_password (str): User's old password.
            new_password (str): User's new password.
    """
    email: EmailStr
    old_password: str
    new_password: str
