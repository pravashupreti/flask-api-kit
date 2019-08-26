# pylint: disable=too-few-public-methods,no-self-use
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import ModelSchema
from marshmallow.fields import UUID, Email, Nested, Url, Dict, String

from api.models import Post
from api.models.base_model import session

from api.schemas.base_schema import BaseSchema


class PostSchema(ModelSchema, BaseSchema):
    id = UUID(required=False)
    post = String(required=True)
    posted_by = UUID(required=True)
    user = Nested("UserSchema", many=False)

    class Meta:
        model = Post
        strict = True
        sqla_session = session
