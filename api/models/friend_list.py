# pylint: disable=too-few-public-methods,redefined-builtin
from enum import Enum
from uuid import uuid4, UUID

from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy_utils import UUIDType
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property

from api.models.meta import Base
from api.models.base_model import BaseModel

class FriendList(Base, BaseModel):
    __tablename__ = "friend_list"
    
    id = Column(UUIDType(binary=False), primary_key=True)
    user_id = Column(UUIDType(binary=False), ForeignKey("users.id"), nullable=False)
    friend_id = Column(UUIDType(binary=False), ForeignKey("users.id"), nullable=False)

    def __init__(
            self, *, id: UUID = None, user_id: UUID, friend_id: UUID
    ):
        self.id = id or uuid4()
        self.user_id = user_id
        self.friend_id = friend_id
        
    def __repr__(self):
        return f'<Friend {self.user_id}>'
