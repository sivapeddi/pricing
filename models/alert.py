import uuid
from typing import List, Dict

from libs.mailgun import Mailgun
from models.item import Item
from models.model import Model
from dataclasses import dataclass, field
from models.user import User


@dataclass(eq=False)
class Alert(Model):
    collection: str = field(init=False, default="alerts")
    alert_name: str
    item_id: str
    user_email: str
    price_limit: float
    _id: str = field(default=uuid.uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "alert_name": self.alert_name,
            "price_limit": self.price_limit,
            "item_id": self.item_id,
            "user_email": self.user_email
        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print("price is in desired range")
            Mailgun.send_mail(
                [self.user_email],
                f"Notification for {self.alert_name}",
                f"Your alert {self.alert_name} has reached a price under {self.price_limit}. The latest price is {self.item.price}. Go to this address to check your item: {self.item.url}",
                f"<p>Your alert {self.alert_name} has reached a price under {self.price_limit}"

            )
