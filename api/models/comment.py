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

class Comment(Base, BaseModel):
    __tablename__ = "comments"

    id = Column(UUIDType(binary=False), primary_key=True)
    comment = Column(String,nullable=False)

    post_id = Column(UUIDType(binary=False), ForeignKey("posts.id"), nullable=True,)
    comment_id = Column(UUIDType(binary=False), ForeignKey("comments.id"), nullable=True)
    commented_by = Column(UUIDType(binary=False), ForeignKey("users.id"), nullable=False)

    def __init__(
            self, *, id: UUID = None, comment: str, post_id: UUID, comment_id: UUID, commented_by: UUID
    ):
        self.id = id or uuid4()
        self.comment = comment
        self.post_id = post_id
        self.comment_id = comment_id
        self.commented_by = commented_by
        
    def __repr__(self):
        return f'<Comment {self.comment} ({self.id})>'
