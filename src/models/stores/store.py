import uuid
import src.models.stores.constants as StoreConstants
from src.common.database import Database
import src.models.stores.errors as StoreErrors


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, item_name_tag, item_name_query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self.item_name_tag = item_name_tag
        self.item_name_query = item_name_query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query,
            "item_name_tag": self.item_name_tag,
            "item_name_query": self.item_name_query
        }

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"_id": id}))

    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION, {'_id': self._id}, self.json())

    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"name": store_name}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(url_prefix) }}))

    @classmethod
    def find_by_url(cls, url):
        """
        Return a store from item's URL like "http://www.amazon.in/Neutrogena-Ultra-Sheer-Drytouch-Sunblock/dp/B000EPA4GQ/"
        :param url: URL of the item
        :return: Store, if the URL matches an entry in the Stores collection, else StoreNotFound Exception
        """
        url_length = len(url)
        for i in range(0, url_length):
            try:
                store = cls.get_by_url_prefix(url[:url_length-i])
                if store:
                    return store
            except:
                pass

        return StoreErrors.StoreNotFound("The URL prefix for the item doesn't math any store in the DB")

    @classmethod
    def get_all_stores(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]

    def delete(self):
        Database.remove(StoreConstants.COLLECTION, {'_id': self._id})
