# Configure the logging module
import logging
import os

from torch.multiprocessing.reductions import ForkingPickler
import zmq

def request_model(zmq_url: str):
        logging.info("Connecting")
        context = zmq.Context()
        with context.socket(zmq.REQ) as socket:
            socket.connect(zmq_url)
            logging.info("Sending request")
            socket.send(ForkingPickler.dumps(os.getpid()))
            logging.info("Waiting for a response")
            model = ForkingPickler.loads(socket.recv())
        logging.info("Got response from object server")
        return model