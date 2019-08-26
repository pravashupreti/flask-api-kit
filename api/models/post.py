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

class Post(Base, BaseModel):
    __tablename__ = "posts"

    id = Column(UUIDType(binary=False), primary_key=True)
    post = Column(String,nullable=False)
    posted_by = Column(UUIDType(binary=False), ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")

    def __init__(
            self, *, id: UUID = None, post: str, posted_by: UUID
    ):
        self.id = id or uuid4()
        self.post = post
        self.posted_by = posted_by
        
    def __repr__(self):
        return f'<Post {self.post} ({self.id})>'
