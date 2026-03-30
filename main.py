#!/usr/bin/env python3
import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# In-memory data stores
clients = {}
products = {}
categories = {}
services = {}

# ID counters
next_client_id = 1
next_product_id = 1
next_category_id = 1
next_service_id = 1


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        
        # List endpoints
        if path == "/clients":
            return self.json_response(list(clients.values()))
        if path == "/products":
            return self.json_response(list(products.values()))
        if path == "/categories":
            return self.json_response(list(categories.values()))
        if path == "/services":
            return self.json_response(list(services.values()))
        
        # Get by ID endpoints
        match = re.match(r"^/clients/(\d+)$", path)
        if match:
            client_id = int(match.group(1))
            if client_id in clients:
                return self.json_response(clients[client_id])
            return self.json_response({"error": "not found"}, 404)
        
        match = re.match(r"^/products/(\d+)$", path)
        if match:
            product_id = int(match.group(1))
            if product_id in products:
                return self.json_response(products[product_id])
            return self.json_response({"error": "not found"}, 404)
        
        match = re.match(r"^/categories/(\d+)$", path)
        if match:
            category_id = int(match.group(1))
            if category_id in categories:
                return self.json_response(categories[category_id])
            return self.json_response({"error": "not found"}, 404)
        
        match = re.match(r"^/services/(\d+)$", path)
        if match:
            service_id = int(match.group(1))
            if service_id in services:
                return self.json_response(services[service_id])
            return self.json_response({"error": "not found"}, 404)
        
        self.json_response({"error": "not found"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        body = self.get_body()
        
        if path == "/clients":
            global next_client_id
            client_id = next_client_id
            next_client_id += 1
            body["id"] = client_id
            clients[client_id] = body
            return self.json_response(body, 201)
        
        if path == "/products":
            global next_product_id
            product_id = next_product_id
            next_product_id += 1
            body["id"] = product_id
            products[product_id] = body
            return self.json_response(body, 201)
        
        if path == "/categories":
            global next_category_id
            category_id = next_category_id
            next_category_id += 1
            body["id"] = category_id
            categories[category_id] = body
            return self.json_response(body, 201)
        
        if path == "/services":
            global next_service_id
            service_id = next_service_id
            next_service_id += 1
            body["id"] = service_id
            services[service_id] = body
            return self.json_response(body, 201)
        
        self.json_response({"error": "not found"}, 404)

    def do_PUT(self):
        path = urlparse(self.path).path
        body = self.get_body()
        
        match = re.match(r"^/clients/(\d+)$", path)
        if match:
            client_id = int(match.group(1))
            if client_id in clients:
                body["id"] = client_id
                clients[client_id] = body
                return self.json_response(body)
            return self.json_response({"error": "not found"}, 404)
        
        match = re.match(r"^/products/(\d+)$", path)
        if match:
            product_id = int(match.group(1))
            if product_id in products:
                body["id"] = product_id
                products[product_id] = body
                return self.json_response(body)
            return self.json_response({"error": "not found"}, 404)
        
        match = re.match(r"^/categories/(\d+)$", path)
        if match:
            category_id = int(match.group(1))
            if category_id in categories:
                body["id"] = category_id
                categories[category_id] = body
                return self.json_response(body)
            return self.json_response({"error": "not found"}, 404)
        
        match = re.match(r"^/services/(\d+)$", path)
        if match:
            service_id = int(match.group(1))
            if service_id in services:
                body["id"] = service_id
                services[service_id] = body
                return self.json_response(body)
            return self.json_response({"error": "not found"}, 404)
        
        self.json_response({"error": "not found"}, 404)

    def do_DELETE(self):
        path = urlparse(self.path).path
        
        match = re.match(r"^/clients/(\d+)$", path)
        if match:
            client_id = int(match.group(1))
            if client_id in clients:
                del clients[client_id]
                return self.json_response({"deleted": True})
            return self.json_response({"error": "not found"}, 404)
        
        match = re.match(r"^/products/(\d+)$", path)
        if match:
            product_id = int(match.group(1))
            if product_id in products:
                del products[product_id]
                return self.json_response({"deleted": True})
            return self.json_response({"error": "not found"}, 404)
        
        match = re.match(r"^/categories/(\d+)$", path)
        if match:
            category_id = int(match.group(1))
            if category_id in categories:
                del categories[category_id]
                return self.json_response({"deleted": True})
            return self.json_response({"error": "not found"}, 404)
        
        match = re.match(r"^/services/(\d+)$", path)
        if match:
            service_id = int(match.group(1))
            if service_id in services:
                del services[service_id]
                return self.json_response({"deleted": True})
            return self.json_response({"error": "not found"}, 404)
        
        self.json_response({"error": "not found"}, 404)

    def get_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(content_length)) if content_length else {}

    def json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        print(f"[{self.client_address[0]}] {format % args}")


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), Handler)
    print("Server running on http://localhost:8000")
    print("Routes: /clients, /products, /categories, /services")
    server.serve_forever()
