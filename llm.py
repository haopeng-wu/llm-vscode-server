from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

import yaml


class LLM:
    def __init__(self, conf) -> None:
        self.llm = self.get_openai_model(conf)
        self.END_TOKEN = conf["END_TOKEN"]
        self.START_TOKEN = conf["START_TOKEN"]

    def get_openai_model(self, conf):
        with open(conf["openai_key_file"], "r", encoding="utf-8") as f:
            key_conf = yaml.safe_load(f.read())
        OPENAI_API_KEY = key_conf["OPENAI_API_KEY"]
        OPENAI_API_BASE = key_conf["OPENAI_API_BASE"]
        OPENAI_API_VERSION = key_conf["OPENAI_API_VERSION"]
        DEPLOYMENT = key_conf["DEPLOYMENT"]
        MAX_TOKENS = conf["MAX_TOKENS"]

        return AzureChatOpenAI(
            openai_api_type="azure",
            openai_api_version=OPENAI_API_VERSION,
            openai_api_base=OPENAI_API_BASE,
            openai_api_key=OPENAI_API_KEY,
            deployment_name=DEPLOYMENT,
            temperature=0,
            max_tokens=MAX_TOKENS,
        )

    def get_fore_context(self, inputs):
        return inputs[: inputs.find(self.END_TOKEN)].replace(
            self.START_TOKEN, ""
            )

    def complete_code(self, code_context):
        """Take the input from the request and output.

        args:
            code_context(str): the code_context

        return(dict): the response
        """
        fore_context = self.get_fore_context(code_context)
        system_setting = SystemMessage(
            content="You are a code autocompleter.")
        prompt = f"""
        Please complete code for the following code. Only output code text
        without markdown. Make code completion after the end token.
        \n\n
        {fore_context}
        """
        message = HumanMessage(content=prompt)
        return self.llm.invoke([system_setting, message]).content
