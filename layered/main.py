from http.server import HTTPServer

from repository import JsonFileOrderRepository
from service import OrderService
from web import create_handler


def run():
    repository = JsonFileOrderRepository()
    service = OrderService(repository)
    handler_class = create_handler(service)

    server = HTTPServer(("localhost", 8000), handler_class)
    print("Layered architecture app running at http://localhost:8000/")
    print("Submit orders using the form in your browser.")
    server.serve_forever()


if __name__ == "__main__":
    run()
