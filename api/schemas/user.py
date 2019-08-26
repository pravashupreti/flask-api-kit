# pylint: disable=too-few-public-methods,no-self-use
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import ModelSchema
from marshmallow.fields import UUID, Email, Nested, Url, Dict, String

from api.models import User
from api.models.base_model import session

from api.schemas.base_schema import BaseSchema


class UserSchema(ModelSchema, BaseSchema):
    id = UUID(required=False)
    email = Email(required=True)
    username = String(required=True)
    posts = Nested("PostSchema", many=True)
    comments = Nested("CommentSchema", many=True)

    class Meta:
        model = User
        strict = True
        sqla_session = session
