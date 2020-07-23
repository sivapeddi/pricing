import re
import uuid
import requests
from dataclasses import dataclass, field
from typing import Dict, List
from bs4 import BeautifulSoup
from models.model import Model


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    _id: str = field(default=uuid.uuid4().hex)

    def load_price(self):
        response = requests.get(self.url).content
        soup = BeautifulSoup(response, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text
        pattern = re.compile(r"(\d+,?\d+\.\d\d)")
        match = pattern.search(string_price)
        self.price = float(match.group(1).replace(",", ""))
        print(self.price)
        return self.price

    def json(self):
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "price": self.price,
            "query": self.query,
        }