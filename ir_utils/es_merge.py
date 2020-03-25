from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan, bulk
from typing import Dict, List
import certifi


AWS_ENDPOINT = "https://search-ir6200-xjtfl6maa3zicwvxmmygis5dry.us-east-1.es.amazonaws.com" 
AWS_INDEX = "crawler"
AWS_KIBANA = "https://search-ir6200-xjtfl6maa3zicwvxmmygis5dry.us-east-1.es.amazonaws.com/_plugin/kibana/app/kibana#/dev_tools/console?_g=()"


def _assert_attribute(attr_name, attr_type, source):
    assert (attr_name in source and type(source[attr_name]) is attr_type), \
        f"Missing '{attr_name}' (type: {attr_type})"


def _extract_doc_from_json(doc_id, source):
    assert doc_id and type(doc_id) is str, "Missing '_id' (type: str)"
    _assert_attribute("inlinks", list, source)
    _assert_attribute("outlinks", list, source)
    _assert_attribute("url", str, source)
    _assert_attribute("wave", int, source)
    _assert_attribute("body", str, source)
    _assert_attribute("crawler", str, source)
    return {
        "_op_type": "update",
        "_id": doc_id,
        "upsert": {
            "body": source["body"],
            "url": source["url"],
            "wave": source["wave"],
            "outlinks": source["outlinks"],
            "inlinks": source["inlinks"],
            "crawler": source["crawler"],
            "raw_html": source.get("raw_html", ""),
            "headers": source.get("headers", "")
        },
        "script": {
            "lang": "painless",
            "source": """
                List inlinks = params.inlinks;
                List outlinks = params.outlinks;
                Set sourceInlinks = new HashSet(ctx._source.inlinks);
                Set sourceOutlinks = new HashSet(ctx._source.outlinks);
                for (int i = 0; i < inlinks.size(); i++) {
                    if (!sourceInlinks.contains(inlinks[i])) {
                        ctx._source.inlinks.add(inlinks[i]);
                    }
                }
                for (int i = 0; i < outlinks.size(); i++) {
                    if (!sourceOutlinks.contains(outlinks[i])) {
                        ctx._source.outlinks.add(outlinks[i]);
                    }
                }
            """,
            "params": {
                "inlinks": source["inlinks"],
                "outlinks": source["outlinks"]
            }
        }
    }


def _get_all_local_docs(local_endpoint, local_index, doc_transform_func):
    local = Elasticsearch(hosts=[local_endpoint])
    es_query = {
        "query": {
            "match_all": {}
        }
    }
    processed = 0
    for json in scan(local, index=local_index, query=es_query, request_timeout=50000):
        yield _extract_doc_from_json(json["_id"], doc_transform_func(json["_source"]))
        processed += 1
        if processed % 1000 == 0:
            print(f"\t{processed} docs processed")
    print(f"\t{processed} docs processed")


def _merge(remote_endpoint, remote_index, docs):
    remote = Elasticsearch(hosts=[remote_endpoint], use_ssl=True,
        ca_certs=certifi.where())
    bulk(remote, docs, index=remote_index, max_chunk_bytes=10485760,
        request_timeout=50000)

def _confirm_input(remote_endpoint, remote_index) -> bool:
    print(f"Remote endpoint: {remote_endpoint}")
    print(f"Remote index: {remote_index}")
    confirm = input("Verify info before proceed, this is a non-reversible " 
        "operation\nDoes this look correct? y/n? ")
    if confirm == "y":
        print("Merging indices:")
        return True
    print("Cancelling merging operation")
    return False


def merge_non_es(docs: List[Dict],
    remote_endpoint: str = AWS_ENDPOINT, remote_index: str = AWS_INDEX, 
    kibana_endpoint: str = AWS_KIBANA):
    if not _confirm_input(remote_endpoint, remote_index):
        return
    docs = [_extract_doc_from_json(doc["_id"], doc) for doc in docs]
    _merge(remote_endpoint, remote_index, docs)
    print("Done")
    print(f"Check for your data at {kibana_endpoint}")


def merge_es(local_endpoint: str, local_index: str, 
    remote_endpoint: str = AWS_ENDPOINT, remote_index: str = "", 
    kibana_endpoint: str = AWS_KIBANA, doc_transform_func=lambda x: x):
    if not remote_index:
        remote_index = local_index
    print(f"Local endpoint: {local_endpoint}")
    print(f"Local index: {local_index}")
    if not _confirm_input(remote_endpoint, remote_index):
        return
    docs = _get_all_local_docs(local_endpoint, local_index, 
        doc_transform_func)
    _merge(remote_endpoint, remote_index, docs)
    print("Done")
    print(f"Check for your data at {kibana_endpoint}")
    

if __name__ == "__main__":

    lst = [
        {
            "_id": "example.com/abc.html",
            "body": "the page body",
            "url": "https://example.com/abc.html",
            "wave": -1,
            "outlinks": [],
            "inlinks": [],
            "crawler": "cralwer name"
        }
    ]

    merge_non_es(lst)