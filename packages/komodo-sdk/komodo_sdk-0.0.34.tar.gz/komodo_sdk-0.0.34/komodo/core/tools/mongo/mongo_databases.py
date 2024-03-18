from komodo.core.tools.mongo.mongo_connect import get_mongo_client
from komodo.framework.komodo_tool import KomodoTool



class MongoDBLister(KomodoTool):
    name = "MongoDB Lister"
    purpose = "Lists all databases and collections within those databases in a MongoDB server. " + \
              "Useful for navigating and querying MongoDB data structures."
    shortcode = "mongodb_lister"

    definition = {
        "type": "function",
        "function": {
            "name": shortcode,
            "description": purpose,
            "parameters": {
                "type": "object",
                "properties": {
                    "list_collections": {
                        "type": "boolean",
                        "description": "If true, lists collections for each database. Defaults to false.",
                        "default": False
                    },
                },
                "required": []
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
            data = {"databases": {}}
            list_collections = args.get("list_collections", False)

            for db_name in client.list_database_names():
                if list_collections:
                    db = client[db_name]
                    collection_names = db.list_collection_names()
                    data["databases"][db_name] = collection_names
                else:
                    data["databases"][db_name] = []
            client.close()

            print(data)
            return KomodoTool.to_base64(data)

        except Exception as e:
            return "Error: Could not list MongoDB data: " + str(e)


if __name__ == "__main__":
    mongodb_lister = MongoDBLister()
    result = mongodb_lister.action({"list_collections": True})
    print(result)
