from api.models import User
from api.schemas import UserSchema
from api.services.base_service import BaseService


class UserService(BaseService):
    model_schema = UserSchema
    model = User
