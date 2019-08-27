# pylint: disable=no-self-use,protected-access
from typing import List
from flask import request
from datetime import datetime
from flask_restplus import Resource
from werkzeug.datastructures import FileStorage

from api.models import User
from api.schemas import UserSchema
from api.services import UserService
from api.resources.api import api as user_api
from api.services.meta_service import MetaService
from api.services.api_resource import ApiResource
from api.utilities.database import session_commit_context

meta = MetaService(UserSchema)

meta.index_parser.add_argument("email", type=str, help="User email")

resource = ApiResource(user_api, meta)

@user_api.route("/users")
class UserList(Resource):
    @resource.index
    def get(self) -> List[User]:
        return UserService.fetch(request.args)

    @resource.post
    def post(self) -> User:
        with session_commit_context():
            return UserService.create(user_api.payload)


@user_api.route("/users/<id>")
class UserItem(Resource):
    @resource.get
    def get(self, id) -> User:
        return UserService.fetch_by_id(id)

    @resource.put
    def put(self, id) -> User:
        with session_commit_context():
            return UserService.update(id, user_api.payload)

    @resource.delete
    def delete(self, id):
        with session_commit_context():
            UserService.delete(id)
