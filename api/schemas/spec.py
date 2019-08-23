from apispec import APISpec
from flask_restplus import Api
from marshmallow import Schema
from typing import Type, Union, List
from flask_restplus.model import Model
from flask_restplus.namespace import Namespace
from apispec.ext.marshmallow import MarshmallowPlugin

spec = APISpec(title="", version="1.0.0", plugins=(MarshmallowPlugin(),))

BaseApi = Union[Api, Namespace]


# https://apispec.readthedocs.io/en/stable/api_ext.html
# https://flask-restplus.readthedocs.io/en/stable/marshalling.html#define-model-using-json-schema
def marshmallow_to_restplus(
    api: BaseApi, schema: Type[Schema], fields: Union[tuple, List[str]] = None
) -> Model:
    class_name = schema.Meta.model.__name__
    spec.definition(class_name, schema=schema)

    openapi = spec.to_dict()

    data: dict = openapi["definitions"][class_name]

    if fields:
        data["properties"] = {k: v for k, v in data["properties"].iteritems() if k in fields}

    return api.schema_model(class_name, data)
