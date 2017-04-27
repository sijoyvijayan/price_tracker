import re
import uuid

import requests
from bs4 import BeautifulSoup

from src.common.database import Database
import src.models.items.constants as ItemConstants
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.url = url
        store = Store.find_by_url(url)
        self._id = uuid.uuid4().hex if _id is None else _id
        self.tag_name = store.tag_name
        self.query = store.query
        self.item_name_tag = store.item_name_tag
        self.item_name_query = store.item_name_query
        self.name = name
        self.price = None if price is None else price

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def get_item_name(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        request = requests.get(self.url, headers=headers)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.item_name_tag, self.item_name_query)
        self.name = element.text.strip()
        return self.name

    def load_price(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        request = requests.get(self.url, headers=headers)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()
        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)
        self.price = float(match.group().replace(',', ''))
        return self.price

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {'_id': self._id}, self.json())

    def find_from_mongo(self):
        Database.find(ItemConstants.COLLECTION, {"name": self.name})

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "price": self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))
