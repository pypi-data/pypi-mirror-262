import time
from datetime import datetime

from komodo.core.vector_stores.qdrant_store import QdrantStore
from komodo.core.vector_stores.vector_store_helper import VectorStoreHelper
from komodo.framework.komodo_datasource import default_data_directory
from komodo.shared.utils.filestats import file_details
from komodo.shared.utils.globber import Globber
from komodo.store.collection_store import CollectionStore


class Indexer:
    def __init__(self, collection_name: str, path: str = default_data_directory()):
        CollectionStore().get_or_create_collection(collection_name)
        self.collection_name = collection_name
        self.globber = Globber(path, self.__on_created, self.__on_deleted)

    def __on_created(self, filepath):
        print("Created: " + filepath)
        store = CollectionStore()
        collection = store.retrieve_collection(self.collection_name)
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
        collection = store.retrieve_collection(self.collection_name)
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
        store = QdrantStore.create(self.collection_name)
        helper = VectorStoreHelper(filepath)
        try:
            text = helper.text
            data = helper.data
            print("Content: " + text[:60])
            store.upsert_batched(data)
        except Exception as e:
            print("Error indexing: " + filepath)
            print(e)

    def add_intelligence(self, filepath):
        print("Adding intelligence to: " + filepath)

    def remove(self, filepath):
        print("Removing from index: " + filepath)
        store = QdrantStore.create(self.collection_name)
        store.delete_all_by_source(filepath)

    def delete_all(self):
        store = QdrantStore.create(self.collection_name)
        store.delete_all()
        store = CollectionStore()
        store.reset_default_collection(self.collection_name)

    def run(self, max_updates=1, update_interval=5, reindex=False):
        if reindex:
            self.delete_all()

        self.globber.start()
        update_count = 1  # start runs the initial update
        while update_count < max_updates or max_updates == 0:
            time.sleep(update_interval)
            self.globber.updates()
            update_count += 1

        print("Exiting after " + str(update_count) + " updates...")


if __name__ == "__main__":
    qdrant = QdrantStore.create("test")
    store = CollectionStore()
    collection = store.get_or_create_collection("default", "My Collection", "My personal collection")
    path = '/Users/komodo/dev/komodo-sdk/sample/data/komodo'  # os.path.dirname(__file__)
    indexer = Indexer("default", path)
    indexer.run(update_interval=5)
