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
    # TODO change openid_url to nullable=False
    openid_url = Column(URLType, unique=True, nullable=True)
    email = Column(EmailType, unique=True, nullable=False)    

    contact_id = Column(UUIDType(binary=False), ForeignKey("contacts.id"))
    contact = relationship("Contact")

    labs = association_proxy("user_lab_roles", "lab")
    workspaces = association_proxy("user_workspace_roles", "workspace")
    projects = association_proxy("user_project_roles", "project")

    def __init__(
            self, *, id: UUID = None, email: str, status: str = None,
            openid_url: str = None, contact_id: UUID = None, contact=None,
    ):
        self.user_profile = None

        self.id = id or uuid4()
        self.email = email        
        self.openid_url = openid_url

        if contact:
            self.contact = contact
        else:
            self.contact_id = contact_id

    def __repr__(self):
        return f'<User {self.email} ({self.id})>'
