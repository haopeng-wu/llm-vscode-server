from argparse import ArgumentParser
import logging

import torch
from torch.multiprocessing.reductions import ForkingPickler
import zmq

import torch. multiprocessing as mp
from accelerate import Accelerator
from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa: E402


def load_model():
    accelerator = Accelerator()
    tokenizer = AutoTokenizer.from_pretrained(
                "stabilityai/stable-code-3b")
    model = AutoModelForCausalLM.from_pretrained(
        "stabilityai/stable-code-3b",
        torch_dtype="auto",
        )
    device = accelerator.device
    model.to(device)
    return model


def share_object(obj, url):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(url)
    while True:
        logging.info("Waiting for requests on %s", url)
        message = socket.recv()
        logging.info("Got a message from %d", ForkingPickler.loads(message))
        socket.send(ForkingPickler.dumps(obj))


if __name__ == '__main__':
    parser = ArgumentParser(description="Serve model")
    parser.add_argument("--listen-address", default="tcp://127.0.0.1:5555")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logging.info("Loading model")

    model = load_model()
    share_object(model, args.listen_address)
