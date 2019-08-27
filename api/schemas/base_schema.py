from typing import List
from marshmallow import pre_load

from sqlalchemy import inspect
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import ValidationError

from api.utilities.db import hybrid_property_select


class BaseSchema:
    @classmethod
    def model_hybrid_columns(cls) -> List[str]:
        if not issubclass(cls, ModelSchema):
            raise Exception('class "%s" is not subclass of "%s"' % (cls.__name__, ModelSchema.__name__))

        return [
            attribute.__name__ for attribute in inspect(cls.Meta.model).all_orm_descriptors
            if isinstance(attribute, hybrid_property_select)
        ]

    @classmethod
    def model_columns(cls, include_hybrid_columns=True) -> List[str]:
        if hasattr(cls, "Meta") and hasattr(cls.Meta, "selects"):
            return cls.Meta.selects

        if not issubclass(cls, ModelSchema):
            raise Exception('class "%s" is not subclass of "%s"' % (cls.__name__, ModelSchema.__name__))

        columns = [c.name for c in inspect(cls.Meta.model).columns]
        return columns + cls.model_hybrid_columns() if include_hybrid_columns else columns

    @classmethod
    def model_relationships(cls) -> List[str]:
        if hasattr(cls, "Meta") and hasattr(cls.Meta, "joins"):
            return cls.Meta.joins

        if not issubclass(cls, ModelSchema):
            raise Exception('class "%s" is not subclass of "%s"' % (cls.__name__, ModelSchema.__name__))
        relationships = inspect(cls.Meta.model).relationships
        hybrid_properties = [
            attribute.__name__ for attribute in inspect(cls.Meta.model).all_orm_descriptors
            if isinstance(attribute, hybrid_property)
        ]

        return [k for k, _ in relationships.items()] + hybrid_properties

    @classmethod
    def object_id_exists(cls, object_id, model):
        if not model.exists(object_id):
            raise ValidationError("Id {} does not exist in {}".format(object_id, model.__tablename__))

    @classmethod
    def unique_field_exists(cls, value, model, field):
        if model.fetch_one({field: value}):
            raise ValidationError(
                "'{}' should be unique, '{}' is already exist in {}".format(
                    field, value, model.__tablename__
                )
            )
