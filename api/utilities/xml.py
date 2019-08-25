from xml.dom import minidom
from xml.dom.minidom import Element, Document, Text
from typing import Callable, Iterator
from contextlib import contextmanager


@contextmanager
def xmldoc_context(file_in: str, file_out: str = None) -> Iterator[Document]:
    if file_out is None:
        file_out = file_in

    try:
        xmldoc = minidom.parse(file_in)
    except FileNotFoundError:
        xmldoc = Document()

    yield xmldoc

    with open(file_out, 'w') as file:
        xmldoc.writexml(file, indent="  ", newl="\n")


def get_first_table(file: str):
    xmldoc = minidom.parse(file)
    return xmldoc.getElementsByTagName("table")[0]


def remove_whitespace(el: Element):
    for node in [n for n in el.childNodes if isinstance(n, Text) and not n.nodeValue.strip()]:
        el.removeChild(node)


def filter_xml(xmldoc: Document, test: Callable[[Element], bool]):
    table_node = get_or_create_table(xmldoc)
    rows = table_node.getElementsByTagName("row")

    for row in rows:
        if not test(row):
            table_node.removeChild(row)


def get_or_create_table(xmldoc: Document) -> Element:
    tables = xmldoc.getElementsByTagName("table")

    if tables:
        return tables[0]

    table = xmldoc.createElement("table")
    xmldoc.appendChild(table)
    return table


def map_xml(xmldoc: Document, callback: Callable[[Element], Element]):
    table_node = get_or_create_table(xmldoc)
    rows = table_node.getElementsByTagName("row")

    for row in rows:
        callback(row)
