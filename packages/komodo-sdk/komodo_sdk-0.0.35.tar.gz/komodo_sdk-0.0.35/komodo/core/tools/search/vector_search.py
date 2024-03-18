import json

from komodo.core.vector_stores.qdrant_store import QdrantStore
from komodo.framework.komodo_tool import KomodoTool


class VectorSearch(KomodoTool):
    name = "Vector Search"
    shortcode = "vector_search_tool"
    purpose = "Search available data sources"

    definition = {
        "type": "function",
        "function": {
            "name": shortcode,
            "description": purpose,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search across all available data using vector search"
                    }
                },
                "required": ["query"]
            }
        }
    }

    def __init__(self, store):
        self.store = store
        super().__init__(shortcode=self.shortcode,
                         definition=self.definition,
                         action=self.action)

    def action(self, args):
        text = args['query']
        result = self.store.search(text, top_k=3)
        if len(result) > 0:
            return json.dumps(result)
        return "No results found for: {}".format(args['query'])


class VectorSearchToolFactory():
    @classmethod
    def qdrant(cls, collection_name):
        store = QdrantStore.create(collection_name=collection_name)
        store.get_collection()
        return VectorSearch(store)


if __name__ == "__main__":
    store = QdrantStore.create(collection_name="test")
    store.get_collection()
    store.upsert_single(3, "test out this world", source="tool test")
    store.wait_for_upsert(3)

    tool = VectorSearchToolFactory.qdrant("test")
    print(tool.definition)
    print(tool.action({"query": "test"}))
