from accelerate import Accelerator
accelerator = Accelerator()
from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa: E402
# Configure the logging module
import logging


tokenizer = AutoTokenizer.from_pretrained(
            "stabilityai/stable-code-3b")
model = AutoModelForCausalLM.from_pretrained(
    "stabilityai/stable-code-3b",
    torch_dtype="auto",
    )
device = accelerator.device
model.to(device)


class LLM:
    def __init__(self, conf) -> None:
        # self.tokenizer = AutoTokenizer.from_pretrained(
        #             "stabilityai/stable-code-3b")
        # self.model = AutoModelForCausalLM.from_pretrained(
        #     "stabilityai/stable-code-3b",
        #     torch_dtype="auto",
        #     )
        # self.device = accelerator.device
        # self.model.to(self.device)
        pass

    def complete_code(self, code_context):
        """Take the input from the request and output.

        args:
            code_context(str): the code_context

        return(dict): the response
        """
        logging.debug("code_context")
        logging.debug(code_context)
        logging.debug("\n")
        # inputs = self.tokenizer(code_context,
        #                         return_tensors="pt").to(self.model.device)
        # tokens = self.model.generate(
        #     **inputs,
        #     max_new_tokens=48,
        #     temperature=0.2,
        #     do_sample=True,
        # )
        # completion = self.tokenizer.decode(tokens[0], skip_special_tokens=True)
        logging.debug(model.device)
        inputs = tokenizer(code_context,
                           return_tensors="pt").to(model.device)
        tokens = model.generate(
            **inputs,
            max_new_tokens=48,
            temperature=0.2,
            do_sample=True,
        )
        completion = tokenizer.decode(tokens[0], skip_special_tokens=True)
        logging.debug("completion")
        logging.debug(completion)
        return completion
