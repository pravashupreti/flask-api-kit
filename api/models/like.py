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

class Like(Base, BaseModel):
    __tablename__ = "likes"
    __table_args__ = {'extend_existing': True} 

    id = Column(UUIDType(binary=False), primary_key=True)
    post_id = Column(UUIDType(binary=False), ForeignKey("posts.id"),  nullable=True)
    comment_id = Column(UUIDType(binary=False), ForeignKey("comments.id"), nullable=True)
    liked_by = Column(UUIDType(binary=False), ForeignKey("users.id"), nullable=False)
    
    def __init__(
            self, *, id: UUID = None, post_id: UUID, comment_id: UUID, liked_by: UUID
    ):        
        self.id = id or uuid4()
        self.post_id = post_id
        self.comment_id = comment_id
        self.liked_by = liked_by
        
    def __repr__(self):
        return f'<Like {self.liked_by})>'
