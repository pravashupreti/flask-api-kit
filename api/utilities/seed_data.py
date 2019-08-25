import os

from logzero import logger
from sqlalchemy.orm import Session

from api.utilities.db import table_name_set, session_commit_context, disable_triggers
from api.fixtures.xml_fixture import XMLFixture
from api.utilities.xml import get_first_table
from config import Config, TESTING


class SeedData:
    seed_path = None
    seed_file_order = None
    file_mapper = {}

    @classmethod
    def run(cls, session: Session):
        cls.downgrade(session)
        cls.upgrade(session)

    @classmethod
    def _upgrade_table(cls, session: Session, file: str):
        xml_file = os.path.join(cls.seed_path, file)
        fixture = XMLFixture(session, get_first_table(xml_file))

        logger.debug("SEEDING TABLE '{}' from file '{}'".format(fixture.table_name, xml_file))

        cls.insert_data(session, fixture)

    @classmethod
    def upgrade_table(cls, session, file: str):
        with session_commit_context(session):
            cls._upgrade_table(session, file)

    @classmethod
    def update(cls, session, file: str):
        xml_file = os.path.join(cls.seed_path, file)
        fixture = XMLFixture(session, get_first_table(xml_file))

        with session_commit_context(session):
            fixture.update()

    @classmethod
    def upgrade(cls, session: Session, seed_xmls=None):
        if seed_xmls is None:
            seed_xmls = cls.seed_file_order
        with session_commit_context(session, deferred=True):
            for file in seed_xmls:
                cls._upgrade_table(session, file)

    @classmethod
    def downgrade(cls, session: Session, tables=None):
        xml_file = ""
        if tables is None:
            tables = table_name_set(session)
        try:
            for file in cls.seed_file_order:
                xml_file = os.path.join(cls.seed_path, file)
                fixture = XMLFixture(session, get_first_table(xml_file))

                if fixture.table_name not in tables:
                    logger.debug("Skipping '{}' from file '{}' (it doesn't exist)".format(
                        fixture.table_name, xml_file))
                    continue

                cls.file_mapper[fixture.table_name] = file

                logger.debug("TRUNCATING TABLE '{}' from file '{}'".format(fixture.table_name, xml_file))

                fixture.unload()

            session.commit()
        except Exception as error:
            session.rollback()
            logger.error("Error in file:", xml_file)
            raise error

    @classmethod
    def insert_data(cls, session: Session, fixture: XMLFixture):

        if Config.FLASK_ENV == TESTING:
            # TODO remove disable_triggers context after fixing the test seed
            with disable_triggers(session, fixture.table_name):
                fixture.load()
        else:
            fixture.load()
