# pylint: disable=too-few-public-methods,no-self-use
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import ModelSchema
from marshmallow.fields import UUID, Email, Nested, Url, Dict, String

from api.models import Like
from api.models.base_model import session

from api.schemas.base_schema import BaseSchema


class LikeSchema(ModelSchema, BaseSchema):
    extend_existing=True
    post_id = UUID(required=False)
    comment_id = UUID(required=False)
    liked_by = UUID(required=True)
    
    class Meta:
        model = Like
        strict = True
        sqla_session = session
