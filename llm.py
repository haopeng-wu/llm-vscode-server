from accelerate import Accelerator
from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa: E402

from torch.multiprocessing.reductions import ForkingPickler
import zmq

# Configure the logging module
import logging
import os


class LLM:
    def __init__(self, model) -> None:
        self.model = model
        self.tokenizer = AutoTokenizer.from_pretrained(
            "stabilityai/stable-code-3b")

    # @staticmethod
    # def request_model(zmq_url: str):
    #     logging.info("Connecting")
    #     context = zmq.Context()
    #     with context.socket(zmq.REQ) as socket:
    #         socket.connect(zmq_url)
    #         logging.info("Sending request")
    #         socket.send(ForkingPickler.dumps(os.getpid()))
    #         logging.info("Waiting for a response")
    #         model = ForkingPickler.loads(socket.recv())
    #     logging.info("Got response from object server")
    #     return model

    def complete_code(self, code_context):
        """Take the input from the request and output.

        args:
            code_context(str): the code_context

        return(dict): the response
        """
        inputs = self.tokenizer(code_context,
                            return_tensors="pt").to(self.model.device)
        tokens = self.model.generate(
            **inputs,
            max_new_tokens=48,
            temperature=0.2,
            do_sample=True,
        )
        completion = self.tokenizer.decode(tokens[0], skip_special_tokens=True)
        return completion
