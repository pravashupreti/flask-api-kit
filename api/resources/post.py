# pylint: disable=no-self-use,protected-access
from typing import List
from flask import request
from datetime import datetime
from flask_restplus import Resource
from werkzeug.datastructures import FileStorage

from api.models import Post
from api.schemas import PostSchema
from api.services import PostService
from api.resources.api import api as post_api
from api.services.meta_service import MetaService
from api.services.api_resource import ApiResource
from api.utilities.database import session_commit_context

meta = MetaService(PostSchema)

resource = ApiResource(post_api, meta)

@post_api.route("/posts")
class PostList(Resource):
    @resource.index
    def get(self) -> List[Post]:
        return PostService.fetch(request.args)

    @resource.post
    def post(self) -> Post:
        with session_commit_context():
            return PostService.create(post_api.payload)


@post_api.route("/posts/<id>")
class PostItem(Resource):
    @resource.get
    def get(self, id) -> Post:
        return PostService.fetch_by_id(id)

    @resource.put
    def put(self, id) -> Post:
        with session_commit_context():
            return PostService.update(id, post_api.payload)

    @resource.delete
    def delete(self, id):
        with session_commit_context():
            PostService.delete(id)
