from http.server import HTTPServer

from repository_adapter import JsonFileOrderRepository
from service import OrderService
from web_adapter import create_handler


def run():
    repository = JsonFileOrderRepository()
    service = OrderService(repository)
    handler_class = create_handler(service)

    server = HTTPServer(("localhost", 8001), handler_class)
    print("Hexagonal architecture app running at http://localhost:8001/")
    print("Submit orders using the form in your browser.")
    server.serve_forever()


if __name__ == "__main__":
    run()
