from api.models import FriendList
from api.schemas import FriendListSchema
from api.services.base_service import BaseService



class FriendListService(BaseService):
    model_schema = FriendListSchema
    model = FriendList
