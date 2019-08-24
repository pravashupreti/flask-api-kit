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

class Comment(Base, BaseModel):
    __tablename__ = "comments"

    id = Column(UUIDType(binary=False), primary_key=True)
    comment = Column(String,nullable=False)

    post_id = Column(UUIDType(binary=False,nullable=True), ForeignKey("posts.id"))
    comment_id = Column(UUIDType(binary=False,nullable=True), ForeignKey("comments.id"))
    commented_by = Column(UUIDType(binary=False,nullable=False), ForeignKey("users.id"))

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
