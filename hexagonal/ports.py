from abc import ABC, abstractmethod

from domain import Order


class OrderInputPort(ABC):
    @abstractmethod
    def submit_order(self, product_id, quantity):
        raise NotImplementedError


class OrderRepositoryPort(ABC):
    @abstractmethod
    def save_order(self, order: Order):
        raise NotImplementedError
