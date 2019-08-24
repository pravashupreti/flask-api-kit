# pylint: disable=too-few-public-methods,no-self-use
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import ModelSchema
from marshmallow.fields import UUID, Email, Nested, Url, Dict, String

from api.models import FriendList
from api.models.base_model import session

from api.schemas.base_schema import BaseSchema


class FriendListSchema(ModelSchema, BaseSchema):
    id = UUID(required=False)
    user_id = UUID(required=True)
    friend_id = UUID(required=True)
    
    class Meta:
        model = FriendList
        strict = True
        sqla_session = session
