from api.models import Like
from api.schemas import LikeSchema
from api.services.base_service import BaseService


class LikeService(BaseService):
    model_schema = LikeSchema
    model = Like
