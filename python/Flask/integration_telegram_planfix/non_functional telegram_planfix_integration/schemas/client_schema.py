# non_functional telegram_planfix_integration/schemas/client_schema.py

from marshmallow import Schema, fields, validate

from app.models.client import SessionStatusEnum
from app.utils import validate_channel, validate_email

print("client_schema.py")


class SessionSchema(Schema):
    session_id = fields.Int()
    name = fields.Str()
    path = fields.Str()


class ClientSchema(Schema):
    name = fields.Str(required=True)
    channel = fields.Str(required=True, validate=validate_channel)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    token = fields.Str()
    user_id = fields.Int()
    name_session = fields.Str()
    path_session = fields.Str()
    chat_id = fields.Str()
    message = fields.Str()
    title = fields.Str()
    contact_id = fields.Str()
    contact_name = fields.Str()
    contact_last_name = fields.Str()
    contact_ico = fields.Str()
    contact_email = fields.Str(validate=validate_email)
    contact_data = fields.Str()
    attachments_name = fields.Str()
    attachments_url = fields.Str()
    user_email = fields.Str(validate=validate_email)
    telegram_user_name = fields.Str()
    telegram_user_id = fields.Str()
    token_planfix = fields.Str()
    url_planfix = fields.Str()
    current_session = fields.Nested(SessionSchema(), exclude=('client',))
    sessions = fields.Nested(SessionSchema(), many=True, exclude=('client',))

    # Валидация статуса сессии
    status = fields.Str(validate=validate.OneOf([status.value for status in SessionStatusEnum]))
