# pylint: disable=too-few-public-methods,no-self-use
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import ModelSchema
from marshmallow.fields import UUID, Email, Nested, Url, Dict, String

from api.models import Comment
from api.models.base_model import session

from api.schemas.base_schema import BaseSchema


class CommentSchema(ModelSchema, BaseSchema):
    id = UUID(required=False)
    comment = String(required=True)
    post_id = UUID(required=False)
    comment_id = UUID(required=False)
    commented_by = UUID(required=True)

    class Meta:
        model = Comment
        strict = True
        sqla_session = session
