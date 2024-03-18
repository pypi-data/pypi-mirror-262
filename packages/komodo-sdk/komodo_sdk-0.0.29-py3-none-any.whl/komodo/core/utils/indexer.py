import time
from datetime import datetime

from komodo.core.vector_stores.qdrant_store import QdrantStore
from komodo.core.vector_stores.vector_store_helper import VectorStoreHelper
from komodo.framework.komodo_datasource import default_data_directory
from komodo.shared.utils.filestats import file_details
from komodo.shared.utils.globber import Globber
from komodo.store.collection_store import CollectionStore


class Indexer:
    def __init__(self, store: QdrantStore, collection_guid: str, path: str = default_data_directory()):
        self.store = store
        self.collection_guid = collection_guid
        self.globber = Globber(path, self.__on_created, self.__on_deleted)

    def __on_created(self, filepath):
        print("Created: " + filepath)
        store = CollectionStore()
        collection = store.retrieve_collection(self.collection_guid)
        file = self.find_file(collection, filepath)
        if not file:
            file = file_details(filepath)
            collection.files.append(file)

        file = self.find_file(collection, filepath)
        if file and file.indexed_at:
            print("Already indexed: " + filepath)
            return

        self.index(filepath)
        file.indexed_at = datetime.utcnow().isoformat() + 'Z'
        store.store_collection(collection)

    def __on_deleted(self, filepath):
        print("Deleted: " + filepath)
        store = CollectionStore()
        collection = store.retrieve_collection(self.collection_guid)
        file = self.find_file(collection, filepath)
        if file:
            self.remove(filepath)
            collection.files.remove(file)
            store.store_collection(collection)

    @staticmethod
    def find_file(collection, filepath):
        for file in collection.files or []:
            if file.path == filepath:
                return file
        return None

    def index(self, filepath):
        print("Indexing: " + filepath)
        helper = VectorStoreHelper(filepath)
        try:
            text = helper.text
            data = helper.data
            print("Content: " + text[:60])
            self.store.upsert_batched(data)
        except Exception as e:
            print("Error indexing: " + filepath)
            print(e)

    def add_intelligence(self, filepath):
        print("Adding intelligence to: " + filepath)

    def remove(self, filepath):
        print("Removing from index: " + filepath)
        self.store.delete_all_by_source(filepath)

    def run(self, max_updates=1, update_interval=5):
        self.globber.start()
        update_count = 1  # start runs the initial update
        while update_count < max_updates or max_updates == 0:
            time.sleep(update_interval)
            self.globber.updates()
            update_count += 1

        print("Exiting after " + str(update_count) + " updates...")


if __name__ == "__main__":
    qdrant = QdrantStore(shortcode="default", name="Default Store", collection_name="test")
    store = CollectionStore()
    collection = store.get_or_create_collection("default", "My Collection", "My personal collection")
    path = '/Users/komodo/dev/komodo-sdk/sample/data/komodo'  # os.path.dirname(__file__)
    indexer = Indexer(qdrant, "default", path)
    indexer.run(update_interval=5)
