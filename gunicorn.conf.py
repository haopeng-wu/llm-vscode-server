import logging

from client import request_model
from main import app

import yaml

logging.basicConfig(level=logging.INFO)


PORT = 8000

bind = f"0.0.0.0:{PORT}"
workers = 4
zmq_url = "tcp://127.0.0.1:5555"


def post_fork(server, worker):
    app.config['MODEL'] = request_model(zmq_url)
