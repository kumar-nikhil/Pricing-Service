import uuid
from typing import Dict
from libs.mailgun import MailGun
from models.item import Item
from models.user.user import User
from models.model import Model
from dataclasses import dataclass, field


@dataclass(eq=False)
class Alert(Model):
    collection: str = field(init=False, default="alerts")
    item_id: str
    name: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "price_limit": self.price_limit,
            "item_id": self.item_id,
            "user_email": self.user_email
        }

    def load_item_price(self):
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(f"Item {self.item} has reached the price under {self.price_limit}, Latest Price : {self.item.price}.")
            MailGun.send_email([
                                "niksguru.1@gmail.com"],
                                f"Notification for {self.name}",
                                f"Your alert {self.name} has reached a price under {self.price_limit}, The latest price is {self.item.price}, "
                                f"Go to this address to check your item {self.item.url}.",
                                f'<p> Your alert {self.name} has reached a price under {self.price_limit} </p>'
                                f'<p>The latest price is {self.item.price}</p>'
                                f'Click <a href="{self.item.url}">here</a> to purchase your item. </p> ')
