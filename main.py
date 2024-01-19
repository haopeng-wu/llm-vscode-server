from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
import yaml

app = Flask(__name__)
api = Api(app)


class LLM:
    def __init__(self) -> None:
        with open(".env.yml", "r", encoding="utf-8") as f:
            conf = yaml.safe_load(f.read())
        OPENAI_API_KEY = conf["OPENAI_API_KEY"]
        OPENAI_API_BASE = conf["OPENAI_API_BASE"]
        self.llm = AzureChatOpenAI(
            openai_api_type="azure",
            openai_api_version="2023-05-15",
            openai_api_base=OPENAI_API_BASE,
            openai_api_key=OPENAI_API_KEY,
            deployment_name="gpt-35-turbo-16k",
            temperature=0,
        )

    def complete(self, query):
        # Run the LLM
        message = HumanMessage(
            content=query
        )
        return self.llm([message]).content

llm = LLM()

class Health(Resource):
    def get(self):
        return {'message': 'healthy'}, 200

class Generate(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            request_json = request.get_json()
            input = request_json['inputs']

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