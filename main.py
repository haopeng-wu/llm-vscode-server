from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import yaml
import json

app = Flask(__name__)
api = Api(app)


class LLM:
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
        )

    def complete(self, query):
        """Answer to a query."""
        system_setting = SystemMessage(
            content="You help to complete the user's code.")
        
        message = HumanMessage(content=query)
        return self.llm.invoke([system_setting, message]).content
    
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
        Please complete code for the following code. Make code completion after the end token.
        \n\n
        {code_context}
        """
        message = HumanMessage(content=prompt)
        return self.llm.invoke([system_setting, message]).content

llm = LLM(".env-35-16k.yml")

def get_fore_context(inputs):
    return inputs[: inputs.find("{end token}")].replace("{start token}","")

class Health(Resource):
    def get(self):
        return {'message': 'healthy'}, 200

class Generate(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            request_json = request.get_json()
            inputs = request_json['inputs']
            llm.complete_code(inputs)
            # Returning a response with status code 200
            return {'completion': llm.complete(input)}, 200
        else:
            return "Content type is not supported."
        
        


##
## Actually setup the Api resource routing here
##

# curl http://localhost:5000/health
api.add_resource(Health, '/health')
# curl http://localhost:5000/generate -d '{"inputs":"hi"}' -H "Content-Type: application/json" -v
api.add_resource(Generate, '/generate')


if __name__ == '__main__':
    app.run(debug=True)