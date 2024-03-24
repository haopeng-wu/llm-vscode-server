from flask import Flask, request
from flask_restful import Api, Resource

from gunicorn.app.base import BaseApplication
import yaml

from llm import LLM

# Configure the logging module
import logging
logging.basicConfig(filename="llm.log",
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
api = Api(app)


class Health(Resource):
    def get(self):
        return {'message': 'healthy'}, 200


class Generate(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            inputs = request.get_json()['inputs']
            llm = LLM(app.config['MODEL'])
            return {'generated_text': llm.complete_code(inputs)}, 200
        else:
            return "Content type is not supported."


api.add_resource(Health, '/health')
api.add_resource(Generate, '/generate', '/')
