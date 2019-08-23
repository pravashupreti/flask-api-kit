# pylint: disable=redefined-builtin
from typing import TypeVar, Generic, List, NoReturn

from marshmallow.exceptions import ValidationError

from api.models.base_model import BaseModel
from api.exceptions import InvalidPayloadException, RowNotFoundException


T = TypeVar("T", bound=BaseModel)


class BaseService(Generic[T]):
    model = None
    model_schema = None

    @classmethod
    def fetch(cls, params) -> List[T]:
        return cls.model.fetch(params)

    @classmethod
    def fetch_one(cls, params) -> T:
        return cls.model.fetch_one(params)

    @classmethod
    def fetch_by_id(cls, id) -> T:
        data = cls.model.fetch_by_id(id)
        if not data:
            raise RowNotFoundException()

        return data

    @classmethod
    def create(cls, data: dict) -> T:
        try:
            schema = cls.model_schema(many=False)
            model_data, errors = schema.load(data)
            if errors:
                raise InvalidPayloadException("Invalid payload", errors)

            cls.model.create(model_data)

            return model_data
        except ValidationError as error:
            raise InvalidPayloadException("Invalid payload", detail=error.messages)

    @classmethod
    def update(cls, id, data: dict) -> T:
        try:
            old = cls.fetch_by_id(id)
            if not old:
                raise RowNotFoundException()

            if "id" in data:
                raise InvalidPayloadException("'id' field is not updatable")

            data["id"] = id
            schema = cls.model_schema(many=False, partial=True)
            model_data, errors = schema.load(data)
            if errors:
                raise InvalidPayloadException("Invalid payload", errors)

            cls.model.update(model_data)

            return model_data
        except ValidationError as error:
            raise InvalidPayloadException("Invalid payload", detail=error.messages)

    @classmethod
    def update_one_by_criteria(cls, criteria: dict, data: dict) -> T:
        try:
            old = cls.fetch_one(criteria)
            if not old:
                raise RowNotFoundException()
            if "id" in data:
                raise InvalidPayloadException("'id' field is not updatable")

            data["id"] = old.id
            schema = cls.model_schema(many=False, partial=True)
            model_data, errors = schema.load(data)
            if errors:
                raise InvalidPayloadException("Invalid payload", errors)

            cls.model.update(model_data)

            return model_data
        except ValidationError as error:
            raise InvalidPayloadException("Invalid payload", detail=error.messages)

    @classmethod
    def save(cls, object):
        cls.model.save(object)

    @classmethod
    def delete(cls, id) -> NoReturn:
        old = cls.fetch_by_id(id)
        if not old:
            raise RowNotFoundException()

        cls.model.delete(old)

    @classmethod
    def delete_by_params(cls, params):
        cls.model.delete_all(params)
