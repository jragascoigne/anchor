"""
mock_api.py
A tiny local mock server that simulates a real API response.
Run with: python mock_api.py
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler

MOCK_USER = {
    "id": 1,
    "name": "John Doe",
    "username": "JohnDoe",
    "email": "john@doe.com",
    "phone": "01-234-567-8901",
    "website": "johndoe.org",
    "address": {
        "street": "Paper Street",
        "suite": "Apt. 123",
        "city": "Drive Thru City",
        "zipcode": "12345",
        # coords are strings to test type mismatches
        "geo": {
            "lat": "-44.53225",
            "lng": "105.39719"
        }
    },
    "company": {
        "name": "Paper Co.",
        "catchPhrase": "So fake it hurts",
        "bs": "fake data for testing purposes"
    }
}


class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/user":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(MOCK_USER).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Silence request logs


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8765), MockHandler)
    print("Mock API running at http://localhost:8765")
    server.serve_forever()