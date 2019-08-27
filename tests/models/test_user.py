

from api.models.user import User
from api.models.meta import session
from tests.test_base import TestBase


class TestUser(TestBase):
    def test_user_name(self, client):
        user = session.query(User).get("91d9c872-6c3b-40aa-9b23-9f8daf4d179f")
        assert user is not None
        assert user.username == "aiden.660"

        aiden_660 = session.query(User).filter_by(username="aiden.660").all()

        assert len(aiden_660) == 1

        assert str(aiden_660[0].id) == "91d9c872-6c3b-40aa-9b23-9f8daf4d179f"
        