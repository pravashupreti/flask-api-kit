from typing import Set, MutableMapping, Tuple, Any, NoReturn

from sqlalchemy.orm import Session

from .base_fixture import BaseFixture


class Loader:
    def __init__(self, session: Session):
        self.session = session
        self._fixtures: MutableMapping[str, BaseFixture] = dict()
        self._pending: Set[str] = set()

    def add(self, fixture: BaseFixture) -> NoReturn:
        self._fixtures[fixture.key] = fixture
        self._pending.add(fixture.key)

    def load(self, pending: Set[str] = None, circular: Tuple[str, Any] = None) -> NoReturn:
        if pending is None:
            pending = self._pending.copy()

        if circular is None:
            circular = tuple()

        while pending:
            key = pending.pop()

            if key not in self._fixtures:
                raise Exception("no fixture for key: '{}'".format(key))

            fixture = self._fixtures[key]

            if key in circular:
                continue
                # raise Exception("circular reference to: '{}', path: '{}'".format(key, "', '".join(circular)))

            dependencies = self._pending & fixture.dependencies
            if dependencies:
                self.load(dependencies, (key, *circular))

            if key in self._pending:
                fixture.load()
                self._pending.remove(key)
