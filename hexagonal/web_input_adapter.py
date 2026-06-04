from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

from domain import PRODUCTS
from ports import OrderInputPort

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Hexagonal Order Form</title>
</head>
<body>
  <h1>Hexagonal Architecture Order Form</h1>
  <p>{message}</p>
  <form method="POST">
    <label>Product:</label>
    <select name="product_id">
      {options}
    </select>
    <br /><br />
    <label>Quantity:</label>
    <input type="number" name="quantity" value="1" min="1" />
    <br /><br />
    <button type="submit">Submit Order</button>
  </form>
</body>
</html>
"""


def render_form(message="Please choose a product and quantity."):
    options = "\n".join(
        f'<option value="{item.id}">{item.name} (${item.price})</option>'
        for item in PRODUCTS
    )
    return HTML_FORM.format(message=message, options=options)


class HexagonalHandler(BaseHTTPRequestHandler):
    def __init__(self, order_port: OrderInputPort, *args, **kwargs):
        self.order_port = order_port
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.respond(render_form())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        data = parse_qs(body)

        product_id = data.get("product_id", [""])[0]
        quantity_text = data.get("quantity", ["1"])[0]

        try:
            quantity = int(quantity_text)
        except ValueError:
            success = False
            message = "Quantity must be a number."
        else:
            success, message = self.order_port.submit_order(product_id, quantity)

        self.respond(render_form(message if success else f"Error: {message}"))

    def respond(self, html_text):
        content = html_text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def create_handler(order_port):
    def handler(*args, **kwargs):
        HexagonalHandler(order_port, *args, **kwargs)

    return handler
