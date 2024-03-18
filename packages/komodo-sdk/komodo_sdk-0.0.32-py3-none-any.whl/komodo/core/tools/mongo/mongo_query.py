import json
from datetime import datetime

from bson import ObjectId

from komodo.core.tools.mongo.mongo_connect import get_mongo_client
from komodo.framework.komodo_tool import KomodoTool


class MongoDBQuery(KomodoTool):
    name = "MongoDB Query"
    purpose = "Executes a query on a specified collection in a MongoDB database and returns the results. " + \
              "Optionally encodes the results as a Base64 encoded string."
    shortcode = "mongodb_query"

    definition = {
        "type": "function",
        "function": {
            "name": shortcode,
            "description": purpose,
            "parameters": {
                "type": "object",
                "properties": {
                    "database_name": {
                        "type": "string",
                        "description": "The name of the MongoDB database to query."
                    },
                    "collection_name": {
                        "type": "string",
                        "description": "The name of the collection within the database to query."
                    },
                    "query": {
                        "type": "string",
                        "description": "A JSON string representing the query to execute on the collection."
                    },
                    "page": {
                        "type": "integer",
                        "description": "The page number to retrieve. Defaults to 1.",
                        "default": 1
                    },
                    "pageSize": {
                        "type": "integer",
                        "description": "The number of items per page. Defaults to 10.",
                        "default": 10
                    }
                },
                "required": ["database", "collection", "query"]
            }
        }
    }

    def __init__(self):
        super().__init__(shortcode=self.shortcode,
                         definition=self.definition,
                         action=self.action)

    def action(self, args):
        try:
            client = get_mongo_client()
            database_name = args["database_name"]
            collection_name = args["collection_name"]
            query_string = args["query"]
            page = args.get("page", 1)
            pageSize = args.get("pageSize", 10)

            # Convert the query string to a dictionary
            query = json.loads(query_string)

            # Calculate the number of documents to skip
            skips = pageSize * (page - 1)

            db = client[database_name]
            collection = db[collection_name]
            results = list(collection.find(query).skip(skips).limit(pageSize))
            client.close()

            # Custom JSON Encoder to handle ObjectId and datetime
            class CustomEncoder(json.JSONEncoder):
                def default(self, obj):
                    if isinstance(obj, ObjectId):
                        return str(obj)
                    if isinstance(obj, datetime):
                        return obj.isoformat()
                    return json.JSONEncoder.default(self, obj)

            print(results)
            encoded = json.dumps(results, cls=CustomEncoder)
            return KomodoTool.to_base64(encoded)

        except Exception as e:
            return "Error: Could not execute MongoDB query: " + str(e)


if __name__ == "__main__":
    mongodb_query = MongoDBQuery()
    query_args = {
        "database_name": "test_database",
        "collection_name": "posts",
        "query": '{"author": "Mike"}'
    }
    result = mongodb_query.action(query_args)
    print(result)
