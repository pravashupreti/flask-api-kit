# pylint: disable=no-self-use,protected-access
from typing import List
from flask import request
from datetime import datetime
from flask_restplus import Resource
from werkzeug.datastructures import FileStorage

from api.models import Like
from api.schemas import LikeSchema
from api.services import LikeService
from api.resources.api import api as like_api
from api.services.meta_service import MetaService
from api.services.api_resource import ApiResource
from api.utilities.database import session_commit_context

meta = MetaService(LikeSchema)

resource = ApiResource(like_api, meta)

@like_api.route("/likes")
class LikeList(Resource):
    @resource.index
    def get(self) -> List[Like]:
        return LikeService.fetch(request.args)

    @resource.post
    def post(self) -> Like:
        with session_commit_context():
            return LikeService.create(like_api.payload)


@like_api.route("/likes/<id>")
class Like(Resource):
    @resource.get
    def get(self, id) -> Like:
        return LikeService.fetch_by_id(id)

    @resource.put
    def put(self, id) -> Like:
        with session_commit_context():
            return LikeService.update(id, like_api.payload)

    @resource.delete
    def delete(self, id):
        with session_commit_context():
            LikeService.delete(id)
