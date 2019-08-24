from api.models import Post
from api.schemas import PostSchema
from api.services.base_service import BaseService


class UserService(BaseService):
    model_schema = PostSchema
    model = Post
