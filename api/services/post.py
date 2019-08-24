from api.models import Post
from api.schemas import PostSchema
from api.services.base_service import BaseService


class PostService(BaseService):
    model_schema = PostSchema
    model = Post
