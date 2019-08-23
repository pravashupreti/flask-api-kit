# pylint: disable=too-few-public-methods,no-self-use
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import ModelSchema
from marshmallow.fields import UUID, Email, Nested, Url, Dict

from api.models import User
from api.models.base_model import session

from api.schemas.base_schema import BaseSchema


class UserSchema(ModelSchema, BaseSchema):
    id = UUID(required=False)
    email = Email(required=True)
    openid_url = Url(required=False, dump_only=True)
    user_profile = Dict()

    contact = Nested("ContactSchema", many=False, exclude=("user",))
    field_events = Nested("FieldEventSchema", many=True, exclude=("assignees",))
    workspaces = Nested("WorkspaceSchema", many=True, exclude=("users",))
    projects = Nested("ProjectSchema", many=True, exclude=("users",))
    labs = Nested("LabSchema", many=True, exclude=("users",))
    collected_samples = Nested("SampleSchema", many=True)
    user_project_roles = Nested("UserProjectRoleSchema", many=True, exclude=("user",))
    user_workspace_roles = Nested("UserWorkspaceRoleSchema", many=True, exclude=("user",))
    user_lab_roles = Nested("UserLabRoleSchema", many=True, exclude=("user",))
    user_registration_devices = Nested("UserRegistrationDeviceSchema", many=True, exclude=("user",))

    class Meta:
        model = User
        strict = True
        sqla_session = session

        selects = User.column_names() + ["user_profile"]
        joins = User.relation_names() + [
            "labs",
            "workspaces",
            "projects"
        ]
