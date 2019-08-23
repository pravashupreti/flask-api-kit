from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError

from api.models.meta import session
from api.exceptions.database_exception import DatabaseException


@contextmanager
def session_commit_context():
    try:
        yield session
        session.commit()
    except SQLAlchemyError as error:
        session.rollback()
        raise DatabaseException(detail=error._message())
    except Exception as error:
        session.rollback()
        raise error
