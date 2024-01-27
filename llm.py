from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate


import yaml


class LLM:
    def __init__(self, conf) -> None:
        self.END_TOKEN = conf["END_TOKEN"]
        self.START_TOKEN = conf["START_TOKEN"]
        self.MID_TOKEN = conf["MID_TOKEN"]
        self.MAX_TOKENS = conf["MAX_TOKENS"]
        # read secret
        with open(conf["openai_key_file"], "r", encoding="utf-8") as f:
            key_conf = yaml.safe_load(f.read())
        self.OPENAI_API_KEY = key_conf["OPENAI_API_KEY"]
        self.OPENAI_API_BASE = key_conf["OPENAI_API_BASE"]
        self.OPENAI_API_VERSION = key_conf["OPENAI_API_VERSION"]
        self.DEPLOYMENT = key_conf["DEPLOYMENT"]

        if conf["is_chat_model"]:
            self.model = self.get_chat_model()
        else:
            self.model = self.get_llm_model()


    def get_chat_model(self):
        return AzureChatOpenAI(
            openai_api_type="azure",
            openai_api_version=self.OPENAI_API_VERSION,
            openai_api_base=self.OPENAI_API_BASE,
            openai_api_key=self.OPENAI_API_KEY,
            deployment_name=self.DEPLOYMENT,
            temperature=0,
            max_tokens=self.MAX_TOKENS,
        )
    
    def get_llm_model(self):
        return AzureOpenAI(
            openai_api_type="azure",
            openai_api_version=self.OPENAI_API_VERSION,
            openai_api_base=self.OPENAI_API_BASE,
            openai_api_key=self.OPENAI_API_KEY,
            deployment_name=self.DEPLOYMENT,
            temperature=0,
            max_tokens=self.MAX_TOKENS,
        )

    def get_fore_context(self, inputs):
        return inputs[: inputs.find(self.END_TOKEN)].replace(
            self.START_TOKEN, ""
            )
    
    def replace_pos_token(self, context):
        return context.replace(self.START_TOKEN, "{start_token}"
                               ).replace(self.END_TOKEN, "{middle_token}"
                                         ).replace(self.MID_TOKEN, "{end_token}")

    def complete_code(self, code_context):
        """Take the input from the request and output.

        args:
            code_context(str): the code_context

        return(dict): the response
        """
        prompt_context = f"""Please insert code in the middle of following code snippet. The code snippet starts
            with {self.START_TOKEN} and ends by {self.MID_TOKEN}. Insert code right after {self.MID_TOKEN}.
            The inserted code will be used in place in a code editor."""
        prompt_template = PromptTemplate.from_template(
            prompt_context + "Only output the inserted code. The code snippet is the following, delimited by ```. \n\n```{code_context}```")
        chain = prompt_template | self.model 
        return chain.invoke({"code_context": code_context})
