from komodo.core.tools.mongo.mongo_connect import get_mongo_client
from komodo.core.tools.mongo.mongo_databases import MongoDBLister
from komodo.core.tools.mongo.mongo_query import MongoDBQuery
from komodo.core.tools.mongo.mongo_schema import MongoDBSchema
from komodo.testdata.config import TestConfig


def test_mongo_connection_string():
    url = TestConfig.get_mongo_connection_string()
    client = get_mongo_client(url)
    print(client.list_database_names())
    client.close()


def test_mongo_database_tool():
    url = TestConfig.get_mongo_connection_string()
    mongodb_lister = MongoDBLister(url)
    result = mongodb_lister.action({"list_collections": True})
    assert result is not None


def test_mongo_query_tool():
    url = TestConfig.get_mongo_connection_string()
    mongodb_query = MongoDBQuery(url)
    query_args = {
        "database_name": "test_database",
        "collection_name": "posts",
        "query": '{"author": "Mike"}'
    }
    result = mongodb_query.action(query_args)
    print(result)
    assert result is not None


def test_mongo_schema_tool():
    url = TestConfig.get_mongo_connection_string()
    mongodb_schema = MongoDBSchema(url)
    result = mongodb_schema.action({"database_name": "test_database", "collection_name": "posts"})
    print(result)
    assert result is not None
