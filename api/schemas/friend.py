# pylint: disable=too-few-public-methods,no-self-use
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import ModelSchema
from marshmallow.fields import UUID, Email, Nested, Url, Dict, String

from api.models import User
from api.models.base_model import session

from api.schemas.base_schema import BaseSchema


class FriendSchema(ModelSchema, BaseSchema):
    user_id = UUID(required=True)
    friend_id = UUID(required=True)
    
    class Meta:
        model = Friend
        strict = True
        sqla_session = session
