# pylint: disable=no-self-use,protected-access
from typing import List
from flask import request
from datetime import datetime
from flask_restplus import Resource

from api.models import FriendList
from api.schemas import FriendListSchema
from api.services import FriendListService
from api.resources.api import api as friend_list_api
from api.services.meta_service import MetaService
from api.services.api_resource import ApiResource
from api.utilities.database import session_commit_context

meta = MetaService(FriendListSchema)

resource = ApiResource(friend_list_api, meta)

@friend_list_api.route("/friend_list")
class FriendList(Resource):
    @resource.index
    def get(self) -> List[FriendList]:
        return FriendListService.fetch(request.args)

    @resource.post
    def post(self) -> FriendList:
        with session_commit_context():
            return FriendListService.create(friend_list_api.payload)


@friend_list_api.route("/friend_list/<id>")
class Friend(Resource):
    @resource.get
    def get(self, id) -> FriendList:
        return FriendListService.fetch_by_id(id)

    @resource.put
    def put(self, id) -> FriendList:
        with session_commit_context():
            return FriendListService.update(id, friend_list_api.payload)

    @resource.delete
    def delete(self, id):
        with session_commit_context():
            FriendListService.delete(id)
