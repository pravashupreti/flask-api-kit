from apispec import APISpec
from marshmallow import Schema
from typing import Type, Union, Tuple
from flask_restplus import Api
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_restplus.namespace import Namespace, SchemaModel

from api.services.schema_parser import SchemaParser

BaseApi = Union[Namespace, Api]


class MetaService:
    spec = APISpec(title="", version="1.0.0", plugins=(MarshmallowPlugin(),))

    def __init__(self, schema_class: Type[Schema]):
        self.schema_class = schema_class

        self.view_parser = SchemaParser(schema_class)
        self.view_parser.add_selects_argument()
        self.view_parser.add_fields_argument()

        self.index_parser = self.view_parser.copy()
        self.index_parser.add_pagination_arguments()

        self.api_model = self.marshmallow_to_restplus(schema_class, relations=False)

    @classmethod
    def marshmallow_to_openapi(cls, schema: Type[Schema], relations=True) -> Tuple[str, dict]:
        class_name = schema.Meta.model.__name__ if hasattr(schema.Meta, "model") else schema.__name__
        cls.spec.definition(class_name, schema=schema)

        openapi = cls.spec.to_dict()

        data = openapi["definitions"][class_name]

        if not relations:
            properties = {}

            for k, v in data["properties"].items():
                if "$ref" in v:
                    continue
                if "type" not in v:
                    raise Exception("property '%s' does not have a 'type'" % k)
                if v["type"] not in ("object", "array"):
                    properties[k] = v
            data["properties"] = properties

        return class_name, data

    # https://apispec.readthedocs.io/en/stable/api_ext.html
    # https://flask-restplus.readthedocs.io/en/stable/marshalling.html#define-model-using-json-schema
    @classmethod
    def marshmallow_to_restplus(cls, schema: Type[Schema], relations=True) -> SchemaModel:
        """
        https://apispec.readthedocs.io/en/stable/api_ext.html
        https://flask-restplus.readthedocs.io/en/stable/marshalling.html#define-model-using-json-schema
        :param schema: Type[Schema]: the Marshmallow Schema
        :param relations: bool: Should the model include relations
        :return: SchemaModel: the restplus model
        """
        class_name, data = cls.marshmallow_to_openapi(schema, relations)

        return SchemaModel(class_name, data)
