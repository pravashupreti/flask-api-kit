# pylint: disable=too-few-public-methods,redefined-builtin
from enum import Enum
from uuid import uuid4, UUID

from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy_utils import UUIDType, EmailType, URLType, ChoiceType, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property

from api.models.meta import Base
from api.models.base_model import BaseModel

class Friend(Base, BaseModel):
    __tablename__ = "friends"

    user_id = Column(UUIDType(binary=False,nullable=False), ForeignKey("users.id"))
    friend_id = Column(UUIDType(binary=False,nullable=False), ForeignKey("users.id"))

    def __init__(
            self, *, user_id: UUID, friend_id: UUID
    ):
        self.user_id = user_id
        self.friend_id = friend_id
        
    def __repr__(self):
        return f'<Friend {self.user_id}>'
