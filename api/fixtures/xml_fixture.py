from typing import List, Mapping, Set
from xml.dom.minidom import Element

from logzero import logger
from sqlalchemy.orm import Session

from api.fixtures.base_fixture import BaseFixture
from api.utilities.db import table_ids, update_row, insert_row, Row, Scalar, truncate_table, disable_triggers


class XMLFixture(BaseFixture):

    def __init__(self, session: Session, el: Element):
        self.session = session
        self._el = el
        # self.xmldoc = minidom.parse(path)
        # self._el = self.xmldoc.getElementsByTagName("table")[0]

    @property
    def dependency_elements(self) -> List[Element]:
        return self._el.getElementsByTagName("dependency")

    @property
    def row_elements(self) -> List[Element]:
        return self._el.getElementsByTagName("row")

    @property
    def rows(self) -> List[Mapping[str, Scalar]]:
        return [dict(el.attributes.items()) for el in self.row_elements]

    @property
    def table_name(self) -> str:
        return self._el.attributes["name"].value

    def insert_row(self, row: Row):
        insert_row(self.session, self.table_name, row)

    def update_row(self, row: Row):
        update_row(self.session, self.table_name, row)

    @property
    def exiting_ids(self) -> Set[str]:
        return table_ids(self.session, self.table_name)

    def update(self):
        existing = table_ids(self.session, self.table_name)

        for row in self.rows:
            if row["id"] in existing:
                logger.debug("update: %s", str(row))
                self.update_row(row)
            else:
                logger.debug("insert: %s", str(row))
                self.insert_row(row)

    def load(self):
        logger.debug("loading table '{}'".format(self.table_name))
        for row in self.rows:
            self.insert_row(row)

    def unload(self):
        truncate_table(self.session, self.table_name)

    @property
    def dependencies(self) -> Set[str]:
        return set(el.getAttribute("table") for el in self.dependency_elements)

    @property
    def key(self) -> str:
        if "key" in self._el.attributes:
            return self._el.attributes["key"]
        return self.table_name
