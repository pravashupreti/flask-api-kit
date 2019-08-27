import inspect
from sqlalchemy.orm.mapper import Mapper
from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy.event import listens_for

import api.models as models
from api.utilities.seed_data import SeedData
from tests.conftest import test_path, seed_file_order
from api.utilities.db import empty_tables
from sqlalchemy.orm import Session


class TestDataSeed(SeedData):
    seed_path = test_path + '/seed/data/'
    seed_file_order = seed_file_order
    changed_tables = set()

    @classmethod
    def listens_for_changes(cls):
        for name, obj in inspect.getmembers(models):
            if isinstance(obj, DefaultMeta):
                @listens_for(obj, 'after_insert')
                def receive_after_insert(mapper: Mapper, connection, target):
                    cls.changed_tables.add(mapper.mapped_table.name)

                @listens_for(obj, 'after_update')
                def receive_after_insert(mapper, connection, target):
                    cls.changed_tables.add(mapper.mapped_table.name)

                @listens_for(obj, 'after_delete')
                def receive_after_insert(mapper, connection, target):
                    cls.changed_tables.add(mapper.mapped_table.name)

    @classmethod
    def rollback_test_seed(cls, session: Session):
        seed_xmls = []

        if cls.changed_tables:
            cls.downgrade(session, cls.changed_tables)

            for table in empty_tables(session):
                if table in SeedData.file_mapper:
                    seed_xmls.append(SeedData.file_mapper.get(table))

            cls.upgrade(session, seed_xmls)

        cls.changed_tables = set()
