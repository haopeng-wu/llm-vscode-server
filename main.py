from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from gunicorn.app.base import BaseApplication
import yaml

import logging

# Configure the logging module
logging.basicConfig(filename='llm.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
api = Api(app)

with open("conf.yml", "r") as f:
    config = yaml.safe_load(f)

END_TOKEN = config["END_TOKEN"]
START_TOKEN = config["START_TOKEN"]
MID_TOKEN = config["MID_TOKEN"]
MAX_TOKENS = config["MAX_TOKENS"]

NUM_WORKS = config["NUM_WORKS"]
PORT = config["PORT"]


class LLM:
    verbose = False
    def __init__(self, conf_file) -> None:
        with open(conf_file, "r", encoding="utf-8") as f:
            conf = yaml.safe_load(f.read())
        OPENAI_API_KEY = conf["OPENAI_API_KEY"]
        OPENAI_API_BASE = conf["OPENAI_API_BASE"]
        OPENAI_API_VERSION = conf["OPENAI_API_VERSION"]
        DEPLOYMENT = conf["DEPLOYMENT"]
        self.llm = AzureChatOpenAI(
            openai_api_type="azure",
            openai_api_version=OPENAI_API_VERSION,
            openai_api_base=OPENAI_API_BASE,
            openai_api_key=OPENAI_API_KEY,
            deployment_name=DEPLOYMENT,
            temperature=0,
            max_tokens=MAX_TOKENS,
        )

    def complete_code(self, code_context):
        """Take the input from the request and output.

        args:
            code_context(str): the code_context

        return(dict): the response
        """
        fore_context = get_fore_context(code_context)
        system_setting = SystemMessage(
            content="You are a code autocompleter.")
        prompt = f"""
        Please complete code for the following code. Only output code text without markdown. Make code completion after the end token.
        \n\n
        {fore_context}
        """
        logging.info(fore_context)
        message = HumanMessage(content=prompt)
        return self.llm.invoke([system_setting, message]).content

llm = LLM(".env-35-16k.yml")

def get_fore_context(inputs):
    return inputs[: inputs.find(END_TOKEN)].replace(START_TOKEN,"") 

class Health(Resource):
    def get(self):
        return {'message': 'healthy'}, 200

class Generate(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            request_json = request.get_json()
            inputs = request_json['inputs']
            # Returning a response with status code 200
            return {'generated_text': llm.complete_code(inputs)}, 200
        else:
            return "Content type is not supported."


##
## Actually setup the Api resource routing here
##

# curl http://0.0.0.0:8000/health
api.add_resource(Health, '/health')
# curl http://0.0.0.0:8000/generate -d '{"inputs":"hi"}' -H "Content-Type: application/json" -v
api.add_resource(Generate, '/generate', '/')
 
def run():
    app.run(debug=True)

class StandaloneRandomNumberAPI(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()
    def load_config(self):
            config = {key: value for key, value in self.options.items()
                    if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)
    def load(self):
            return self.application

if __name__ == "__main__":
    options = {
        'bind': '%s:%s' % ('0.0.0.0', PORT),
        'workers': NUM_WORKS,
    }
    StandaloneRandomNumberAPI(app, options).run()
