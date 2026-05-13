from dataclasses import dataclass


@dataclass
class Product:
    id: str
    name: str
    price: float


@dataclass
class Order:
    product_id: str
    quantity: int

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "quantity": self.quantity,
        }


PRODUCTS = [
    Product(id="p1", name="Notebook", price=12.50),
    Product(id="p2", name="Pen set", price=5.75),
    Product(id="p3", name="Wireless mouse", price=22.00),
    Product(id="p4", name="Backpack", price=34.90),
    Product(id="p5", name="Coffee mug", price=8.20),
]


def find_product(product_id):
    for product in PRODUCTS:
        if product.id == product_id:
            return product
    return None
