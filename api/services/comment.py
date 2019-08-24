from api.models import comment
from api.schemas import CommentSchema
from api.services.base_service import BaseService


class UserService(BaseService):
    model_schema = CommentSchema
    model = comment
