# pylint: disable=too-few-public-methods,redefined-builtin
from enum import Enum
from uuid import uuid4, UUID

from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy_utils import UUIDType, EmailType, URLType, ChoiceType
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property

from api.models.meta import Base
from api.models.base_model import BaseModel

class User(Base, BaseModel):
    __tablename__ = "users"

    id = Column(UUIDType(binary=False), primary_key=True)
    email = Column(EmailType, unique=True, nullable=False)    

    def __init__(
            self, *, id: UUID = None, email: str
    ):
        self.id = id or uuid4()
        self.email = email        
        
    def __repr__(self):
        return f'<User {self.email} ({self.id})>'
