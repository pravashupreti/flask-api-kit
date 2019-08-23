from typing import Mapping

from sqlalchemy import inspect
from sqlalchemy.orm import Query
from sqlalchemy.ext.hybrid import hybrid_property

from api.models.meta import session


class BaseModel:
    def __repr__(self) -> str:
        return "<%s %r>" % (type(self).__name__, self.id)

    @classmethod
    def query(cls) -> Query:
        return Query(cls, session)

    @classmethod
    def fetch(cls, params: Mapping, query: Query = None):
        if not query:
            query = session.query(cls)

        for param in params:
            if param in inspect(cls).columns:
                if isinstance(params.get(param), list) and params.get(param):
                    query = query.filter(getattr(cls, param).in_(params.get(param)))
                else:
                    query = query.filter(getattr(cls, param) == params.get(param))
            if param in inspect(cls).relationships:
                relation_params = params.get(param)
                for relation_param in params.get(param):
                    query = query.filter(relation_params.get(relation_param))

        order_on = (
            params.get("order_on")
            if params.get("order_on") and params.get("order_on") in inspect(cls).columns
            else "id"
        )
        order_by = params.get("order_by").upper() if params.get("order_by") else "ASC"

        if order_on in inspect(cls).columns:
            query = (
                query.order_by(getattr(cls, order_on).desc())
                if order_by == "DESC"
                else query.order_by(getattr(cls, order_on).asc())
            )

        if params.get("limit"):
            limit = int(params.get("limit"))
            offset = int(params.get("offset")) if params.get("offset") else 0
            query = query.limit(limit)
            query = query.offset(offset)

        return query.all()

    @classmethod
    def fetch_one(cls, params: Mapping):
        query = session.query(cls)

        for param in params:
            if param in inspect(cls).columns:
                query = query.filter(getattr(cls, param) == params.get(param))
            if param in inspect(cls).relationships:
                relation_params = params.get(param)
                for relation_param in params.get(param):
                    query = query.filter(relation_params.get(relation_param))

        order_on = (
            params.get("order_on")
            if params.get("order_on") and params.get("order_on") in inspect(cls).columns
            else "id"
        )
        order_by = params.get("order_by").upper() if params.get("order_by") else "ASC"

        if order_on in inspect(cls).columns:
            query = (
                query.order_by(getattr(cls, order_on).desc())
                if order_by == "DESC"
                else query.order_by(getattr(cls, order_on).asc())
            )

        return query.first()

    @classmethod
    def fetch_by_id(cls, id):
        query = session.query(cls)
        query = query.filter(getattr(cls, "id") == id)

        return query.first()

    @classmethod
    def create(cls, data):
        session.add(data)

    @classmethod
    def save(cls, object):
        session.add(object)

    @classmethod
    def update(cls, data):
        session.add(data)

    @classmethod
    def delete(cls, object):
        session.delete(object)

    @classmethod
    def delete_all(cls, params: Mapping, query: Query = None):
        if not query:
            query = session.query(cls)

        for param in params:
            if param in inspect(cls).columns:
                if isinstance(params.get(param), list) and params.get(param):
                    query = query.filter(getattr(cls, param).in_(params.get(param)))
                else:
                    query = query.filter(getattr(cls, param) == params.get(param))
            if param in inspect(cls).relationships:
                relation_params = params.get(param)
                for relation_param in params.get(param):
                    query = query.filter(relation_params.get(relation_param))

        query.delete()

    @classmethod
    def exists(cls, id):
        primary_key = inspect(cls).primary_key[0].key
        query = session.query(cls)
        query = query.filter(getattr(cls, primary_key) == id)
        return query.scalar()

    @classmethod
    def column_names(cls):
        return [c.name for c in inspect(cls).columns]

    @classmethod
    def relation_names(cls):
        return [r for r, _ in inspect(cls).relationships.items()]

    @classmethod
    def hybrid_property_name(cls):
        return [
            attribute.__name__
            for attribute in inspect(cls).all_orm_descriptors
            if isinstance(attribute, hybrid_property)
        ]

    @classmethod
    def clone(cls, obj, include=None, exclude=None, mod_data=None):
        columns = set(cls.column_names())
        if include:
            columns = columns.union(include)
        if exclude:
            columns = columns - set(exclude)
        primary_keys = set(pk.key for pk in inspect(cls).primary_key)
        columns = columns - primary_keys
        params = {col: getattr(obj, col) for col in columns}
        if mod_data:
            params.update(mod_data)
        cloned_obj = cls(**params)
        cls.create(cloned_obj)
        return cloned_obj
