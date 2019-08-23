from typing import Type
from copy import deepcopy

from marshmallow import Schema
from flask_restplus.reqparse import RequestParser


class SchemaParser(RequestParser):
    def __init__(self, schema_class: Type[Schema], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema_class = schema_class

    def copy(self):
        """Creates a copy of this RequestParser with the same set of arguments"""
        parser_copy = self.__class__(self.schema_class, self.argument_class, self.result_class)
        parser_copy.args = deepcopy(self.args)
        parser_copy.trim = self.trim
        parser_copy.bundle_errors = self.bundle_errors
        return parser_copy

    def add_selects_argument(self, choices: tuple = ()):
        # TODO custom argument class to check for fields that do not belong
        if not choices and hasattr(self.schema_class, "model_columns"):
            choices = tuple(self.schema_class.model_columns())

        if choices:
            help_ = "Select what fields to display [%s]" % ", ".join(choices)
        else:
            help_ = "Select columns"

        return self.add_argument(
            "selects", type=str, help=help_, action="append"
        )  # , choices=choices)

    def add_fields_argument(self, choices: tuple = ()):
        # TODO custom argument class to check for fields that do not belong
        if not choices and hasattr(self.schema_class, "model_relationships"):
            choices = tuple(self.schema_class.model_relationships())

        if choices:
            help_ = "Addition fields to include in the response [%s]" % ", ".join(choices)
        else:
            help_ = "Addition fields to include in the response"

        return self.add_argument(
            "fields", action="append", type=str, help=help_
        )  # , choices=choices)

    def add_pagination_arguments(self):
        self.add_argument("offset", type=int, help="Number of items to skip before returning the results.")
        self.add_argument(
            "limit", type=int, help="Maximum number of items to return."
        )
        self.add_argument("order_on", type=str, help="Order On column")
        self.add_argument("order_by", choices=("ASC", "DESC"), help="Order By asc/desc")

    # def add_schema_arguments(self):
    #     for k, v in self.schema_class._declared_fields.items():
    #         self.add_argument(k, type=str)
