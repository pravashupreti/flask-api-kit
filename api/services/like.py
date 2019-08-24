from api.models import Like
from api.schemas import LikeSchema
from api.services.base_service import BaseService


class UserService(BaseService):
    model_schema = LikeSchema
    model = Like
