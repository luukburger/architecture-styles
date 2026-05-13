from domain import Order, find_product


class OrderService:
    def __init__(self, repository):
        self.repository = repository

    def submit_order(self, product_id, quantity):
        product = find_product(product_id)
        if product is None:
            return False, "Unknown product."

        if quantity <= 0:
            return False, "Quantity must be greater than zero."

        order = Order(product_id=product_id, quantity=quantity)
        self.repository.save_order(order)
        return True, f"Order saved: {quantity} x {product.name}"
