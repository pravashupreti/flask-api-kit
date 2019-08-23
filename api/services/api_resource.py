from typing import Callable, Union, Mapping
from http import HTTPStatus

from flask_restplus import fields
from flask_restplus import Api as BaseApi
from flask_restplus.namespace import Namespace

# from api import di
from api.services.meta_service import MetaService
from api.decorators.marshmallow_with import marshmallow_with

from config import Config

Api = Union[BaseApi, Namespace]
# auth = di.auth()


def _combine(n: Callable, *ns: Callable) -> callable:
    if not ns:
        return n
    return n(_combine(*ns))


class ApiResource:
    # TODO remove Config.AUTH_REQUIRED once it is fully implemented in the UI
    def __init__(self, api: Api, meta: MetaService, require_auth=Config.AUTH_REQUIRED):
        self.api = api
        self.meta = meta
        self.model = api.add_model(meta.api_model.name, meta.api_model)
        self.require_auth = require_auth

    # @property
    # def _auth(self) -> Callable:
    #     if not self.require_auth:
    #         return lambda x: x
    #     return auth.required

    @property
    def _doc_kvargs(self) -> Mapping:
        if not self.require_auth:
            return {}
        return {"security": 'apiKey'}

    def index(self, function: Callable) -> Callable:
        return _combine(
            self._auth,
            self.api.expect(self.meta.index_parser),
            self.api.doc(model=[self.model], **self._doc_kvargs),
            marshmallow_with(
                self.meta.schema_class,
                many=True,
                strict=True,
                request_parser=self.meta.index_parser),
            function)

    def post(self, function: Callable) -> Callable:
        # validate_schema(self.meta.api_model)
        response_status = HTTPStatus.CREATED
        return _combine(
            self._auth,
            self.api.expect(self.model),
            self.api.doc(**self._doc_kvargs),
            self.api.response(response_status, response_status.phrase, model=self.model),
            marshmallow_with(
                self.meta.schema_class,
                many=False,
                strict=True,
                request_parser=self.meta.view_parser,
                response_status=response_status),
            function)

    def get(self, function: Callable) -> Callable:
        return _combine(
            self._auth,
            self.api.expect(self.meta.view_parser),
            self.api.doc(model=self.model, **self._doc_kvargs),
            marshmallow_with(
                self.meta.schema_class,
                many=False,
                strict=True,
                request_parser=self.meta.view_parser),
            function)

    def get_html(self, function: Callable) -> Callable:
        return _combine(
            self._auth,
            self.api.expect(self.meta.view_parser),
            self.api.doc(model=self.model, **self._doc_kvargs),
            function)

    def put(self, function: Callable) -> Callable:
        return _combine(
            # @validate_schema(put_validator)
            self._auth,
            self.api.doc(model=self.model, **self._doc_kvargs),
            self.api.expect(self.model),
            marshmallow_with(
                self.meta.schema_class,
                many=False,
                strict=True,
                request_parser=self.meta.view_parser),
            function)

    def patch(self, function: Callable) -> Callable:
        return self.put(function)

    def patch(self, function: Callable) -> Callable:
        return _combine(
            self._auth,
            self.api.doc(model=self.model, **self._doc_kvargs),
            self.api.expect(self.model),
            marshmallow_with(self.meta.schema_class, many=False, strict=True),
            function)

    def delete(self, function: Callable) -> Callable:
        response_status = HTTPStatus.NO_CONTENT

        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
            return None, response_status

        return _combine(
            self._auth,
            self.api.doc(**self._doc_kvargs),
            self.api.response(response_status, response_status.phrase),
            wrapper)
