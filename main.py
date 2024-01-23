from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

from gunicorn.app.base import BaseApplication
import yaml

import logging

from llm import LLM

# Configure the logging module
logging.basicConfig(filename='llm.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
api = Api(app)

with open("conf.yml", "r") as f:
    config = yaml.safe_load(f)

PORT = config["PORT"]

llm = LLM(config)


class Health(Resource):
    def get(self):
        return {'message': 'healthy'}, 200

class Generate(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            request_json = request.get_json()
            inputs = request_json['inputs']
            return {'generated_text': llm.complete_code(inputs)}, 200
        else:
            return "Content type is not supported."


##
## Actually setup the Api resource routing here
##

api.add_resource(Health, '/health')
api.add_resource(Generate, '/generate', '/')

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
        'workers': 4,
    }
    StandaloneRandomNumberAPI(app, options).run()
