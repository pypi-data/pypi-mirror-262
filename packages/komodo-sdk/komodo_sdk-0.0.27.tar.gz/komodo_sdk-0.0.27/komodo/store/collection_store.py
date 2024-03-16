import uuid

from komodo.proto.generated.collection_pb2 import Collection, Intelligence
from komodo.store.redis_database import RedisDatabase, get_redis_server


class CollectionStore:
    DEFAULT_GUID = "default"
    DEFAULT_NAME = "Default Collection"
    DEFAULT_DESCRIPTION = "Default Appliance Collection"

    def __init__(self, database=RedisDatabase.COLLECTIONS):
        self.redis = get_redis_server(database)

    def get_or_create_collection(self, guid, name, description):
        if guid is None or guid == "":
            guid = str(uuid.uuid4())
            collection = Collection(name=name, description=description)
            collection.guid = guid
            self.store_collection(collection)
        else:
            collection = self.retrieve_collection(guid)
            if not collection:
                collection = Collection(name=name, description=description)
                collection.guid = guid
                self.store_collection(collection)
        return collection

    def get_default_collection(self, shortcode):
        collection = self.get_or_create_collection(self.DEFAULT_GUID, self.DEFAULT_NAME, self.DEFAULT_DESCRIPTION)
        self.add_appliance_collection(collection.guid, shortcode)
        return collection

    def reset_default_collection(self, shortcode):
        if self.retrieve_collection(self.DEFAULT_GUID):
            self.remove_collection(self.DEFAULT_GUID)
        return self.get_default_collection(shortcode)

    def store_collection(self, collection: Collection):
        collection_data = collection.SerializeToString()
        key = f"collection:{collection.guid}"
        self.redis.set(key, collection_data)

    def retrieve_collection(self, guid):
        key = f"collection:{guid}"
        collection_data = self.redis.get(key)
        if collection_data:
            collection = Collection()
            collection.ParseFromString(collection_data)
            return collection
        else:
            return None

    def remove_collection(self, guid):
        key = f"collection:{guid}"
        self.redis.delete(key)
        keys = self.redis.keys(f"user:*:collection:{guid}")
        for key in keys:
            self.redis.delete(key)
        keys = self.redis.keys(f"appliance:*:collection:{guid}")
        for key in keys:
            self.redis.delete(key)

    def retrieve_all_collections(self):
        keys = self.redis.keys("collection:*")
        collections = []
        for key in keys or []:
            collection_data = self.redis.get(key)
            collection = Collection()
            collection.ParseFromString(collection_data)
            collections.append(collection)
        return collections

    def add_user_collection(self, user_email, guid):
        key = f"user:{user_email}:collection:{guid}"
        self.redis.sadd(key, guid)

    def remove_user_collection(self, user_email, guid):
        key = f"user:{user_email}:collection:{guid}"
        self.redis.delete(key)

    def exists_user_collection(self, user_email, guid):
        key = f"user:{user_email}:collection:{guid}"
        return self.redis.exists(key)

    def retrieve_collections_by_user(self, user_email):
        keys = self.redis.keys(f"user:{user_email}:collection:*")
        collections = []
        for key in keys or []:
            guid = key.decode('utf-8').split(":")[-1]
            collection = self.retrieve_collection(guid)
            collections.append(collection)
        return collections

    def add_appliance_collection(self, guid, shortcode):
        key = f"appliance:{shortcode}:collection:{guid}"
        self.redis.sadd(key, guid)

    def remove_appliance_collection(self, guid, shortcode):
        key = f"appliance:{shortcode}:collection:{guid}"
        self.redis.delete(key)

    def exists_appliance_collection(self, guid, shortcode):
        key = f"appliance:{shortcode}:collection:{guid}"
        return self.redis.exists(key)

    def retrieve_collections_by_appliance(self, shortcode):
        keys = self.redis.keys(f"appliance:{shortcode}:collection:*")
        collections = []
        for key in keys or []:
            guid = key.decode('utf-8').split(":")[-1]
            collection = self.retrieve_collection(guid)
            collections.append(collection)
        return collections

    def add_intelligence(self, guid, source, intelligence: Intelligence):
        intelligence_data = intelligence.SerializeToString()
        key = f"collection:{guid}:intelligence:{source}"
        self.redis.set(key, intelligence_data)

    def retrieve_intelligence(self, guid, source):
        key = f"collection:{guid}:intelligence:{source}"
        intelligence_data = self.redis.get(key)
        if intelligence_data:
            intelligence = Intelligence()
            intelligence.ParseFromString(intelligence_data)
            return intelligence
        else:
            return None

    def remove_intelligence(self, guid, source):
        key = f"collection:{guid}:intelligence:{source}"
        self.redis.delete(key)


if __name__ == "__main__":
    store = CollectionStore(database=RedisDatabase.TEST)
    collection = Collection(name="Test Collection", description="Test Description")
    collection.guid = "123"
    store.store_collection(collection)
    print(store.retrieve_collection("123"))

    user_email = "a@b.com"
    store.add_user_collection(user_email, "123")
    print(store.retrieve_collections_by_user(user_email))

    shortcode = "test"
    store.add_appliance_collection("123", shortcode)
    print(store.retrieve_collections_by_appliance(shortcode))

    collections = store.retrieve_all_collections()
    for collection in collections:
        print(collection)
        print(collection.guid)
        store.remove_collection(collection.guid)
    print(store.retrieve_all_collections())
    print(store.retrieve_collections_by_user(user_email))
    print(store.retrieve_collections_by_appliance(shortcode))

    intelligence = Intelligence()
    intelligence.source = "test"
    intelligence.summary = "test"
    intelligence.faq.add(question="test", answer="test")
    intelligence.faq.add(question="test2", answer="test2")

    store.add_intelligence(collection.guid, "test", intelligence)
    print(store.retrieve_intelligence(collection.guid, "test"))

    store.remove_intelligence(collection.guid, "test")
    print(store.retrieve_intelligence(collection.guid, "test"))
    store.redis.flushdb()
