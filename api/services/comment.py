from api.models import Comment
from api.schemas import CommentSchema
from api.services.base_service import BaseService


class CommentService(BaseService):
    model_schema = CommentSchema
    model = Comment
