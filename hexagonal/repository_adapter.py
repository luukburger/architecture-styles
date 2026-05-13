import json
import os

from domain import Order
from ports import OrderRepositoryPort


class JsonFileOrderRepository(OrderRepositoryPort):
    def __init__(self, path=None):
        base_dir = os.path.dirname(__file__)
        self.path = path or os.path.join(base_dir, "orders.json")
        if not os.path.exists(self.path):
            self._write_orders([])

    def save_order(self, order: Order):
        orders = self._load_orders()
        orders.append(order.to_dict())
        self._write_orders(orders)

    def _load_orders(self):
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_orders(self, orders):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(orders, file, indent=2)
