from komodo.core.tools.mongo.mongo_connect import get_mongo_client
from komodo.framework.komodo_tool import KomodoTool


class MongoDBUnique(KomodoTool):
    name = "MongoDB Unique Value Finder"
    purpose = "Finds unique values for a specified field within a MongoDB collection."
    shortcode = "mongodb_unique"

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
                        "description": "The name of the database."
                    },
                    "collection_name": {
                        "type": "string",
                        "description": "The name of the collection to search for unique values."
                    },
                    "field_name": {
                        "type": "string",
                        "description": "The field for which to find unique values."
                    }
                },
                "required": ["database_name", "collection_name", "field_name"]
            }
        }
    }

    def __init__(self):
        super().__init__(shortcode=self.shortcode,
                         definition=self.definition,
                         action=self.action)

    def action(self, args):
        try:
            database_name = args["database_name"]
            collection_name = args["collection_name"]
            field_name = args["field_name"]

            client = get_mongo_client()
            db = client[database_name]
            unique_values = db[collection_name].distinct(field_name)
            client.close()

            print(unique_values)
            return KomodoTool.to_base64(unique_values)

        except Exception as e:
            return "Error: Could not find unique values: " + str(e)


if __name__ == "__main__":
    tool = MongoDBUnique()
    print(tool.definition)
    print(tool.action({"database_name": "test_database", "collection_name": "posts", "field_name": "author"}))
