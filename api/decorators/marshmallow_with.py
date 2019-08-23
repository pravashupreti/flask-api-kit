from functools import wraps, reduce
from http import HTTPStatus
from operator import iconcat
from typing import Callable, Type, Optional, List, Tuple

from flask_restplus.reqparse import RequestParser
from marshmallow.fields import Nested
from marshmallow import ValidationError
from marshmallow import Schema as MarshmallowSchema

from api.models.meta import Base
from api.schemas.base_schema import BaseSchema


def _get_query_list(query_param: str, request_parser: RequestParser) -> Optional[List[str]]:
    params = request_parser.parse_args()

    if query_param not in params:
        return None

    items = params[query_param]

    if not items:
        return None

    if isinstance(items, (tuple, list)):
        return reduce(iconcat, [[x.strip() for x in item.split(",")] for item in items], [])

    if isinstance(items, str):
        return [x.strip() for x in items.split(",")]

    raise Exception("Can't handle '%s' type (%s)" % query_param, type(items))


def _get_fields_recursively(schema: MarshmallowSchema, fields: Tuple[str, ...]) -> Tuple[str, ...]:
    select_fields = set(schema.model_columns() + schema.model_hybrid_columns()).intersection(fields)

    nested_fields = set(fields) - select_fields
    recursive_fields = set()

    for field in nested_fields:
        if "." in field:
            nested_schema_name, nested_schema_field = field.split(".", 1)
            if nested_schema_name not in schema.declared_fields:
                raise ValidationError(
                    "attribute '{}' does not exist in '{}'".format(
                        nested_schema_name, schema.__class__.__name__
                    )
                )

            nested_schema = schema.declared_fields[nested_schema_name].schema
            recursive_fields = recursive_fields.union(
                "{}.{}".format(nested_schema_name, sub_field)
                for sub_field in _get_fields_recursively(nested_schema, (nested_schema_field,))
            )
        else:
            if field not in schema.declared_fields:
                raise ValidationError(
                    "attribute '{}' does not exist in '{}'".format(field, schema.__class__.__name__)
                )
            if hasattr(schema.declared_fields[field], "schema"):
                nested_schema = schema.declared_fields[field].schema
                if isinstance(nested_schema, BaseSchema):
                    recursive_fields = recursive_fields.union(
                        "{}.{}".format(field, sub_field) for sub_field in nested_schema.model_columns()
                    )
                else:
                    recursive_fields = recursive_fields.union({field})
            else:
                recursive_fields = recursive_fields.union({field})

    return tuple(select_fields.union(recursive_fields))


def _add_fields_to_kwargs(
        request_parser: Optional[RequestParser], schema_class: Type[MarshmallowSchema], **kwargs
) -> dict:
    # copies the arguments so they don't persist between request
    kwargs_copy = kwargs.copy()

    if not request_parser:
        return kwargs_copy

    selects = _get_query_list("selects", request_parser)
    if selects:
        kwargs_copy["only"] = selects
    fields = _get_query_list("fields", request_parser)
    if fields:
        if "only" in kwargs_copy:
            fields = set().union(kwargs_copy["only"], fields)
        kwargs_copy["only"] = tuple(fields)
    if "only" in kwargs_copy:
        kwargs_copy["only"] = _get_fields_recursively(schema_class(), kwargs_copy["only"])

    return kwargs_copy


def marshmallow_with(
        schema_class: Type[MarshmallowSchema],
        *mm_args,
        response_status=HTTPStatus.OK,
        request_parser: RequestParser = None,
        only=None,
        **mm_kwargs
) -> Callable:
    """
    Converts the resulting object into a dictionary.
    Based on on restplus marshal_with decorator.
    :param response_status: HTTPStatus: The default response string
    :param only: Union[List[str], Tuple[str]]: default list of only fields
    :param schema_class: Type[MarshmallowSchema]: The marshmallow schema class for the conversion
    :param request_parser: RequestParser: The request parser to use
    :return: a decorated function
    """
    if only is None and hasattr(schema_class, "model_columns"):
        only = schema_class.model_columns()

    mm_kwargs["only"] = only

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args, **kwargs) -> Tuple[dict, HTTPStatus]:
            mm_kwargs_copy = _add_fields_to_kwargs(request_parser, schema_class, **mm_kwargs)
            schema = schema_class(*mm_args, **mm_kwargs_copy)
            entity = function(*args, **kwargs)

            if isinstance(entity, Base) or (
                    isinstance(entity, list) and all(isinstance(obj, Base) for obj in entity)
            ):
                data = schema.dump(entity).data
            else:
                data = entity

            return data, response_status

        return wrapper

    return decorator
