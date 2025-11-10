import glob
import os

import typesense
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import (
    check_for_hash,
    extract_fulltext,
)
from acdh_xml_pyutils.xml import NSMAP
from tqdm import tqdm
from typesense.exceptions import ObjectNotFound

COLLECTION_NAME = "wiener-rundschau-static"
files = glob.glob("./data/editions/*.xml")
tag_blacklist = [
    "{http://www.tei-c.org/ns/1.0}abbr",
    "{http://www.tei-c.org/ns/1.0}del",
]
namespaces = {"tei": "http://www.tei-c.org/ns/1.0"}


TYPESENSE_API_KEY = os.environ.get("TYPESENSE_API_KEY", "xyz")
TYPESENSE_TIMEOUT = os.environ.get("TYPESENSE_TIMEOUT", "120")
TYPESENSE_HOST = os.environ.get("TYPESENSE_HOST", "localhost")
TYPESENSE_PORT = os.environ.get("TYPESENSE_PORT", "8108")
TYPESENSE_PROTOCOL = os.environ.get("TYPESENSE_PROTOCOL", "http")
client = typesense.Client(
    {
        "nodes": [
            {
                "host": TYPESENSE_HOST,
                "port": TYPESENSE_PORT,
                "protocol": TYPESENSE_PROTOCOL,
            }
        ],
        "api_key": TYPESENSE_API_KEY,
        "connection_timeout_seconds": int(TYPESENSE_TIMEOUT),
    }
)


try:
    client.collections[COLLECTION_NAME].delete()
except ObjectNotFound:
    pass

current_schema = {
    "name": COLLECTION_NAME,
    "enable_nested_fields": True,
    "fields": [
        {"name": "id", "type": "string"},
        {"name": "rec_id", "type": "string", "sort": True},
        {"name": "title", "type": "string"},
        {"name": "full_text", "type": "string"},
        {"name": "year", "type": "int32", "sort": True, "facet": True},
        {"name": ".*_entities", "type": "auto", "facet": True, "optional": True},
    ],
}

client.collections.create(current_schema)


records = []
cfts_records = []
for x in tqdm(files, total=len(files)):
    doc = TeiReader(x)
    try:
        body = doc.any_xpath(".//tei:body")[0]
    except IndexError:
        continue
    record = {}
    record["id"] = os.path.split(x)[-1].replace(".xml", "")
    record["rec_id"] = os.path.split(x)[-1].replace(".xml", "")
    record["title"] = doc.any_xpath(".//tei:titleStmt/tei:title[@level='a']")[0].text
    record["full_text"] = extract_fulltext(body, tag_blacklist=tag_blacklist)
    record["year"] = int(doc.any_xpath(".//tei:date/@when-iso")[0].split("-")[0])

    record["bibl_entities"] = []
    for y in doc.any_xpath(".//tei:bibl[@n='current text' and @corresp]"):
        item = {}
        item["id"] = check_for_hash(y.attrib["corresp"])
        item["label"] = y.xpath("./tei:title[@level='a']/text()", namespaces=NSMAP)[0]
        try:
            item["author"] = y.xpath("./tei:author/text()", namespaces=NSMAP)[0]
        except IndexError:
            item["author"] = "ohne Autor*in"
        record["bibl_entities"].append(item)

    record["author_entities"] = []
    for y in doc.any_xpath(
        ".//tei:bibl[@n='current text']/tei:author[@ref and ./text()]"
    ):
        item = {}
        item["id"] = check_for_hash(y.attrib["ref"])
        item["label"] = y.text
        record["author_entities"].append(item)

    records.append(record)


make_index = client.collections[COLLECTION_NAME].documents.import_(records)
print(make_index)
print("done with indexing")
