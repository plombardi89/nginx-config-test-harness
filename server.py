#!/usr/bin/env python

from flask import Flask, jsonify, request
from flask_sockets import Sockets

import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
     
# create console handler and set level to info
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)
app.logger.addHandler(handler)
app.config['DEBUG'] = True
sockets = Sockets(app)


def headers_to_dict(headers):
    r = {}
    for k, v in headers.items():
        r[k] = v
        
    return r
    

@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)


@app.route('/api/<path:path>')
def test(path):
    return jsonify({
        'headers': headers_to_dict(request.headers),
        'path': request.path,
        'query_params': request.args,
        'form_fields': request.form
    })

@app.route('/health')
def health_check():
    return jsonify({"healthy": True})

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
