# pylint: disable=no-self-use,protected-access
from typing import List
from flask import request
from datetime import datetime
from flask_restplus import Resource
from werkzeug.datastructures import FileStorage

from api.models import Comment
from api.schemas import CommentSchema
from api.services import CommentService
from api.resources.api import api as comment_api
from api.services.meta_service import MetaService
from api.services.api_resource import ApiResource
from api.utilities.database import session_commit_context

meta = MetaService(CommentSchema)

resource = ApiResource(comment_api, meta)

@comment_api.route("/comments")
class CommentList(Resource):
    @resource.index
    def get(self) -> List[Comment]:
        return CommentService.fetch(request.args)

    @resource.post
    def post(self) -> Comment:
        with session_commit_context():
            return CommentService.create(comment_api.payload)


@comment_api.route("/comments/<id>")
class CommentItem(Resource):
    @resource.get
    def get(self, id) -> Comment:
        return CommentService.fetch_by_id(id)

    @resource.put
    def put(self, id) -> Comment:
        with session_commit_context():
            return CommentService.update(id, comment_api.payload)

    @resource.delete
    def delete(self, id):
        with session_commit_context():
            CommentService.delete(id)
