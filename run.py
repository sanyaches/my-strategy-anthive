#!/usr/bin/env python

import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        mockActions = {"18": 12, "19": 10, "20": 24, "21": 13}

        self.wfile.write(bytes(json.dumps(mockActions), "utf8"))
        return


def run():
    print("let's ant")
    server_address = ('127.0.0.1', 7070)
    httpd = HTTPServer(server_address, Handler)
    httpd.serve_forever()


run()
