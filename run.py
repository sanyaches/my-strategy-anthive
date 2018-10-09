#!/usr/bin/env python

import json
import random
from http.server import BaseHTTPRequestHandler, HTTPServer

ACTIONS = ["move", "eat", "load", "unload"]
DIRECTIONS = ["up", "down", "right", "left"]


class Handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        self._set_headers()
        payload = self.rfile.read(int(self.headers['Content-Length']))
        response = {}

        # Hive object from request payload
        hive = json.loads(payload)

        # Loop through ants and give orders
        for ant in hive['ants']:
            response[ant] = {
                "act": ACTIONS[random.randint(0, 3)],
                "dir": DIRECTIONS[random.randint(0, 3)]
            }

        print("Orders:", response)
        self.wfile.write(bytes(json.dumps(response), "utf8"))

        # json format sample:
        # {"1":{"act":"load","dir":"down"},"17":{"act":"load","dir":"up"}}
        return


def run():
    print("let's ant")
    server_address = ('127.0.0.1', 7070)
    httpd = HTTPServer(server_address, Handler)
    httpd.serve_forever()


run()
