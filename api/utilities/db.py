from typing import Iterable, Mapping, Any, NoReturn, Set, Optional, Union
from contextlib import contextmanager

from logzero import logger
from sqlalchemy.exc import SQLAlchemyError

from config import Config
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Query, Session
from sqlalchemy.ext.hybrid import hybrid_property

IGNORED_TABLES = ("alembic_version",)  # TODO import from alembic settings

Scalar = Optional[Union[str, float, int, bool]]
Row = Mapping[str, Scalar]


@contextmanager
def session_commit_context(session: Session, deferred=False) -> Iterable[Session]:
    try:
        if deferred:
            session.execute("SET CONSTRAINTS ALL DEFERRED")
        yield session
        session.commit()
    except SQLAlchemyError as error:
        session.rollback()
        raise error
    except Exception as error:
        session.rollback()
        raise error


@contextmanager
def disable_triggers(session: Session, table: str) -> Iterable[Session]:
    logger.warning("disable triggers should not be used, use deferred option instead")
    session.execute("ALTER TABLE {} DISABLE TRIGGER ALL".format(table))
    yield session
    session.execute("ALTER TABLE {} ENABLE TRIGGER ALL".format(table))


def raw_sql(query: Query) -> str:
    return str(query.statement.compile(dialect=postgresql.dialect()))


def table_name_set(session: Session) -> Set[str]:
    result = session.execute("SELECT table_name FROM information_schema.tables "
                             "WHERE table_schema = 'public';")

    return set(row.table_name for row in result if row.table_name not in IGNORED_TABLES)


def table_ids(session: Session, table: str) -> Set[str]:
    result = session.execute("SELECT id FROM {};".format(table))

    return set(str(r["id"]) for r in result)


def table_rows(session: Session, table: str) -> Iterable[Mapping[str, Any]]:
    result = session.execute("SELECT * FROM {}".format(table))

    for row in result:
        yield {k: str(v) for k, v in row.items() if v is not None}


def insert_row(session: Session, table: str, row: Row, logging=False) -> NoReturn:
    keys = row.keys()
    columns = ", ".join(keys)
    params = ", ".join(':' + k for k in keys)

    if logging:
        logger.debug("inserting row in '{}'".format(table))

    session.execute(
        "INSERT INTO {table} ({columns}) VALUES ({params})".format(
            table=table, columns=columns, params=params),
        row
    )


def update_row(session: Session, table: str, row: Row, pkey="id", logging=False) -> NoReturn:
    keys = [k for k in row.keys() if k != pkey]
    columns = ", ".join(keys)
    params = ", ".join(':' + k for k in keys)

    if logging:
        logger.debug("updating table '{table}' ({pkey}={value})".format(table=table, pkey=pkey, value=row[pkey]))

    session.execute(
        "UPDATE {table} SET ({columns}) = ROW({params}) WHERE {pkey} = :{pkey};".format(
            table=table, columns=columns, params=params, pkey=pkey),
        row
    )


def truncate_table(session: Session, table: str) -> NoReturn:
    logger.debug("Truncating table '{}'".format(table))
    session.execute("TRUNCATE TABLE {} CASCADE".format(table))


def truncate_all(session: Session) -> NoReturn:
    if not Config.SEED_DATABASE:
        raise Exception("SEED_DATABASE is disabled. db can not be truncated")

    for table in table_name_set(session):
        truncate_table(session, table)


def table_dependencies(session: Session, table: str) -> set:
    """
    https://stackoverflow.com/questions/1152260/postgres-sql-to-list-table-foreign-keys
    :param session:
    :param table:
    :return:
    """
    result = session.execute(
        "SELECT "
        "  ccu.table_name "
        "FROM "
        "  information_schema.table_constraints AS tc "
        "  JOIN information_schema.key_column_usage AS kcu "
        "    ON tc.constraint_name = kcu.constraint_name "
        "    AND tc.table_schema = kcu.table_schema "
        "  JOIN information_schema.constraint_column_usage AS ccu "
        "    ON ccu.constraint_name = tc.constraint_name "
        "    AND ccu.table_schema = tc.table_schema "
        "WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name=:table;",
        {
            "table": table
        }
    )

    return set(row.table_name for row in result)


def empty_tables(session):
    tables = table_name_set(session)
    empty_tables = []

    for table in tables:
        result = session.execute(f"SELECT COUNT(*) AS count FROM {table}")
        for row in result:
            if row.count == 0:
                empty_tables.append(table)

    return empty_tables


class hybrid_property_select(hybrid_property):
    """
    Used by api.schema.base_schema and marshmallow_with to determine if a property
    should be added to the select fields by default
    """
    pass
