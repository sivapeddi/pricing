import re
import uuid
from typing import Dict
from models.model import Model
from dataclasses import dataclass, field


@dataclass(eq=False)
class Store(Model):
    collection: str = field(init=False, default="store")
    name: str
    url_prefix: str
    tag_name: str
    query: Dict
    _id: str = field(default=uuid.uuid4().hex)

    def json(self):
        return {
            "name": self.name,
            "_id": self._id,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_name(cls, store_name: str) -> "Store":
        return cls.find_one_by("name", store_name)

    @classmethod
    def get_by_url_prefix(cls, url_prefix: str) -> "Store":
        url_regex = {"$regex": f"^{url_prefix}"}
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url:str) -> "Store":
        pattern = re.compile(r"(https?://.*?/)")
        match = pattern.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)