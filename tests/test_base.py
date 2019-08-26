# pylint: disable=no-self-use
import pytest
from alembic import command

from app import create_app
from api.models.meta import session
from tests.seed import TestDataSeed
from tests.conftest import alembic_cfg
from unittest.mock import patch

from api.services import StorageService

# from api.services import StorageService
# from config import Config

def mock_init_services():
    StorageService.minio_client = None

class TestBase:
    test_app = None
    test_client = None
    is_db_migrated = False
    abort_testing = False
    token = None
    changed_tables = []

    @classmethod
    @patch('app._init_services')
    def get_app(cls, init_services):
        init_services.side_effect = mock_init_services
        test_app = create_app()
        test_app.app_context().push()
        test_app.debug = True

        return test_app

    @pytest.fixture(scope="function")
    def client(self):
        test_app = TestBase.get_app()
        client = test_app.test_client()
        # client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(self.auth_token())
        return client

    def setup_method(self, _):
        try:
            if TestBase.abort_testing:
                raise Exception("Abort testing due to data seeding failed")
        except Exception as error:
            TestBase.abort(error)

    def teardown_method(self, method):
        TestDataSeed.rollback_test_seed(session)

    @classmethod
    def setup_class(cls):
        cls.get_app()

        if TestBase.is_db_migrated is False:
            TestBase.is_db_migrated = True
            TestDataSeed.downgrade(session)
            TestBase.downgrade()
            TestBase.upgrade()
            TestDataSeed.run(session)
            TestDataSeed.listens_for_changes()

    @classmethod
    def abort(cls, error):
        TestBase.abort_testing = True
        pytest.fail(error)

    @classmethod
    def upgrade(cls):
        try:
            command.upgrade(alembic_cfg, 'head', sql=False, tag=None)
        except Exception as error:
            TestBase.abort(error)

    @classmethod
    def downgrade(cls):
        try:
            command.downgrade(alembic_cfg, 'base', sql=False, tag=None)
        except Exception as error:
            TestBase.abort(error)
