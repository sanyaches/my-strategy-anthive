#!/usr/bin/env python

import json
import random
import math

try:  # For python 3
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:  # For python 2
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

        # Hive object from request payload
        hive = json.loads(payload)

        # Save the map_food
        coords_food = "-,-"
        map_food = []
        for i in range(0, hive['map']['height']):
            map_food.append([])
            for j in range(0, hive['map']['width']):
                if 'food' in hive['map']['cells'][i][j]:
                    map_food[i].append(hive['map']['cells'][i][j]['food'])
                    coords_food += '|' + str(i) + ';' + str(j)
                else:
                    map_food[i].append(0)

        # Search min path to food
        min_coords = []
        min_dist = math.sqrt(hive['map']['width'] ** 2 + hive['map']['height'] ** 2)
        for coords in coords_food.split('|'):
            x = coords.split(',')[0]
            y = coords.split(',')[1]
            new_dist = math.sqrt((hive['ants'][0]['x'] - x) ** 2 +
                                 (hive['ants'][0]['y'] - y) ** 2)
            if new_dist < min_dist:
                min_dist = new_dist
                min_coords.clear()
                min_coords.append(x)
                min_coords.append(y)

        # Loop through ants and give orders
        orders = {}
        for ant in hive['ants']:
            x_ant = hive['ants'][ant]['x']
            y_ant = hive['ants'][ant]['y']
            if (hive['map']['cells'][x_ant - 1][y_ant]['food'] > 0):
                orders[ant] = {
                    "act": ACTIONS['load'],
                    "dir": DIRECTIONS['left']
                }
            elif (hive['map']['cells'][x_ant + 1][y_ant]['food'] > 0):
                orders[ant] = {
                    "act": ACTIONS['load'],
                    "dir": DIRECTIONS['right']
                }
            elif (hive['map']['cells'][x_ant][y_ant - 1]['food'] > 0):
                orders[ant] = {
                    "act": ACTIONS['load'],
                    "dir": DIRECTIONS['up']
                }
            elif (hive['map']['cells'][x_ant][y_ant + 1]['food'] > 0):
                orders[ant] = {
                    "act": ACTIONS['load'],
                    "dir": DIRECTIONS['down']
                }
            if ant['x'] > min_coords[0]:
                orders[ant] = {
                    'act': 'move',
                    'dir': 'left'
                }
            elif ant['x'] < min_coords[0]:
                orders[ant] = {
                    'act': 'move',
                    'dir': 'right'
                }
            elif ant['y'] < min_coords[1]:
                orders[ant] = {
                    'act': 'move',
                    'dir': 'up'
                }
            elif ant['y'] > min_coords[1]:
                orders[ant] = {
                    'act': 'move',
                    'dir': 'down'
                }
        response = json.dumps(orders)
        print(response)

        try:  # For python 3
            out = bytes(response, "utf8")
        except TypeError:  # For python 2
            out = bytes(response)

        self.wfile.write(out)

        # json format sample:
        # {"1":{"act":"load","dir":"down"},"17":{"act":"load","dir":"up"}}
        return


def run():
    server_address = ('0.0.0.0', 7070)
    httpd = HTTPServer(server_address, Handler)
    httpd.serve_forever()


run()
