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

class Like(Base, BaseModel):
    __tablename__ = "likes"

    post_id = Column(UUIDType(binary=False,nullable=True), ForeignKey("posts.id"))
    comment_id = Column(UUIDType(binary=False,nullable=True), ForeignKey("comments.id"))
    liked_by = Column(UUIDType(binary=False,nullable=False), ForeignKey("users.id"))
    
    def __init__(
            self, *, post_id: UUID, comment_id: UUID, liked_by: UUID
    ):        
        self.post_id = post_id
        self.comment_id = comment_id
        self.liked_by = liked_by
        
    def __repr__(self):
        return f'<Like {self.liked_by})>'
